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
        Attempts to locate the element to interact with, based on LLM suggestions.
        Uses multiple selector strategies. Logs a warning if multiple elements are found.
        Returns the first matching element, or None.
        @todo The LLM needs to return a more specific element selector if ID is not available.
        """
        selector_strategies = [
            lambda t: f'#{t}',  # By id
            lambda t: f'text="{t}"',  # By visible text
        ]

        for make_selector in selector_strategies:
            selector = make_selector(self.target_text)
            try:
                elements = page.query_selector_all(selector)
                if elements:
                    if len(elements) > 1:
                        logger.warning(f"Multiple elements found with selector '{selector}'; using the first one.")
                    return elements[0]
            except Exception as e:
                logger.debug(f"Selector '{selector}' failed: {e}")

        return None

