import logging

from ai_e2e_tester.browser.actions.browser_action import BrowserAction

logger = logging.getLogger('ai-e2e-tester.browser.actions.scroll')


class ScrollAction(BrowserAction):
    name = 'scroll'

    def __init__(self, scroll_amount=2000):
        self.scroll_amount = scroll_amount

    def run(self, page) -> str:
        logger.info("→ Scrolling down")
        page.mouse.wheel(0, self.scroll_amount)
        return "Scrolled down the page."

    def __str__(self):
        return f"Scrolled down the page."
