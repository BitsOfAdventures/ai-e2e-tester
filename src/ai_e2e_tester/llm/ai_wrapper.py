from abc import ABC
from typing import Dict


class AiWrapper(ABC):
    def run(self, system_prompt: str, user_prompt: str, screenshot_b64) -> Dict:
        pass
