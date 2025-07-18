import logging

from playwright.sync_api import Page, ElementHandle

from ai_e2e_tester.browser.actions.browser_action import BrowserAction

logger = logging.getLogger('ai-e2e-tester.browser.actions.element')


class BrowserElementAction(BrowserAction):
    """
    Defines an action on a specific element on the webpage (button, input, etc.)
    """

    def __init__(self, target_text: str):
        self.target_text = target_text

    def get_element(self, page: Page) -> ElementHandle | None:
        """
        Attempts to locate the element of the html to interact with based on tips from the LLM
        :return:
        """
        try:
            # 1. Try by id
            el = page.query_selector(f'#{self.target_text}')

            # 2. Trying by element text
            if not el:
                el = page.query_selector(f'text="{self.target_text}"')

            return el
        except Exception as e:
            logger.exception(e)
