from playwright.sync_api import ElementHandle, Page

from ai_e2e_tester.browser.html.visibility.visibility_check import VisibilityCheck


class BasicVisibilityCheck(VisibilityCheck):
    def run(self, el: ElementHandle, page: Page, context: dict) -> tuple[bool, dict]:
        try:
            return el.is_visible(), context
        except Exception:
            return False, context
