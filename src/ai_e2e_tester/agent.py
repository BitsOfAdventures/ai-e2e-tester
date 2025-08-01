import logging
import os
import time
from collections import defaultdict
from typing import List, Dict
from urllib.parse import urlparse, urlunparse

from ai_e2e_tester.browser.actions import ACTION_REGISTRY
from ai_e2e_tester.browser.guards.domain_guard import ensure_stay_on_domain
from ai_e2e_tester.browser.session import BrowserSession
from ai_e2e_tester.browser.visited_page import VisitedPage
from ai_e2e_tester.llm.openai import OpenAiWrapper
from ai_e2e_tester.reporting.console import ConsoleReporter
from ai_e2e_tester.utils import load_config

logger = logging.getLogger('ai-e2e-tester.agent')


class TestingAgent:
    """
    The TestingAgent is an intermediary allowing the LLM to use the web browser.
    """

    def __init__(self, url, config_path):

        self.url = url
        self.config = load_config(config_path)
        self.llm = OpenAiWrapper(prompts=self.config['prompts'])

        self.reporter = ConsoleReporter()

        self.visited_pages: List[VisitedPage] = []

        self.wait_between_steps = 0.5

    def run(self, max_steps: int):
        logger.info(f"Test started. Max steps: {max_steps}")
        browser_session = BrowserSession(self.url, headless=True)

        goal = None
        expectation = None

        for step_idx in range(max_steps):

            logger.info(f'[Step {step_idx + 1}] On Page: {browser_session.url}')

            user_prompt = self._get_user_prompt(browser_session)
            system_prompt = self._get_system_prompt()
            screenshot_b64 = browser_session.get_screenshot(path=f"reports/screenshot_{step_idx + 1}.png")

            self._save_report(f"prompt-{step_idx}.txt", user_prompt)

            result = self.llm.run(system_prompt, user_prompt, screenshot_b64)

            goal = result.get('updated_goal') or result.get('goal')
            expectation = result.get('expected_vs_actual')
            logger.info(f'Current goal: {goal}')
            logger.debug(f'Current expectations: {expectation}')

            visited_page = VisitedPage.from_json(browser_session.page, result)
            self.visited_pages.append(visited_page)

            if visited_page.has_next_step():
                visited_page.run_next_step(browser_session)
                ensure_stay_on_domain(browser_session, visited_page)
                logger.info(visited_page.next_step.get_feedback_summary())
            else:
                logger.info("The LLM has decided that there is nothing more to do.")
                break

            time.sleep(self.wait_between_steps)

        browser_session.close()
        logger.info("Test finished.")
        grouped_visits = self._get_grouped_visits()
        self.reporter.print_report(grouped_visits)

    def _get_grouped_visits(self) -> Dict[str, List[VisitedPage]]:
        """
        Groups all visits from the same URL together.
        Ignores anchors.
        :return:
        """
        grouped_visits = defaultdict(list)
        for page in self.visited_pages:
            parts = urlparse(page.page_url)
            normalized = parts._replace(query='', fragment='')
            clean_url = urlunparse(normalized)
            grouped_visits[clean_url].append(page)
        return grouped_visits

    def _generate_llm_context(self) -> str:
        return "\n".join(visited_page.get_llm_visit_summary() for visited_page in self.visited_pages)

    @classmethod
    def _generate_llm_available_actions(cls) -> str:
        """
        Explains to the LLM which actions it can do on the webpage.
        :return:
        """
        return "\n".join(
            action_cls.describe_for_llm() for action_cls in ACTION_REGISTRY.values()
        )

    @classmethod
    def _save_report(cls, name: str, content: str):
        os.makedirs('reports', exist_ok=True)
        with open(f"reports/{name}", "w", encoding="utf-8") as f:
            f.write(content)

    def _get_user_prompt(self, browser_session: BrowserSession) -> str:
        return self.config['prompts']['user'].format(
            page_url=browser_session.url,
            page_html=browser_session.get_optimized_html(),
            console_logs=browser_session.get_console_messages(),
            context=self._generate_llm_context(),
            available_actions=self._generate_llm_available_actions()
        )

    def _get_system_prompt(self) -> str:
        return self.config['prompts']['system']
