from abc import ABC, abstractmethod

from playwright.sync_api import ElementHandle, Page


class VisibilityCheck(ABC):
    """
    Base class for all visibility checks.
    A check inspects (el, page, context) and returns (ok: bool, new_context: dict).
    """
    @abstractmethod
    def run(self, el: ElementHandle, page: Page, context: dict) -> tuple[bool, dict]:
        pass