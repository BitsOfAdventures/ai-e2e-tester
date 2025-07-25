import logging

from ai_e2e_tester.browser.session import BrowserSession
from ai_e2e_tester.browser.visited_page import VisitedPage

logger = logging.getLogger('ai-e2e-tester.browser.guards.domain')


class DomainGuardException(Exception):
    pass


def ensure_stay_on_domain(session: BrowserSession, page: VisitedPage):
    """
    If AI navigated out of the starting domain, we go back.
    raises Exception if could not return back to original domain.
    """
    main_domain = session.get_start_domain()
    curr_domain = session.get_current_domain()
    if curr_domain != main_domain:
        external_url = session.url
        logger.info(f"External URL: {external_url}). Going back to website.")
        try:
            session.go_back()
            curr_domain = session.get_current_domain()
            if curr_domain != main_domain:
                raise DomainGuardException("Still not on main domain after going back.")
            else:
                page.next_step.update_action_state_change(
                    f"Visited page {external_url} on external domain. It is not part of testing plan. Returned back to previous page.")
        except Exception as e:
            raise DomainGuardException("Error going back in browser history:", e)
