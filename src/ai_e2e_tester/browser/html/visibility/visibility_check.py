from abc import ABC, abstractmethod
from typing import Dict

from playwright.sync_api import ElementHandle, FloatRect


class VisibilityCheck(ABC):
    """
    Base class for all visibility checks.
    A check inspects (el, page, context) and returns (ok: bool, new_context: dict).
    """

    @abstractmethod
    def is_visible(self, el: ElementHandle, box: FloatRect, viewport: Dict, scroll_x: float, scroll_y: float) -> bool:
        """

        :param el: (ElementHandle): The Playwright handle for the element to check.
        :param box: (FloatRect): The element's bounding box, with 'x', 'y', 'width', 'height' as keys.
        :param viewport:
        :param scroll_x: (float): The current horizontal scroll offset of the page (window.scrollX)
        :param scroll_y: (float): The current vertical scroll offset of the page (window.scrollY).

        :return: True if the element is visible and can be interacted with.
        """
        pass
