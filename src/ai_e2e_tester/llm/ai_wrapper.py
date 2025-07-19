from abc import ABC
from typing import Dict


class AiWrapper(ABC):
    def run(self, page_url: str, page_html: str, screenshot_b64, context: str, available_actions: str) -> Dict:
        pass
