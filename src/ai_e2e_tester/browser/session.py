import base64
import logging
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright

logger = logging.getLogger('ai-e2e-tester.browser')


class BrowserSession:
    """
    Encapsulates a Playwright browser session for automated web testing.

    This class manages browser startup/shutdown, page navigation, page text/screenshot extraction,
    and simple navigation actions, making it easier to interact with a browser in a reusable way.
    """

    def __init__(self, start_url: str, headless=True):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=headless)
        self.page = self.browser.new_page()
        self.start_url = start_url

        if self.start_url:
            self.goto_url(self.start_url)

    def goto_url(self, url):
        self.page.goto(url)
        self.page.wait_for_load_state('load')

    def go_back(self):
        self.page.go_back()
        self.page.wait_for_load_state('load')

    def get_page_text(self) -> str:
        return self.page.evaluate("() => document.body.innerText")

    def get_page_html(self) -> str:
        return self.page.content()

    def get_screenshot(self, path):
        self.page.screenshot(path=path)
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode('utf-8')

    def close(self):
        self.browser.close()
        self.playwright.stop()

    @property
    def url(self):
        return self.page.url

    def get_current_domain(self):
        return self.get_domain(self.url)

    def get_start_domain(self):
        return self.get_domain(self.start_url)

    @classmethod
    def get_domain(cls, url):
        return urlparse(url).netloc.lower()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
