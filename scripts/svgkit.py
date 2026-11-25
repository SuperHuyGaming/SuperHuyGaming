"""Pure-Python SVG drawing primitives matching bentruong.dev's editorial emerald & gold design system."""

from __future__ import annotations

from html import escape


SANS_FONT = "'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, Arial, sans-serif"
MONO_FONT = "'JetBrains Mono', Consolas, ui-monospace, SFMono-Regular, Menlo, monospace"


def esc(text: str) -> str:
    return escape(str(text), quote=True)


def approx_text_width(text: str, font_size: float, mono: bool = False, bold: bool = False) -> float:
    if mono:
        return len(text) * font_size * 0.60
    wide = sum(1 for c in text if c in "MW@#%&")
    narrow = sum(1 for c in text if c in "ijlI1!|.,:;'` ")
    normal = len(text) - wide - narrow
    factor = 0.57 if bold else 0.53
    return (normal * factor + wide * 0.76 + narrow * 0.28) * font_size


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


def dot_field_defs(pid: str, dot_color: str, step: int = 28, r: float = 1.15, opacity: float = 0.45) -> str:
    return (
        f'    <pattern id="{pid}" width="{step}" height="{step}" patternUnits="userSpaceOnUse">\n'
        f'      <circle cx="{step / 2:.1f}" cy="{step / 2:.1f}" r="{r}" '
        f'fill="{dot_color}" fill-opacity="{opacity}"/>\n'
        f"    </pattern>\n"
    )


def gold_grad_defs(gid: str, c1: str, c2: str) -> str:
    return (
        f'    <linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1">\n'
        f'      <stop offset="0%" stop-color="{c1}"/>\n'
        f'      <stop offset="100%" stop-color="{c2}"/>\n'
        f"    </linearGradient>\n"
    )


def radial_glow_defs(gid: str, color: str, cx: str = "82%", cy: str = "24%", r: str = "58%", opacity: float = 0.16) -> str:
    return (
        f'    <radialGradient id="{gid}" cx="{cx}" cy="{cy}" r="{r}">\n'
        f'      <stop offset="0%" stop-color="{color}" stop-opacity="{opacity}"/>\n'
        f'      <stop offset="100%" stop-color="{color}" stop-opacity="0"/>\n'
        f"    </radialGradient>\n"
    )


def surface_frame(
    width: int,
    height: int,
    t: dict[str, str],
    pattern_id: str | None = None,
    glow_id: str | None = None,
    radius: int = 12,
    fill_key: str = "bg",
) -> str:
    out = (
        f'  <rect x="0.75" y="0.75" width="{width - 1.5}" height="{height - 1.5}" '
        f'rx="{radius}" fill="{t[fill_key]}" stroke="{t["divider"]}" stroke-width="1"/>\n'
    )
    if pattern_id:
        out += (
            f'  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" '
            f'rx="{radius}" fill="url(#{pattern_id})"/>\n'
        )
    if glow_id:
        out += (
            f'  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" '
            f'rx="{radius}" fill="url(#{glow_id})"/>\n'
        )
    return out


def chip(
    x: float,
    y: float,
    text: str,
    t: dict[str, str],
    font_size: float = 12,
    height: float = 26,
    pad_x: float = 10,
    mono: bool = False,
    accent: str | None = None,
) -> tuple[str, float]:
    tw = approx_text_width(text, font_size, mono=mono, bold=False)
    w = round(tw + pad_x * 2)
    font = MONO_FONT if mono else SANS_FONT
    if accent == "primary":
        fill, stroke, tc = t["primary_soft"], t["primary"], t["primary"]
    elif accent == "secondary":
        fill, stroke, tc = t["secondary_soft"], t["secondary"], t["secondary"]
    else:
        fill, stroke, tc = t["paper"], t["divider"], t["muted"]

    svg = (
        f'  <rect x="{x:.1f}" y="{y:.1f}" width="{w}" height="{height}" rx="6" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="1"/>\n'
        f'  <text x="{x + w / 2:.1f}" y="{y + height / 2 + font_size * 0.35:.1f}" '
        f'text-anchor="middle" font-family="{font}" font-size="{font_size}" '
        f'font-weight="500" fill="{tc}">{esc(text)}</text>\n'
    )
    return svg, w


def bt_logo_mark(x: float, y: float, size: float, grad_id: str, monogram: str = "BT") -> str:
    """Renders the exact BT gold-bordered mark from bentruong.dev/resume-logo-circle.svg."""
    s = size / 256.0
    return (
        f'  <g transform="translate({x:.1f},{y:.1f}) scale({s:.4f})">\n'
        f'    <rect width="256" height="256" rx="56" fill="#06120D"/>\n'
        f'    <rect x="10" y="10" width="236" height="236" rx="48" fill="none" stroke="url(#{grad_id})" stroke-width="8"/>\n'
        f'    <text x="128" y="138" dominant-baseline="middle" text-anchor="middle" '
        f'font-family="{MONO_FONT}" font-weight="700" font-size="104" fill="url(#{grad_id})">{esc(monogram)}</text>\n'
        f"  </g>\n"
    )


def icon_svg(name: str, x: float, y: float, size: float, color: str) -> str:
    s = size / 24.0
    g_open = f'  <g transform="translate({x:.1f},{y:.1f}) scale({s:.3f})">\n'
    g_close = "  </g>\n"

    if name == "globe":
        inner = (
            f'    <circle cx="12" cy="12" r="9" stroke="{color}" stroke-width="1.9"/>\n'
            f'    <ellipse cx="12" cy="12" rx="4" ry="9" stroke="{color}" stroke-width="1.7"/>\n'
            f'    <path d="M3.5 9h17M3.5 15h17" stroke="{color}" stroke-width="1.7"/>\n'
        )
    elif name == "doc":
        inner = (
            f'    <path d="M6 3h8l4 4v14H6V3z" stroke="{color}" stroke-width="1.9" stroke-linejoin="round"/>\n'
            f'    <path d="M14 3v4h4M9 12h6M9 16h6" stroke="{color}" stroke-width="1.8" stroke-linecap="round"/>\n'
        )
    elif name == "linkedin":
        inner = (
            f'    <rect x="3" y="3" width="18" height="18" rx="3.5" stroke="{color}" stroke-width="1.9"/>\n'
            f'    <circle cx="8" cy="8.5" r="1.2" fill="{color}"/>\n'
            f'    <path d="M8 11.5v5.5M12 17v-5.5M12 13.5c0-1.5 1.2-2.2 2.2-2.2 1.2 0 2 .8 2 2.4V17" '
            f'stroke="{color}" stroke-width="1.9" stroke-linecap="round"/>\n'
        )
    elif name == "mail":
        inner = (
            f'    <rect x="3" y="5" width="18" height="14" rx="2.5" stroke="{color}" stroke-width="1.9"/>\n'
            f'    <path d="M4 7l8 6 8-6" stroke="{color}" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/>\n'
        )
    elif name == "arrow_ne":
        inner = (
            f'    <path d="M7 17L17 7M9 7h8v8" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>\n'
        )
    else:
        inner = f'    <circle cx="12" cy="12" r="7" stroke="{color}" stroke-width="1.9"/>\n'

    return g_open + inner + g_close
