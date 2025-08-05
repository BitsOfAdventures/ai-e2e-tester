import logging
import re
from typing import List, Dict

from playwright.sync_api import Page, ElementHandle

from ai_e2e_tester.browser.html.visibility.basic_check import BasicVisibilityCheck
from ai_e2e_tester.browser.html.visibility.occlusion_check import OcclusionCheck
from ai_e2e_tester.browser.html.visibility.viewport_check import ViewportIntersectionCheck
from ai_e2e_tester.browser.html.visibility.visibility_check import VisibilityCheck

logger = logging.getLogger('ai-e2e-tester.browser.html.optimizer')


class HtmlOptimizer:
    """
    Optimizes the HTML to be given to the LLM:
    - Only keeps visible elements (reduces the number of tokens and avoid the LLM clicking on unrechable elements)
    - Removes parts of HTML that are too large (large SVG, style and script tags) to reduce number of tokens.
    """

    def __init__(self):
        self.html_cleanup_patterns = [
            r'\s_ngcontent-[^=]+="[^"]*"',  # Angular _ngcontent attributes
            r'\s_nghost-[^=]+="[^"]*"',  # Angular _nghost attributes
            r'\sdata-reactroot(?:="[^"]*")?',  # React root attribute
        ]

        self.visibility_checks: List[VisibilityCheck] = [
            BasicVisibilityCheck(),
            ViewportIntersectionCheck(),
            OcclusionCheck()
        ]

    def get_optimized_html(self, page: Page) -> str:
        initial_html = page.content()
        initial_size = len(initial_html)

        body = page.query_selector("body")
        viewport = page.viewport_size or {"width": float("inf"), "height": float("inf")}
        scroll_x = page.evaluate("() => window.scrollX")
        scroll_y = page.evaluate("() => window.scrollY")

        visible_html = self._visible_subtree(body, viewport, scroll_x, scroll_y) if body else ""

        for cleanup_pattern in self.html_cleanup_patterns:
            visible_html = re.sub(cleanup_pattern, '', visible_html)

        final_size = len(visible_html)
        reduction = ((initial_size - final_size) / initial_size * 100) if initial_size > 0 else 0
        logger.info(f"Optimized HTML size: {initial_size} -> {final_size} : Reduced by {reduction:.2f}%")

        return visible_html

    def _visible_subtree(self, el: ElementHandle, viewport: Dict, scroll_x: float, scroll_y: float) -> str:
        """
        Recursively build HTML for visible elements in the current viewport.
        """
        if not self._is_visible(el, viewport, scroll_x, scroll_y):
            return ""

        tag, attrs = self._get_tag_and_attrs(el)
        opening = f"<{tag}{' ' + attrs if attrs else ''}>"
        html_parts = [opening]

        # Include mixed text nodes
        text_nodes = self._get_text_nodes(el)
        if text_nodes.strip():
            html_parts.append(text_nodes)

        # Recurse for children
        for child in el.query_selector_all(":scope > *"):
            html_parts.append(self._visible_subtree(child, viewport, scroll_x, scroll_y))

        html_parts.append(f"</{tag}>")
        return "".join(html_parts)

    def _is_visible(self, el: ElementHandle, viewport: Dict, scroll_x: float, scroll_y: float) -> bool:
        """Run all registered visibility checks."""
        box = el.bounding_box()

        if not box:
            return False

        return all(check.is_visible(el, box, viewport, scroll_x, scroll_y) for check in self.visibility_checks)

    @classmethod
    def _get_tag_and_attrs(cls, el: ElementHandle) -> tuple[str, str]:
        tag = el.evaluate("el => el.tagName.toLowerCase()")
        attrs = el.evaluate("""
        el => Array.from(el.attributes)
          .map(a => `${a.name}="${a.value}"`)
          .join(' ')
        """)
        return tag, attrs

    @classmethod
    def _get_text_nodes(cls, el: ElementHandle) -> str:
        return el.evaluate("""
        el => Array.from(el.childNodes)
          .filter(n => n.nodeType === 3)
          .map(n => n.textContent)
          .join('')
        """)
