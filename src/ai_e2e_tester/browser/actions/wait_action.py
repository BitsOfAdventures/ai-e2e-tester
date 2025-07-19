import logging
import time

from ai_e2e_tester.browser.actions.browser_action import BrowserAction

logger = logging.getLogger('ai-e2e-tester.browser.actions.wait')


class WaitAction(BrowserAction):
    name = 'wait'
    description = 'Wait until the website has finished loading the data. Use this if you believe the website is not ready yet to be interacted with.'
    input_fields = {
        "wait_time_sec": "How long to wait in seconds."
    }

    def __init__(self, wait_time_sec: str = "5"):
        self.wait_time_ms = wait_time_sec

    def run(self, page) -> str:
        logger.info(f"→ Waiting {self.wait_time_ms}sec for the page to be ready")
        time.sleep(int(self.wait_time_ms))
        return "Success."

    def __str__(self):
        return f"Waiting for {self.wait_time_ms}sec."
