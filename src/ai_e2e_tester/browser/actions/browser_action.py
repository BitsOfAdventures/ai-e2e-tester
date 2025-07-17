import logging
from abc import ABC

logger = logging.getLogger('ai-e2e-tester.browser.actions')


class BrowserAction(ABC):

    def run(self, page) -> str:
        """
        Runs an action in the browser.
        :param page: Current page in the browser.
        :return: Description of the result of this action, in natural language. Will be given to LLM as feedback.
        """
        pass
