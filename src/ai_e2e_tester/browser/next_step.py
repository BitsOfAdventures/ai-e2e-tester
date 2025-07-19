import logging
from typing import Dict

from ai_e2e_tester.browser.actions import ACTION_REGISTRY
from ai_e2e_tester.browser.actions.browser_action import BrowserAction

logger = logging.getLogger('ai-e2e-tester.browser.next_step')


class NextStep:
    reason: str
    browser_action: BrowserAction | None = None
    action_feedback: str = None

    def __init__(self, reason: str, data: Dict):
        self.reason = reason
        self.browser_action = self._get_action(data)

    def __str__(self):
        if self.browser_action:
            return f"Executed {self.browser_action} with result {self.action_feedback}"
        return "No browser action to run."

    def run(self, page):
        logger.info(f"Reasoning for Next Action: {self.reason}")
        self.action_feedback = self.browser_action.run(page=page)

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
    def from_json(cls, data: Dict, reason: str):
        """

        :param data: Ex: {"action": "click", "target_text": "Get Started"}
        :param reason:
        :return:
        """
        return NextStep(reason=reason, data=data)
