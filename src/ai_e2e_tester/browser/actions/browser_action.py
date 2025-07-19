import logging
from abc import ABC
from typing import Dict

from playwright.sync_api import Page

logger = logging.getLogger('ai-e2e-tester.browser.actions')


class BrowserAction(ABC):
    # Name by which the LLM should call this action.
    name: str = None

    # The description will explain to the LLM when it should use this action.
    description: str = None

    # Describing to the LLM which input fields this action needs and how to format them.
    input_fields: Dict[str, str] = {}

    def run(self, page: Page) -> str:
        """
        Runs an action in the browser.
        :param page: Current page in the browser.
        :return: Description of the result of this action, in natural language. Will be given to LLM as feedback.
        """
        pass

    @classmethod
    def describe_for_llm(cls):
        doc = f'- "{cls.name}": {cls.description}'
        if cls.input_fields:
            doc += " This field has following subfields:\n"
            for k, v in cls.input_fields.items():
                doc += f'    - "{k}": {v}\n'
        return doc
