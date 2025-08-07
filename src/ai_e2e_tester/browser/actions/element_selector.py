import logging

from playwright.sync_api import ElementHandle, Page

logger = logging.getLogger('ai-e2e-tester.browser.selector')


class ElementSelector:
    """
    Helper to return an element from the HTML based on the LLM description.
    """

    def __init__(self):
        self.selector_strategies = [
            lambda t: f'#{t}',  # By id
            lambda t: f'text="{t}"',  # By visible text
            lambda t: f'[placeholder="{t}"]',  # By exact placeholder
            lambda t: f'input[placeholder*="{t.split()[0]}"]',  # Fallback: partial match
            lambda t: f'[data-title="{t}"]',  # Fallback: data-title attribute
            lambda t: f'.{t}',  # Fallback: by class name
        ]

    def get_element(self, target_text: str, page: Page) -> ElementHandle | None:
        """
        Attempts to locate the element to interact with, based on LLM suggestions.
        Uses multiple selector strategies. Logs a warning if multiple elements are found.
        Returns the first matching element, or None.
        @todo The LLM needs to return a more specific element selector if ID is not available.
        @todo If multiple matching elements, prioritize elements most likely to be interactive.
        """

        for make_selector in self.selector_strategies:
            selector = make_selector(target_text)
            try:
                elements = page.query_selector_all(selector)
                if elements:
                    if len(elements) > 1:
                        logger.warning(f"Multiple elements found with selector '{selector}'; using the first one.")
                    return elements[0]
            except Exception as e:
                logger.debug(f"Selector '{selector}' failed: {e}")

        return None
