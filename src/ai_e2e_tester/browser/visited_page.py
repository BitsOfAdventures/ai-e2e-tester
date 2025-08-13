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
    summary: str  # Summary of current page
    context: str  # Summary of previous visited pages, actions taken by the agent, and their result
    expectations_vs_reality: str
    feedback: List[Dict[str, str]]
    next_step: NextStep

    def run_next_step(self, browser_session: BrowserSession):
        self.next_step.run(page=browser_session.page)

    def has_next_step(self):
        return self.next_step.browser_action is not None

    def get_llm_condensed_feedback(self):
        return ', '.join([feedback['details'] for feedback in self.feedback])

    def get_llm_visit_summary(self) -> str:
        """
        Returns a combination of visit context (summary of previous actions) and current action.
        :return:
        """
        return '\n'.join(item for item in [self.context, "LAST ACTION:", str(self.get_visit_summary())] if item)

    def get_visit_summary(self) -> Dict:
        return {
            "page_url": self.page_url,
            "observation": self.get_llm_condensed_feedback(),
            "expectations_vs_reality": self.expectations_vs_reality,
            "action_taken": self.next_step.get_llm_step_summary()
        }

    @classmethod
    def from_json(cls, page, result: Dict) -> "VisitedPage":
        return VisitedPage(
            page_url=page.url,
            summary=result.get("summary"),
            context=result.get("context"),
            expectations_vs_reality=result.get("expected_vs_actual"),
            next_step=NextStep.from_json(result.get("next_step")),
            feedback=result.get("feedback", []),
        )
