import logging
import time

from ai_e2e_tester.browser.actions.browser_action import BrowserAction

logger = logging.getLogger('ai-e2e-tester.browser.actions.wait')


class WaitAction(BrowserAction):

    def __init__(self, wait_time_sec: str = "5"):
        self.wait_time_ms = wait_time_sec

    def run(self, page) -> str:
        logger.info(f"→ Waiting {self.wait_time_ms}sec for the page to be ready")
        time.sleep(int(self.wait_time_ms))
        return f"Waited for {self.wait_time_ms}sec."

    def __str__(self):
        return f"Waiting for {self.wait_time_ms}sec."
