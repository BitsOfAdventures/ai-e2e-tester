import logging
from typing import Dict

from playwright.sync_api import ElementHandle, FloatRect

from ai_e2e_tester.browser.html.visibility.visibility_check import VisibilityCheck

logger = logging.getLogger('ai-e2e-tester.browser.html.optimizer.viewport')


class ViewportIntersectionCheck(VisibilityCheck):

    def is_visible(self, el: ElementHandle, box: FloatRect, viewport: Dict, scroll_x: float, scroll_y: float) -> bool:
        """Check if element's bounding box intersects with the viewport."""

        # Element box
        x, y, w, h = box["x"], box["y"], box["width"], box["height"]

        # Viewport
        vp_w, vp_h = viewport["width"], viewport["height"]

        # Return False if the element is completely outside the viewport in any direction
        if (x + w) <= 0 or x >= vp_w or (y + h) <= 0 or y >= vp_h:
            return False

        return True
