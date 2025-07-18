from dataclasses import dataclass
from typing import List, Dict

from ai_e2e_tester.browser.next_step import NextStep
from ai_e2e_tester.browser.session import BrowserSession


@dataclass
class VisitedPage:
    """
    Stores information about a page the AI tester visited on the tested website.
    It is used to write reports at the end.
    """
    page_url: str
    summary: str
    suggestions: List[str]
    bugs: List[str]
    next_step: NextStep

    def run_next_step(self, browser_session: BrowserSession):
        self.next_step.run(page=browser_session.page)

    def has_next_step(self):
        return self.next_step.browser_action is not None

    @classmethod
    def from_json(cls, page, result: Dict) -> "VisitedPage":
        return VisitedPage(
            page_url=page.url,
            summary=result.get("summary"),
            next_step=NextStep.from_json(
                result.get("next_step", {"action": "done"}),
                result.get("reason", "")
            ),
            bugs=result.get("bugs", []),
            suggestions=result.get("suggestions", [])
        )
