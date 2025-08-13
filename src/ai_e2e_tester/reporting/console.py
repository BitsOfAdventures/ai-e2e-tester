from typing import List, Dict

from rich.console import Console

from ai_e2e_tester.browser.visited_page import VisitedPage


class ConsoleReporter:

    def __init__(self):
        self.console = Console()

    def print_feedback_item(self, item: Dict[str, str]):
        self.console.print(f"[bold cyan]{item['category']}[/] [bold]{item['name']}[/]")
        self.console.print(f"[italic]{item['where']}[/]")
        self.console.print(f"[italic]{item['evidence']}[/]")
        self.console.print(f"{item['details']}\n")

    def print_report(self, grouped_visits: Dict[str, List[VisitedPage]]):
        """
        Prints a summary report of all visited pages.
        """
        for page_url, visited_pages in grouped_visits.items():
            self.console.print(f"\n[underline bold]Page:[/] {page_url}")
            seen = set()
            for visited_page in visited_pages:
                for item in visited_page.feedback:
                    signature = item.get("details")
                    if signature not in seen:
                        seen.add(signature)
                        self.print_feedback_item(item)

            self.console.print("---\n", style="dim")
