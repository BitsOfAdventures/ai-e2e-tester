from abc import ABC
from typing import List, Dict

from ai_e2e_tester.browser.next_step import NextStep


class AiWrapper(ABC):
    def run(self, page_html: str, screenshot_b64, prev_steps: List[NextStep]) -> Dict:
        pass
