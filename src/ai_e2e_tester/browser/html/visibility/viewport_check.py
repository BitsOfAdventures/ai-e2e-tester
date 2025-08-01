from typing import Dict

from playwright.sync_api import ElementHandle, Page

from ai_e2e_tester.browser.html.visibility.visibility_check import VisibilityCheck


class ViewportIntersectionCheck(VisibilityCheck):

    def run(self, el: ElementHandle, page: Page, context: dict) -> tuple[bool, dict]:
        box = el.bounding_box()
        if not box:
            return False, context

        viewport = self._get_viewport_size(page)
        if not self._is_intersecting(box, viewport):
            return False, context

        # Update context with useful info
        context = {**context, "box": box}
        return True, context

    @classmethod
    def _get_viewport_size(cls, page: Page) -> Dict:
        """Return viewport size, using infinite fallback if not set."""
        return page.viewport_size or {"width": float("inf"), "height": float("inf")}

    @classmethod
    def _is_intersecting(cls, box: Dict, viewport: Dict) -> bool:
        """Check if element's bounding box intersects with the viewport."""
        x, y, w, h = box["x"], box["y"], box["width"], box["height"]

        # Completely outside on left/right/top/bottom
        if (x + w) <= 0 or (y + h) <= 0:
            return False
        if x >= viewport["width"] or y >= viewport["height"]:
            return False

        return True
