from typing import Dict

from playwright.sync_api import ElementHandle, FloatRect

from ai_e2e_tester.browser.html.visibility.visibility_check import VisibilityCheck


class BasicVisibilityCheck(VisibilityCheck):
    def is_visible(self, el: ElementHandle, box: FloatRect, viewport: Dict, scroll_x: float, scroll_y: float) -> bool:
        try:
            return el.is_visible()
        except Exception:
            return False
