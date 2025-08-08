import logging

from ai_e2e_tester.browser.actions.action_feedback import ActionFeedback
from ai_e2e_tester.browser.actions.element_action import BrowserElementAction

logger = logging.getLogger('ai-e2e-tester.browser.actions.hover')


class HoverAction(BrowserElementAction):
    name = 'hover'
    description = 'Move the mouse cursor over a button, link, or interactive element (for example, to reveal tooltips or menus).'
    input_fields = {
        "target_text": "Use the element's exact `id` if present; otherwise, use the exact visible text on the element you want to hover over."
    }

    def run(self, page) -> ActionFeedback:
        el = self.get_element(page)
        if not el:
            return ActionFeedback(f'Could not find element to hover: "{self.target_text}"', False)

        el.hover()
        return ActionFeedback(f"Hovered over {self.target_text}")
