from dataclasses import dataclass
from typing import Optional


@dataclass
class ActionFeedback:
    result: str
    is_success: bool = True
    state_change: Optional[str] = ''

    def __str__(self):
        return self.result
