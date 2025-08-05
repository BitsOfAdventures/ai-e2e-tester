from typing import Dict

from playwright.sync_api import ElementHandle, FloatRect

from ai_e2e_tester.browser.html.visibility.visibility_check import VisibilityCheck


class ViewportIntersectionCheck(VisibilityCheck):

    def is_visible(self, el: ElementHandle, box: FloatRect, viewport: Dict, scroll_x: float, scroll_y: float) -> bool:
        """Check if element's bounding box intersects with the viewport."""
        x, y, w, h = box["x"], box["y"], box["width"], box["height"]

        # Completely outside on left/right/top/bottom
        if (x + w) <= 0 or (y + h) <= 0:
            return False

        if x >= viewport["width"] or y >= viewport["height"]:
            return False

        return True
