from ai_e2e_tester.browser.actions.back_action import BackAction
from ai_e2e_tester.browser.actions.click_action import ClickAction
from ai_e2e_tester.browser.actions.hover_action import HoverAction
from ai_e2e_tester.browser.actions.scroll_action import ScrollAction
from ai_e2e_tester.browser.actions.type_action import TypeAction
from ai_e2e_tester.browser.actions.wait_action import WaitAction

# List of all actions the LLM can do on the web page.
ACTION_CLASSES = [
    ClickAction,
    TypeAction,
    ScrollAction,
    BackAction,
    WaitAction,
    HoverAction
]

# Build the registry dict automatically from the class .name attribute
ACTION_REGISTRY = {cls.name: cls for cls in ACTION_CLASSES}
