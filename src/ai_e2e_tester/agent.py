import logging
import time
from typing import List

from ai_e2e_tester.browser.session import BrowserSession
from ai_e2e_tester.browser.visited_page import VisitedPage
from ai_e2e_tester.llm.openai import OpenAiWrapper
from ai_e2e_tester.reporting.console import ConsoleReporter
from ai_e2e_tester.utils import load_config

logger = logging.getLogger('ai-e2e-tester.agent')


class TestingAgent:
    """
    @todo Don't repeat feedback when revisiting same page. Pass previous feedback for same page in prompt.
    @todo Make sure the llm only tries to interact with things currently visible on the page.
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
        logger.info("Test started.")
        browser_session = BrowserSession(self.url, headless=True)
        browser_session.goto_url(self.url)

        for step_idx in range(max_steps):

            # Guard BEFORE LLM
            if not browser_session.ensure_stay_on_domain():
                break

            logger.info(f'[{step_idx + 1}] Page: {browser_session.url}')

            text = browser_session.get_page_html()
            screenshot_b64 = browser_session.get_screenshot(path=f"reports/screenshot_{step_idx + 1}.png")

            result = self.llm.run(
                page_html=text,
                screenshot_b64=screenshot_b64,
                prev_steps=[page.next_step for page in self.visited_pages]
            )

            visited_page = VisitedPage.from_json(browser_session.page, result)
            self.visited_pages.append(visited_page)

            if visited_page.has_next_step():
                visited_page.run_next_step(browser_session)
            else:
                logger.info("→ Done! Nothing more to do.")
                break
            time.sleep(self.wait_between_steps)

        browser_session.close()
        logger.info("Test finished.")
        self.reporter.print_report(self.visited_pages)
