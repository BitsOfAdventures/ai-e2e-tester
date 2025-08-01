import logging
from typing import Dict

from ai_e2e_tester.browser.actions import ACTION_REGISTRY
from ai_e2e_tester.browser.actions.action_feedback import ActionFeedback
from ai_e2e_tester.browser.actions.browser_action import BrowserAction

logger = logging.getLogger('ai-e2e-tester.browser.next_step')


class NextStep:
    reason: str
    browser_action: BrowserAction | None = None
    action_feedback: ActionFeedback

    def __init__(self, data: Dict):
        self.reason = data.get('reason')
        self.browser_action = self._get_action(data)

    @classmethod
    def get_state_snapshot(cls, page):
        return {
            "url": page.url,
            "content": page.content()
        }

    @classmethod
    def compare_state(cls, before, after):
        if after["url"] != before["url"]:
            return "Navigated to new URL."
        elif after["content"] != before["content"]:
            return "Page content updated."
        else:
            return "No visible change detected."

    def run(self, page):
        logger.info(f"Reasoning for Next Action: {self.reason}")
        try:
            before = self.get_state_snapshot(page)
            self.action_feedback = self.browser_action.run(page=page)
            after = self.get_state_snapshot(page)
            self.action_feedback.state_change = self.compare_state(before, after)
        except Exception as e:
            logger.error(f'Could not execute browser action {self.browser_action}: {e}')
            self.action_feedback = ActionFeedback(
                is_success=False,
                result=f'Could not execute browser action {self.browser_action}'
            )

    def get_feedback_summary(self) -> str:
        return f"{self.action_feedback.result} → {self.action_feedback.state_change}"

    def update_action_state_change(self, state_change: str):
        self.action_feedback.state_change = state_change

    def get_llm_step_summary(self) -> str:
        if self.browser_action:
            return f"{self.action_feedback.result} → {self.action_feedback.state_change}"
        return "There was no more actions to do."

    @classmethod
    def _get_action(cls, next_step: Dict) -> BrowserAction | None:
        """
        Instantiates the action object.
        :param next_step:
        :return:
        """
        action_type = next_step.get("action")
        action_class = ACTION_REGISTRY.get(action_type)

        if action_type == 'done':
            logger.info("The LLM has decided that there is nothing more to do.")
            return None

        if not action_class:
            logger.warning(f"Unknown action type:{action_type}")
            return None
        return action_class(**{k: v for k, v in next_step.get('params', {}).items()})

    @classmethod
    def from_json(cls, data: Dict):
        """

        :param data: Ex: {"action": "click", "params":{"target_text": "Get Started"}, "reason":"..."}
        :return:
        """
        return NextStep(data=data)
