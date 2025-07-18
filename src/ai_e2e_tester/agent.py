import logging
import time
from collections import defaultdict
from typing import List, Dict

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

    def __init__(self, url, api_key, config_path):

        self.url = url
        self.api_key = api_key
        self.config = load_config(config_path)
        self.prompt_template = self.config['prompts']['main']
        self.llm = OpenAiWrapper(api_key, self.prompt_template)

        self.reporter = ConsoleReporter()

        self.visited_pages: List[VisitedPage] = []

        self.wait_between_steps = 0.5

    def run(self, max_steps: int):
        logger.info(f"Test started. Max steps: {max_steps}")
        browser_session = BrowserSession(self.url, headless=True)
        browser_session.goto_url(self.url)

        for step_idx in range(max_steps):

            # Guard BEFORE LLM
            # @todo Inform LLM that we navigated back after leaving domain.
            if not browser_session.ensure_stay_on_domain():
                break

            logger.info(f'[Step {step_idx + 1}] On Page: {browser_session.url}')

            text = browser_session.get_page_html()
            screenshot_b64 = browser_session.get_screenshot(path=f"reports/screenshot_{step_idx + 1}.png")

            result = self.llm.run(
                page_url=browser_session.url,
                page_html=text,
                screenshot_b64=screenshot_b64,
                context=self._generate_llm_context()
            )

            visited_page = VisitedPage.from_json(browser_session.page, result)
            logger.info(f'{visited_page.summary}')
            self.visited_pages.append(visited_page)

            if visited_page.has_next_step():
                visited_page.run_next_step(browser_session)
            else:
                logger.info("The LLM has decided that there is nothing more to do.")
                break
            time.sleep(self.wait_between_steps)

        browser_session.close()
        logger.info("Test finished.")
        grouped_visits = self._get_grouped_visits()
        self.reporter.print_report(grouped_visits)

    def _get_grouped_visits(self) -> Dict[str, List[VisitedPage]]:
        grouped_visits = defaultdict(list)
        for page in self.visited_pages:
            grouped_visits[page.page_url].append(page)
        return grouped_visits

    def _get_past_visits_for_url(self, url: str) -> List[VisitedPage]:
        return self._get_grouped_visits().get(url)

    @classmethod
    def _generate_llm_visit_summary(cls, visited_page: VisitedPage) -> str:
        return f"""
        You visited the URL {visited_page.page_url}. 
        You found these bugs: {visited_page.bugs} and provided these suggestions: {visited_page.suggestions}. 
        You decided to perform this action: {visited_page.next_step}"""

    def _generate_llm_context(self) -> str:
        return "\nthen\n".join([self._generate_llm_visit_summary(visited_page) for visited_page in self.visited_pages])
