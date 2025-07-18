import logging

from ai_e2e_tester.browser.actions.element_action import BrowserElementAction

logger = logging.getLogger('ai-e2e-tester.browser.actions.type')


class TypeAction(BrowserElementAction):
    name = 'type'

    def __init__(self, target_text: str, value: str = None):
        super().__init__(target_text)
        self.value = value

    def __str__(self):
        return f"Typed {self.value} on input{self.target_text}"

    def run(self, page) -> str:
        el = self.get_element(page)
        logger.info(f'→ Typing in: {self.target_text} value: {self.value}')

        if not el:
            logger.warning(f'Could not type text into {self.target_text}')
            return f'Could not find input for "{self.target_text}"'

        el.type(self.value)
        return f"Typed text {self.value} into {self.target_text}."
