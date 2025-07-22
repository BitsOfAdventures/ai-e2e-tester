import logging

from ai_e2e_tester.browser.actions.browser_action import BrowserAction

logger = logging.getLogger('ai-e2e-tester.browser.actions.back')


class BackAction(BrowserAction):
    name = 'back'
    description = 'Navigate back to the previous page.'

    def run(self, page) -> str:
        page.go_back()
        page.wait_for_load_state('load')
        return f"Navigated back to previous page."
