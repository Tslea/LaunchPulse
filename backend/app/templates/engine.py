"""Lightweight template engine for landing page rendering.

Supports:
- {{placeholder}} — simple string replacement (HTML-escaped)
- {{#array}}...{{/array}} — repeated sections for arrays of objects
- {{.}} — current item in a string array
- {{field}} inside a section — field of the current object
- {{comma}} — outputs "," for all items except the last (for JSON-LD)
"""

import html
import re
from pathlib import Path

TEMPLATE_DIR = Path(__file__).parent

# Match section blocks: {{#name}}...{{/name}}
SECTION_RE = re.compile(r"\{\{#(\w+)\}\}(.*?)\{\{/\1\}\}", re.DOTALL)

# Match simple placeholders: {{name}}
PLACEHOLDER_RE = re.compile(r"\{\{(\w+)\}\}")

# Match dot placeholder for string arrays: {{.}}
DOT_RE = re.compile(r"\{\{\.\}\}")

# Match comma placeholder
COMMA_RE = re.compile(r"\{\{comma\}\}")

MAX_OUTPUT_BYTES = 80_000  # safety limit (50KB target, 80KB hard max)


def _escape(value: str) -> str:
    """HTML-escape a string value."""
    return html.escape(str(value), quote=True)


def _render_section(template_block: str, items: list, is_last_fn) -> str:
    """Render a repeated section for an array of items."""
    parts = []
    for i, item in enumerate(items):
        block = template_block
        is_last = i == len(items) - 1

        # Handle {{comma}} — empty for last item, "," for others
        block = COMMA_RE.sub("" if is_last else ",", block)

        if isinstance(item, str):
            # String array — replace {{.}} with the value
            block = DOT_RE.sub(_escape(item), block)
        elif isinstance(item, dict):
            # Object array — replace {{field}} with object fields
            def replace_field(m, obj=item):
                key = m.group(1)
                if key in obj:
                    return _escape(str(obj[key]))
                return m.group(0)  # leave unmatched placeholders as-is

            block = PLACEHOLDER_RE.sub(replace_field, block)
        parts.append(block)
    return "".join(parts)


def render_template(
    template_name: str,
    values: dict,
    config: dict | None = None,
) -> str:
    """Render a landing page template with the given values.

    Args:
        template_name: Template filename (e.g. "landing_v1.html")
        values: Dict of placeholder values (from LandingPageContent.model_dump())
        config: Optional config values (idea_id, api_base_url, tiktok_pixel_id, etc.)

    Returns:
        Rendered HTML string.
    """
    template_path = TEMPLATE_DIR / template_name
    raw = template_path.read_text(encoding="utf-8")

    # Merge config into values
    all_values = {**values}
    if config:
        all_values.update(config)

    # Set defaults for optional config values
    all_values.setdefault("idea_id", "")
    all_values.setdefault("api_base_url", "")
    all_values.setdefault("tiktok_pixel_id", "")
    all_values.setdefault("canonical_url", "")
    all_values.setdefault("og_image", "")

    # Step 1: Render section blocks ({{#name}}...{{/name}})
    def replace_section(m):
        key = m.group(1)
        block = m.group(2)
        items = all_values.get(key, [])
        if not isinstance(items, list):
            return m.group(0)
        return _render_section(block, items, lambda i, n: i == n - 1)

    output = SECTION_RE.sub(replace_section, raw)

    # Step 2: Render simple placeholders ({{name}})
    def replace_placeholder(m):
        key = m.group(1)
        if key in all_values:
            val = all_values[key]
            if isinstance(val, (list, dict)):
                return m.group(0)  # skip complex values
            return _escape(str(val))
        return m.group(0)  # leave unmatched as-is

    output = PLACEHOLDER_RE.sub(replace_placeholder, output)

    if len(output.encode("utf-8")) > MAX_OUTPUT_BYTES:
        raise ValueError(
            f"Rendered template exceeds {MAX_OUTPUT_BYTES} bytes "
            f"({len(output.encode('utf-8'))} bytes)"
        )

    return output
