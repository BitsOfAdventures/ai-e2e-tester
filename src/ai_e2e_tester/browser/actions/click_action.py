import logging

from playwright.sync_api import Page, ElementHandle

from ai_e2e_tester.browser.actions.action_feedback import ActionFeedback
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

    def run(self, page: Page) -> ActionFeedback:
        el = self.get_element(page)

        if not el:
            return ActionFeedback(f'Could not click. Could not find element with text "{self.target_text}"', False)

        self._force_same_tab_open(page, el)

        el.click()
        page.wait_for_load_state('load')
        return ActionFeedback(f'Clicked on "{self.target_text}"')

    @classmethod
    def _force_same_tab_open(cls, page: Page, el: ElementHandle):
        page.evaluate("""
            el => { if (el.tagName && el.tagName.toLowerCase() === 'a') el.removeAttribute('target'); }
        """, el)
