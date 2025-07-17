import logging

from ai_e2e_tester.browser.actions.browser_action import BrowserAction

logger = logging.getLogger('ai-e2e-tester.browser.actions.type')


class TypeAction(BrowserAction):

    def __init__(self, target_text: str, value: str = None):
        self.value = value
        self.target_text = target_text

    def __str__(self):
        return f"Typed {self.value} on input{self.target_text}"

    def run(self, page) -> str:
        logger.info(f'→ Typing in: {self.target_text} value: {self.value}')

        # 1. Try by id
        el = page.query_selector(f'#{self.target_text}')

        # 2. Fallback: placeholder or aria-label
        if not el:
            el = (
                    page.query_selector(f'input[placeholder*="{self.target_text}"]') or
                    page.query_selector(f'input[aria-label*="{self.target_text}"]') or
                    page.query_selector(f'text="{self.target_text}"')
            )

        if not el:
            logger.warning(f'Could not type text into {self.target_text}')
            return f'Could not find input for "{self.target_text}"'

        el.type(self.value)
        return f"Typed text {self.value} into {self.target_text}."

