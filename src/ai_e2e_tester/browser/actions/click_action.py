import logging

from playwright.sync_api import Page, ElementHandle

from ai_e2e_tester.browser.actions.element_action import BrowserElementAction

logger = logging.getLogger('ai-e2e-tester.browser.actions.click')


class ClickAction(BrowserElementAction):
    """
    Click on buttons and links.
    """
    name = 'click'
    description = 'Click on a button or clickable element.'
    input_fields = {
        "target_text": "Use the clickable element's exact `id` value if it has one. If there is no `id`, use exact visible text shown on the button, link, or element you want to interact with."
    }

    def __init__(self, target_text: str):
        super().__init__(target_text)

    def run(self, page: Page) -> str:
        el = self.get_element(page)

        if not el:
            logger.warning(f'Could not click on {self.target_text}')
            return f'Could not find element with text "{self.target_text}"'

        self._force_same_tab_open(page, el)

        logger.info(f"Clicking on {self.target_text}")
        el.click()
        page.wait_for_load_state('load')
        return f"Clicked on {self.target_text}"

    @classmethod
    def _force_same_tab_open(cls, page: Page, el: ElementHandle):
        page.evaluate("""
            el => { if (el.tagName && el.tagName.toLowerCase() === 'a') el.removeAttribute('target'); }
        """, el)
