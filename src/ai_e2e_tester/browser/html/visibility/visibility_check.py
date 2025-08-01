from abc import ABC, abstractmethod

from playwright.sync_api import ElementHandle, Page, FloatRect


class VisibilityCheck(ABC):
    """
    Base class for all visibility checks.
    A check inspects (el, page, context) and returns (ok: bool, new_context: dict).
    """

    @abstractmethod
    def is_visible(self, el: ElementHandle, box: FloatRect, page: Page) -> bool:
        pass
