from playwright.sync_api import ElementHandle, Page, FloatRect

from ai_e2e_tester.browser.html.visibility.visibility_check import VisibilityCheck


class BasicVisibilityCheck(VisibilityCheck):
    def is_visible(self, el: ElementHandle, box: FloatRect, page: Page) -> bool:
        try:
            return el.is_visible()
        except Exception:
            return False
