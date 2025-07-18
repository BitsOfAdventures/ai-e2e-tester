from typing import List, Dict

from rich.console import Console

from ai_e2e_tester.browser.visited_page import VisitedPage


class ConsoleReporter:

    def __init__(self):
        self.console = Console()

    def print_report(self, grouped_visits: Dict[str, List[VisitedPage]]):
        """
        Prints a summary report of all visited pages.
        """
        for page_url, visited_pages in grouped_visits.items():
            print(f'Page: {page_url}')
            print('Bugs:')
            [print(f'\t- {bug}') for bug in {bug for vp in visited_pages for bug in vp.bugs}]

            print('Suggestions:')
            [print(f'\t- {sg}') for sg in {sg for vp in visited_pages for sg in vp.suggestions}]

            print('---\n')
