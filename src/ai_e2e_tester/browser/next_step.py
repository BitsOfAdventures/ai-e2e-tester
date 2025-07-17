import logging
from typing import Dict

from ai_e2e_tester.browser.actions.back_action import BackAction
from ai_e2e_tester.browser.actions.browser_action import BrowserAction
from ai_e2e_tester.browser.actions.click_action import ClickAction
from ai_e2e_tester.browser.actions.scroll_action import ScrollAction
from ai_e2e_tester.browser.actions.type_action import TypeAction

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
        @todo rewrite for better extensibility
        :param next_step:
        :return:
        """
        action_name = next_step['action']
        if action_name == 'click':
            return ClickAction(target_text=next_step["target_text"])
        elif action_name == 'type':
            return TypeAction(target_text=next_step["target_text"], value=next_step["value"])
        elif action_name == 'scroll':
            return ScrollAction()
        elif action_name == 'back':
            return BackAction()
        elif action_name == 'done':
            return None
        else:
            logger.warning(f"Unknown action name:{action_name}")
            return None

    @classmethod
    def from_json(cls, data: Dict, reason: str):
        """

        :param data: Ex: {"action": "click", "target_text": "Get Started"}
        :param reason:
        :return:
        """
        return NextStep(reason=reason, data=data)
