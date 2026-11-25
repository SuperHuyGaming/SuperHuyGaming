"""Pure-Python SVG drawing helpers for tactile sticker-board profile cards."""

from __future__ import annotations

from html import escape
from typing import Any


DISPLAY_FONT = "'Fredoka', 'Segoe UI', ui-rounded, -apple-system, BlinkMacSystemFont, sans-serif"
MONO_FONT = "'DM Mono', ui-monospace, 'Cascadia Code', SFMono-Regular, Menlo, Consolas, monospace"


def esc(text: str) -> str:
    return escape(str(text), quote=True)


def approx_text_width(text: str, font_size: float, mono: bool = False, bold: bool = False) -> float:
    """Estimate rendered width in px so pills/badges hug text cleanly."""
    if mono:
        return len(text) * font_size * 0.61
    wide = sum(1 for c in text if c in "MW@#%&")
    narrow = sum(1 for c in text if c in "ijlI1!|.,:;'` ")
    normal = len(text) - wide - narrow
    factor = 0.59 if bold else 0.55
    return (normal * factor + wide * 0.78 + narrow * 0.30) * font_size


def svg_doc(width: int, height: int, defs: str, body: str, title: str = "") -> str:
    title_tag = f"  <title>{esc(title)}</title>\n" if title else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" fill="none" role="img">\n'
        f"{title_tag}"
        f"  <defs>\n{defs}  </defs>\n"
        f"{body}"
        f"</svg>\n"
    )


def dot_grid_defs(pid: str, dot_color: str, step: int = 24, r: float = 1.35, opacity: float = 0.45) -> str:
    return (
        f'    <pattern id="{pid}" width="{step}" height="{step}" patternUnits="userSpaceOnUse">\n'
        f'      <circle cx="{step / 2:.1f}" cy="{step / 2:.1f}" r="{r}" '
        f'fill="{dot_color}" fill-opacity="{opacity}"/>\n'
        f"    </pattern>\n"
    )


def board_frame(
    width: int,
    height: int,
    t: dict[str, str],
    pattern_id: str,
    radius: int = 18,
    pad: int = 2,
) -> str:
    w = width - pad * 2
    h = height - pad * 2
    return (
        f'  <rect x="{pad}" y="{pad}" width="{w}" height="{h}" rx="{radius}" '
        f'fill="{t["bg"]}" stroke="{t["border"]}" stroke-width="1.5"/>\n'
        f'  <rect x="{pad}" y="{pad}" width="{w}" height="{h}" rx="{radius}" '
        f'fill="url(#{pattern_id})"/>\n'
    )


def sticker_rect(
    x: float,
    y: float,
    w: float,
    h: float,
    fill: str,
    line: str,
    rx: float = 14,
    shadow: float = 4,
    stroke_w: float = 2,
) -> str:
    parts = []
    if shadow > 0:
        parts.append(
            f'  <rect x="{x + shadow:.1f}" y="{y + shadow:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'rx="{rx}" fill="{line}"/>'
        )
    parts.append(
        f'  <rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
        f'rx="{rx}" fill="{fill}" stroke="{line}" stroke-width="{stroke_w}"/>'
    )
    return "\n".join(parts) + "\n"


def pill(
    x: float,
    y: float,
    text: str,
    fill: str,
    text_color: str,
    line: str,
    font_size: float = 13,
    height: float = 28,
    pad_x: float = 12,
    rx: float = 8,
    shadow: float = 2.5,
    mono: bool = False,
    bold: bool = True,
) -> tuple[str, float]:
    tw = approx_text_width(text, font_size, mono=mono, bold=bold)
    w = round(tw + pad_x * 2)
    font = MONO_FONT if mono else DISPLAY_FONT
    weight = "700" if bold else "500"
    svg = sticker_rect(x, y, w, height, fill, line, rx=rx, shadow=shadow, stroke_w=1.5)
    ty = y + height / 2 + font_size * 0.35
    svg += (
        f'  <text x="{x + w / 2:.1f}" y="{ty:.1f}" text-anchor="middle" '
        f'font-family="{font}" font-size="{font_size}" font-weight="{weight}" '
        f'fill="{text_color}">{esc(text)}</text>\n'
    )
    return svg, w


def icon_svg(name: str, x: float, y: float, size: float, color: str, accent: str = "#ff7a59") -> str:
    """Crisp minimal vector icons positioned at (x, y) scaled to size x size."""
    s = size / 24.0
    g_open = f'  <g transform="translate({x:.1f},{y:.1f}) scale({s:.3f})">\n'
    g_close = "  </g>\n"

    if name == "calendar":
        inner = (
            f'    <rect x="3" y="5" width="18" height="16" rx="3" fill="{accent}" stroke="{color}" stroke-width="2.2"/>\n'
            f'    <path d="M3 10h18" stroke="{color}" stroke-width="2.2"/>\n'
            f'    <path d="M8 3v4M16 3v4" stroke="{color}" stroke-width="2.2" stroke-linecap="round"/>\n'
        )
    elif name == "flame":
        inner = (
            f'    <path d="M12 2c2.5 3.5 6 6.2 6 11a6 6 0 1 1-12 0c0-2.4 1.1-4.6 2.5-6.2.3 1.7 1.3 2.7 2.2 2.9C10.5 7 11.1 4.4 12 2z" '
            f'fill="{accent}" stroke="{color}" stroke-width="2.1" stroke-linejoin="round"/>\n'
        )
    elif name == "trophy":
        inner = (
            f'    <path d="M7 4h10v5a5 5 0 0 1-10 0V4z" fill="{accent}" stroke="{color}" stroke-width="2.1"/>\n'
            f'    <path d="M7 6H4v2a3 3 0 0 0 3 3M17 6h3v2a3 3 0 0 1-3 3" stroke="{color}" stroke-width="2.1" stroke-linecap="round"/>\n'
            f'    <path d="M12 14v5M8 20h8" stroke="{color}" stroke-width="2.2" stroke-linecap="round"/>\n'
        )
    elif name == "bars":
        inner = (
            f'    <rect x="4" y="13" width="4" height="7" rx="1" fill="{accent}" stroke="{color}" stroke-width="1.9"/>\n'
            f'    <rect x="10" y="9" width="4" height="11" rx="1" fill="{accent}" stroke="{color}" stroke-width="1.9"/>\n'
            f'    <rect x="16" y="4" width="4" height="16" rx="1" fill="{accent}" stroke="{color}" stroke-width="1.9"/>\n'
        )
    elif name == "folder":
        inner = (
            f'    <path d="M3 7a2 2 0 0 1 2-2h4.5l2 2H19a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V7z" '
            f'fill="{accent}" stroke="{color}" stroke-width="2.1" stroke-linejoin="round"/>\n'
        )
    elif name == "star":
        inner = (
            f'    <path d="M12 2.8l2.9 5.9 6.5.9-4.7 4.6 1.1 6.5L12 17.6 6.2 20.7l1.1-6.5-4.7-4.6 6.5-.9L12 2.8z" '
            f'fill="{accent}" stroke="{color}" stroke-width="2.1" stroke-linejoin="round"/>\n'
        )
    elif name == "bolt":
        inner = (
            f'    <path d="M13 2L4.5 13.5H12L11 22l8.5-11.5H12L13 2z" '
            f'fill="{accent}" stroke="{color}" stroke-width="2.1" stroke-linejoin="round"/>\n'
        )
    elif name == "linkedin":
        inner = (
            f'    <rect x="3" y="3" width="18" height="18" rx="4" stroke="{color}" stroke-width="2.1"/>\n'
            f'    <circle cx="8" cy="8.5" r="1.2" fill="{color}"/>\n'
            f'    <path d="M8 11.5v5.5M12 17v-5.5M12 13.5c0-1.6 1.2-2.2 2.2-2.2 1.2 0 2 .8 2 2.4V17" '
            f'stroke="{color}" stroke-width="2" stroke-linecap="round"/>\n'
        )
    elif name == "globe":
        inner = (
            f'    <circle cx="12" cy="12" r="9" stroke="{color}" stroke-width="2.1"/>\n'
            f'    <ellipse cx="12" cy="12" rx="4" ry="9" stroke="{color}" stroke-width="1.9"/>\n'
            f'    <path d="M3.5 9h17M3.5 15h17" stroke="{color}" stroke-width="1.9"/>\n'
        )
    elif name == "mail":
        inner = (
            f'    <rect x="3" y="5" width="18" height="14" rx="2.5" stroke="{color}" stroke-width="2.1"/>\n'
            f'    <path d="M4 7l8 6 8-6" stroke="{color}" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"/>\n'
        )
    elif name == "github":
        inner = (
            f'    <path d="M12 2.5a9.5 9.5 0 0 0-3 18.5c.48.09.65-.2.65-.45v-1.7c-2.65.58-3.2-1.12-3.2-1.12-.43-1.1-1.06-1.4-1.06-1.4-.86-.59.07-.58.07-.58.95.07 1.46.98 1.46.98.85 1.45 2.22 1.03 2.76.79.09-.62.33-1.03.6-1.27-2.11-.24-4.34-1.06-4.34-4.7 0-1.04.37-1.89.98-2.55-.1-.24-.43-1.22.09-2.54 0 0 .8-.26 2.62.97a9.1 9.1 0 0 1 4.76 0c1.82-1.23 2.62-.97 2.62-.97.52 1.32.19 2.3.1 2.54.61.66.98 1.51.98 2.55 0 3.65-2.23 4.46-4.35 4.7.34.3.65.88.65 1.78v2.64c0 .25.17.55.66.45A9.5 9.5 0 0 0 12 2.5z" '
            f'fill="{color}"/>\n'
        )
    else:
        inner = f'    <circle cx="12" cy="12" r="8" fill="{accent}" stroke="{color}" stroke-width="2"/>\n'

    return g_open + inner + g_close
