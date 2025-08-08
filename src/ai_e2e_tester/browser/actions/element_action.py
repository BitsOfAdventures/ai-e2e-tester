import logging

from playwright.sync_api import Page, ElementHandle

from ai_e2e_tester.browser.actions.browser_action import BrowserAction
from ai_e2e_tester.browser.actions.element_selector import ElementSelector

logger = logging.getLogger('ai-e2e-tester.browser.actions.element')


class BrowserElementAction(BrowserAction):
    """
    Defines an action on a specific element on the webpage (button, input, etc.)
    """

    def __init__(self, target_text: str):
        self.element_selector = ElementSelector()
        self.target_text = target_text

    def get_element(self, page: Page) -> ElementHandle | None:
        return self.element_selector.get_element(self.target_text, page)

    def __str__(self):
        return f'Browser Action on target "{self.target_text}"'