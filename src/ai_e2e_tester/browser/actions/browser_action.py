import logging
from abc import ABC
from typing import Dict

from playwright.sync_api import Page

from ai_e2e_tester.browser.actions.action_feedback import ActionFeedback

logger = logging.getLogger('ai-e2e-tester.browser.actions')


class BrowserAction(ABC):
    # Name by which the LLM should call this action.
    name: str = None

    # The description will explain to the LLM when it should use this action.
    description: str = None

    # Describing to the LLM which input fields this action needs and how to format them.
    input_fields: Dict[str, str] = {}

    def run(self, page: Page) -> ActionFeedback:
        """
        Runs an action in the browser.
        :param page: Current page in the browser.
        :return: Description of the result of this action, in natural language. Will be given to LLM as feedback.
        """
        pass

    @classmethod
    def describe_for_llm(cls):
        """
        Returns a string describing the action and its 'params' fields for the LLM.
            Example output:

            - "click": Click on a button or clickable element.
              params:
                - "target_text": The element's id or visible text.
        """
        doc = f'- "{cls.name}": {cls.description}\n'
        if cls.input_fields:
            doc += "  params:\n"
            for k, desc in cls.input_fields.items():
                doc += f'    - "{k}": {desc}\n'
        return doc

    def __str__(self):
        return 'Browser Action'
