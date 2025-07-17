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

    def goto_url(self, url):
        self.page.goto(url)
        self.page.wait_for_load_state('load')

    def go_back(self):
        self.page.go_back()
        self.page.wait_for_load_state('load')

    def get_page_text(self):
        return self.page.evaluate("() => document.body.innerText")

    def get_page_html(self):
        return self.page.content()

    def get_screenshot(self, path):
        self.page.screenshot(path=path)
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode('utf-8')

    def close(self):
        self.browser.close()
        self.playwright.stop()

    def ensure_stay_on_domain(self) -> bool:
        """
        If AI navigated out of the starting domain, we go back.
        Returning true if successfully returned back.
        Returning false if could not get back to original domain.
        :return:
        """
        main_domain = self.get_domain(self.start_url)
        curr_domain = self.get_current_domain()
        if curr_domain != main_domain:
            logger.debug(
                f"❗ Left main domain: {curr_domain} (current URL: {self.url}). Trying to go back to previous page in browser history."
            )
            try:
                logger.info('External domain. Going back to website.')
                self.go_back()
                # Check again
                curr_domain = self.get_current_domain()
                if curr_domain != main_domain:
                    # @todo Directly navigate to main domain page
                    logger.error("❗ Still not on main domain after going back. Ending test here.")
                    return False
                else:
                    logger.debug(f"✅ Successfully returned to {self.url}")
                    return True
            except Exception as e:
                logger.error("Error going back in browser history:", e)
                return False
        return True

    @property
    def url(self):
        return self.page.url

    def get_current_domain(self):
        return self.get_domain(self.url)

    @classmethod
    def get_domain(cls, url):
        return urlparse(url).netloc.lower()
