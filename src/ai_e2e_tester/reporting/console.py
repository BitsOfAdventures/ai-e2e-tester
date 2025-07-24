from typing import List, Dict

from rich.console import Console

from ai_e2e_tester.browser.visited_page import VisitedPage


class ConsoleReporter:

    def __init__(self):
        self.console = Console()

    def print_feedback_item(self, item: Dict[str, str]):
        self.console.print(f"[bold cyan]{item['category']}[/] [bold]{item['name']}[/]")
        self.console.print(f"{item['details']}\n")

    def print_page(self, visited_page: VisitedPage):
        for item in visited_page.feedback:
            self.print_feedback_item(item)

    def print_report(self, grouped_visits: Dict[str, List[VisitedPage]]):
        """
        Prints a summary report of all visited pages.
        """
        for page_url, visited_pages in grouped_visits.items():
            self.console.print(f"\n[underline bold]Page:[/] {page_url}")
            for visited_page in visited_pages:
                self.print_page(visited_page)
            self.console.print("---\n", style="dim")
