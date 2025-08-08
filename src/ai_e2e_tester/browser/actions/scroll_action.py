import logging

from ai_e2e_tester.browser.actions.action_feedback import ActionFeedback
from ai_e2e_tester.browser.actions.browser_action import BrowserAction

logger = logging.getLogger('ai-e2e-tester.browser.actions.scroll')


class ScrollAction(BrowserAction):
    """
    Scrolls on the page.
    @todo Add scroll_amount param for the llm to specify scroll amount and direction.
    """
    name = 'scroll'
    description = 'Scroll down a page.'

    def __init__(self, scroll_amount=2000):
        self.scroll_amount = scroll_amount

    def run(self, page) -> ActionFeedback:
        page.mouse.wheel(0, self.scroll_amount)
        return ActionFeedback(f"Scrolled down the page.")
