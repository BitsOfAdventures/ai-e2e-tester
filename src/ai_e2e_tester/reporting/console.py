from collections import defaultdict
from typing import List

from rich.console import Console

from ai_e2e_tester.browser.visited_page import VisitedPage


class ConsoleReporter:

    def __init__(self):
        self.console = Console()

    def print_report(self, all_visited_pages: List[VisitedPage]):
        """
        Prints a summary report of all visited pages.
        """
        grouped_visits = defaultdict(list)
        for page in all_visited_pages:
            grouped_visits[page.page_url].append(page)

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
