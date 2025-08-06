import logging
from typing import Dict

from playwright.sync_api import ElementHandle

from ai_e2e_tester.browser.html.visibility.visibility_check import VisibilityCheck

logger = logging.getLogger('ai-e2e-tester.browser.html.optimizer.occlusion')


class OcclusionCheck(VisibilityCheck):
    """
    Checks if an element is visually unobstructed.
    """

    def is_visible(self, el: ElementHandle, box: dict, viewport: Dict, scroll_x: float, scroll_y: float) -> bool:
        center_x, center_y = self._get_visible_center(box, viewport, scroll_x, scroll_y)

        is_clickable = el.evaluate(
            """
            (el, center) => {
                const [x, y] = center;
                const clientX = x - window.scrollX;
                const clientY = y - window.scrollY;
                const top = document.elementFromPoint(clientX, clientY);
                // Accept exact match or child (contained) match
                return top === el || (top && el.contains(top));
            }
            """,
            [center_x, center_y]
        )

        if not is_clickable:
            logger.info(f'Element did not pass occlusion check: {el}')

        return is_clickable

    @classmethod
    def _get_visible_center(cls, box, viewport: Dict, scroll_x: float, scroll_y: float):
        """
        Returns the center of the intersection between the element's bounding box and the viewport.
        If there is no intersection (element fully offscreen), returns the geometric center of the box.
        """

        # Bounding box in page coordinates
        left = box["x"]
        top = box["y"]
        right = left + box["width"]
        bottom = top + box["height"]

        # Viewport in page coordinates
        vp_left = scroll_x
        vp_top = scroll_y
        vp_right = vp_left + viewport["width"]
        vp_bottom = vp_top + viewport["height"]

        # Intersection rectangle
        vis_left = max(left, vp_left)
        vis_top = max(top, vp_top)
        vis_right = min(right, vp_right)
        vis_bottom = min(bottom, vp_bottom)

        # If no intersection, fallback to geometric center
        if vis_right <= vis_left or vis_bottom <= vis_top:
            return (left + right) / 2, (top + bottom) / 2

        # Center of intersection
        vis_center_x = (vis_left + vis_right) / 2
        vis_center_y = (vis_top + vis_bottom) / 2
        return vis_center_x, vis_center_y
