import logging

from playwright.sync_api import Page, ElementHandle

logger = logging.getLogger('ai-e2e-tester.browser.html.optimizer')

class HtmlOptimizer:
    """
    Optimizes the HTML to be given to the LLM:
    - Only keeps visible elements (reduces the number of tokens and avoid the LLM clicking on unrechable elements)
    - Removes parts of HTML that are too large (large SVG, style and script tags) to reduce number of tokens.
    """


    def get_optimized_html(self, page:Page) -> str:
        initial_html = page.content()
        initial_size = len(initial_html)

        body = page.query_selector("body")
        visible_html = self._visible_subtree(body) if body else ""

        final_size = len(visible_html)
        reduction = ((initial_size - final_size) / initial_size * 100) if initial_size > 0 else 0
        logger.debug(f"Optimized HTML size: {initial_size} -> {final_size} : Reduced by {reduction:.2f}%")

        return visible_html


    @classmethod
    def _visible_subtree(cls, el: ElementHandle) -> str:
        """
        Recursively build HTML for this element and its visible children,
        without modifying the live DOM.
        """
        # Skip if not visible
        try:
            if not el.is_visible():
                return ""
        except Exception:
            return ""

        # Get tag and attributes
        tag = el.evaluate("el => el.tagName.toLowerCase()")
        attrs = el.evaluate(
            "el => Array.from(el.attributes)"
            ".map(a => `${a.name}=\"${a.value}\"`).join(' ')"
        )
        opening = f"<{tag}{' ' + attrs if attrs else ''}>"

        # Recursively add children
        html_parts = [opening]
        children = el.query_selector_all(":scope > *")
        if children:
            for child in children:
                html_parts.append(cls._visible_subtree(child))
        else:
            # Add text content if leaf
            text = el.evaluate(
                "el => el.childNodes.length === 1 && el.childNodes[0].nodeType === 3 ? el.textContent : ''")
            if text.strip():
                html_parts.append(text)

        html_parts.append(f"</{tag}>")
        return "".join(html_parts)