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
            for visited_page in visited_pages:
                for bug in visited_page.bugs:
                    print(f'\t- {bug}')

            print('Suggestions:')
            for visited_page in visited_pages:
                for suggestion in visited_page.suggestions:
                    print(f'\t- {suggestion}')

            print('---\n')
