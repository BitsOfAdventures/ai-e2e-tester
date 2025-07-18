from ai_e2e_tester.browser.actions.back_action import BackAction
from ai_e2e_tester.browser.actions.click_action import ClickAction
from ai_e2e_tester.browser.actions.scroll_action import ScrollAction
from ai_e2e_tester.browser.actions.type_action import TypeAction
from ai_e2e_tester.browser.actions.wait_action import WaitAction

# @todo Use to auto-generate list available actions in LLM prompt.
AVAILABLE_ACTIONS = [
    ClickAction,
    TypeAction,
    ScrollAction,
    BackAction,
    WaitAction,
]
