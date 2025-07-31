from abc import ABC
from typing import Dict, List


class AiWrapper(ABC):
    def run(self, page_url: str, page_html: str, screenshot_b64, console_logs: List, context: str,
            available_actions: str) -> Dict:
        pass
