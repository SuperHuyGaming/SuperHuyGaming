"""Pure-Python SVG primitives: bentruong.dev editorial layout + chunky flat-shaded cartoon icons (zero AI clichés)."""

from __future__ import annotations

import base64
from html import escape
from pathlib import Path


SANS_FONT = "'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, Arial, sans-serif"
MONO_FONT = "'JetBrains Mono', Consolas, ui-monospace, SFMono-Regular, Menlo, monospace"
MEDIA_DIR = Path(__file__).resolve().parent / "media"


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


def load_data_uri(filename: str) -> str:
    data = (MEDIA_DIR / filename).read_bytes()
    b64 = base64.b64encode(data).decode("ascii")
    return f"data:image/jpeg;base64,{b64}"


def svg_doc(width: int, height: int, defs: str, body: str, title: str = "") -> str:
    title_tag = f"  <title>{esc(title)}</title>\n" if title else ""
    defs_block = f"  <defs>\n{defs}  </defs>\n" if defs else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" fill="none" role="img">\n'
        f"{title_tag}"
        f"{defs_block}"
        f"{body}"
        f"</svg>\n"
    )


def surface_frame(
    width: int,
    height: int,
    t: dict[str, str],
    radius: int = 12,
    fill_key: str = "bg",
) -> str:
    return (
        f'  <rect x="0.75" y="0.75" width="{width - 1.5}" height="{height - 1.5}" '
        f'rx="{radius}" fill="{t[fill_key]}" stroke="{t["divider"]}" stroke-width="1"/>\n'
    )


def chip(
    x: float,
    y: float,
    text: str,
    t: dict[str, str],
    font_size: float = 12,
    height: float = 26,
    pad_x: float = 10,
    mono: bool = False,
    icon_name: str | None = None,
) -> tuple[str, float]:
    tw = approx_text_width(text, font_size, mono=mono, bold=False)
    icon_space = 20 if icon_name else 0
    w = round(tw + pad_x * 2 + icon_space)
    font = MONO_FONT if mono else SANS_FONT

    svg = (
        f'  <rect x="{x:.1f}" y="{y:.1f}" width="{w}" height="{height}" rx="6" '
        f'fill="{t["paper"]}" stroke="{t["divider"]}" stroke-width="1"/>\n'
    )
    if icon_name:
        svg += mini_cartoon_icon(icon_name, x + 7, y + (height - 15) / 2, 15, t)
        tx = x + 26 + tw / 2
    else:
        tx = x + w / 2
    svg += (
        f'  <text x="{tx:.1f}" y="{y + height / 2 + font_size * 0.35:.1f}" '
        f'text-anchor="middle" font-family="{font}" font-size="{font_size}" '
        f'font-weight="500" fill="{t["muted"]}">{esc(text)}</text>\n'
    )
    return svg, w


def _ink(t: dict[str, str]) -> str:
    return "#06120D"


def mini_cartoon_icon(name: str, x: float, y: float, size: float, t: dict[str, str]) -> str:
    """Chunky, flat-shaded editorial cartoon icons for focus chips (zero sparkles/glow)."""
    s = size / 24.0
    ink = _ink(t)
    em = t["primary"]
    gd = t["secondary"]
    cream = "#FAFAF7"
    g_open = f'  <g transform="translate({x:.1f},{y:.1f}) scale({s:.3f})">\n'

    if name == "fullstack":
        inner = (
            f'    <rect x="2" y="4" width="20" height="16" rx="3.5" fill="{cream}" stroke="{ink}" stroke-width="2.2"/>\n'
            f'    <rect x="2" y="4" width="20" height="5.5" rx="2" fill="{em}" stroke="{ink}" stroke-width="2.2"/>\n'
            f'    <path d="M8 14.5l-2.5 1.8L8 18M16 14.5l2.5 1.8L16 18M13 13.5l-2 5" stroke="{ink}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>\n'
        )
    elif name == "agents":
        inner = (
            f'    <path d="M5 17l3-9 4 5 4-5 3 9" fill="none" stroke="{ink}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>\n'
            f'    <circle cx="8" cy="8" r="3.2" fill="{gd}" stroke="{ink}" stroke-width="2"/>\n'
            f'    <circle cx="16" cy="8" r="3.2" fill="{em}" stroke="{ink}" stroke-width="2"/>\n'
            f'    <circle cx="12" cy="17" r="3.2" fill="{cream}" stroke="{ink}" stroke-width="2"/>\n'
        )
    elif name == "ml":
        inner = (
            f'    <rect x="3" y="13" width="5" height="8" rx="1.5" fill="{em}" stroke="{ink}" stroke-width="2"/>\n'
            f'    <rect x="9.5" y="8" width="5" height="13" rx="1.5" fill="{gd}" stroke="{ink}" stroke-width="2"/>\n'
            f'    <rect x="16" y="3" width="5" height="18" rx="1.5" fill="{cream}" stroke="{ink}" stroke-width="2"/>\n'
        )
    else:  # dl / layers
        inner = (
            f'    <polygon points="12,3 22,8.5 12,14 2,8.5" fill="{em}" stroke="{ink}" stroke-width="2" stroke-linejoin="round"/>\n'
            f'    <polyline points="2,13 12,18.5 22,13" fill="none" stroke="{gd}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>\n'
            f'    <polyline points="2,17 12,22 22,17" fill="none" stroke="{cream}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>\n'
        )
    return g_open + inner + "  </g>\n"


def badge_cartoon_icon(name: str, x: float, y: float, size: float, t: dict[str, str], on_primary: bool = False) -> str:
    """Chunky flat-shaded cartoon icons for top action buttons."""
    s = size / 24.0
    ink = _ink(t)
    em = "#06120D" if on_primary else t["primary"]
    gd = t["secondary"]
    cream = "#FAFAF7"
    g_open = f'  <g transform="translate({x:.1f},{y:.1f}) scale({s:.3f})">\n'

    if name == "globe":
        inner = (
            f'    <circle cx="12" cy="12" r="9" fill="{cream if on_primary else em}" stroke="{ink}" stroke-width="2.1"/>\n'
            f'    <ellipse cx="12" cy="12" rx="4.2" ry="9" fill="none" stroke="{ink}" stroke-width="1.9"/>\n'
            f'    <path d="M3.5 9.5h17M3.5 14.5h17" stroke="{ink}" stroke-width="1.9"/>\n'
        )
    elif name == "doc":
        inner = (
            f'    <path d="M5 3h9l5 5v13H5V3z" fill="{cream}" stroke="{ink}" stroke-width="2.1" stroke-linejoin="round"/>\n'
            f'    <path d="M14 3v5h5" fill="{gd}" stroke="{ink}" stroke-width="2" stroke-linejoin="round"/>\n'
            f'    <path d="M8.5 12.5h7M8.5 16h5" stroke="{ink}" stroke-width="2" stroke-linecap="round"/>\n'
        )
    elif name == "linkedin":
        inner = (
            f'    <rect x="3" y="3" width="18" height="18" rx="4" fill="{em}" stroke="{ink}" stroke-width="2.1"/>\n'
            f'    <circle cx="8" cy="8.5" r="1.4" fill="{ink}"/>\n'
            f'    <path d="M8 11.5v5.5M12 17v-5.5M12 13.5c0-1.5 1.2-2.2 2.2-2.2 1.2 0 2 .8 2 2.4V17" '
            f'stroke="{ink}" stroke-width="2.1" stroke-linecap="round"/>\n'
        )
    elif name == "mail":
        inner = (
            f'    <rect x="2.5" y="5" width="19" height="14" rx="3" fill="{gd}" stroke="{ink}" stroke-width="2.1"/>\n'
            f'    <path d="M3.5 6.5l8.5 6.5 8.5-6.5" fill="none" stroke="{ink}" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"/>\n'
        )
    else:
        inner = (
            f'    <path d="M7 17L17 7M9 7h8v8" stroke="{t["muted"]}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>\n'
        )
    return g_open + inner + "  </g>\n"


def snapshot_cartoon_icon(name: str, x: float, y: float, size: float, t: dict[str, str]) -> str:
    """Small chunky flat-shaded cartoon icons for the hero snapshot column (zero sparkles/glow)."""
    s = size / 28.0
    ink = _ink(t)
    em = t["primary"]
    gd = t["secondary"]
    cream = "#FAFAF7"
    g_open = f'  <g transform="translate({x:.1f},{y:.1f}) scale({s:.3f})">\n'

    if name == "grad":
        inner = (
            f'    <polygon points="14,5 26,11 14,17 2,11" fill="{em}" stroke="{ink}" stroke-width="2.2" stroke-linejoin="round"/>\n'
            f'    <path d="M7 14v6c0 2 3.2 3.5 7 3.5s7-1.5 7-3.5v-6" fill="{cream}" stroke="{ink}" stroke-width="2.2" stroke-linejoin="round"/>\n'
            f'    <path d="M24 12v7" stroke="{gd}" stroke-width="2.4" stroke-linecap="round"/>\n'
            f'    <circle cx="24" cy="20" r="2" fill="{gd}" stroke="{ink}" stroke-width="1.5"/>\n'
        )
    elif name == "work":
        inner = (
            f'    <rect x="3" y="8" width="22" height="15" rx="3.5" fill="{gd}" stroke="{ink}" stroke-width="2.2"/>\n'
            f'    <path d="M9.5 8V6a2 2 0 0 1 2-2h5a2 2 0 0 1 2 2v2" fill="none" stroke="{ink}" stroke-width="2.2"/>\n'
            f'    <line x1="3" y1="14.5" x2="25" y2="14.5" stroke="{ink}" stroke-width="2"/>\n'
            f'    <rect x="11.5" y="12.5" width="5" height="4" rx="1" fill="{cream}" stroke="{ink}" stroke-width="1.8"/>\n'
        )
    else:  # shuttlecock
        inner = (
            f'    <g transform="rotate(-28 14 14)">\n'
            f'      <polygon points="8,4 20,4 17.5,17 10.5,17" fill="{cream}" stroke="{ink}" stroke-width="2.1" stroke-linejoin="round"/>\n'
            f'      <line x1="12" y1="4" x2="12.8" y2="17" stroke="{ink}" stroke-width="1.5"/>\n'
            f'      <line x1="16" y1="4" x2="15.2" y2="17" stroke="{ink}" stroke-width="1.5"/>\n'
            f'      <rect x="10" y="16" width="8" height="3.2" rx="1" fill="{gd}" stroke="{ink}" stroke-width="1.9"/>\n'
            f'      <path d="M10.5 19.2h7a3.5 3.5 0 0 1-7 0z" fill="{em}" stroke="{ink}" stroke-width="1.9"/>\n'
            f"    </g>\n"
        )
    return g_open + inner + "  </g>\n"


def stat_cartoon_icon(name: str, x: float, y: float, size: float, t: dict[str, str]) -> str:
    """Bold flat-shaded cartoon icons for the 4 GitHub stat cards (clean ink outline, zero sparkles)."""
    s = size / 36.0
    ink = _ink(t)
    em = t["primary"]
    gd = t["secondary"]
    cream = "#FAFAF7"
    g_open = f'  <g transform="translate({x:.1f},{y:.1f}) scale({s:.3f})">\n'

    if name == "calendar":
        inner = (
            f'    <rect x="4" y="7" width="28" height="24" rx="5" fill="{cream}" stroke="{ink}" stroke-width="2.4"/>\n'
            f'    <path d="M4 13h28V12a5 5 0 0 0-5-5H9a5 5 0 0 0-5 5v1z" fill="{em}" stroke="{ink}" stroke-width="2.4"/>\n'
            f'    <rect x="10" y="3" width="4" height="7" rx="2" fill="{gd}" stroke="{ink}" stroke-width="2"/>\n'
            f'    <rect x="22" y="3" width="4" height="7" rx="2" fill="{gd}" stroke="{ink}" stroke-width="2"/>\n'
            f'    <rect x="9" y="18" width="5" height="4" rx="1" fill="{em}"/>\n'
            f'    <rect x="16" y="18" width="5" height="4" rx="1" fill="{gd}"/>\n'
            f'    <rect x="23" y="18" width="4" height="4" rx="1" fill="{em}"/>\n'
            f'    <rect x="9" y="24" width="5" height="3.5" rx="1" fill="{em}"/>\n'
            f'    <rect x="16" y="24" width="11" height="3.5" rx="1" fill="{ink}" fill-opacity="0.22"/>\n'
        )
    elif name == "flame":
        inner = (
            f'    <path d="M18 3c5 6 11 10.5 11 18.5a11 11 0 1 1-22 0c0-4.2 1.8-8 4.4-10.8.5 2.8 2 4.5 3.6 4.8C15.5 11.5 16.5 7 18 3z" '
            f'fill="{em}" stroke="{ink}" stroke-width="2.4" stroke-linejoin="round"/>\n'
            f'    <path d="M18 15c2.2 2.8 5 5.2 5 9a5 5 0 1 1-10 0c0-2.5 1.2-4.8 5-9z" '
            f'fill="{gd}" stroke="{ink}" stroke-width="2" stroke-linejoin="round"/>\n'
        )
    elif name == "trophy":
        inner = (
            f'    <path d="M10 6h16v9a8 8 0 0 1-16 0V6z" fill="{gd}" stroke="{ink}" stroke-width="2.4" stroke-linejoin="round"/>\n'
            f'    <path d="M10 9H5.5v3a4.5 4.5 0 0 0 4.5 4.5M26 9h4.5v3a4.5 4.5 0 0 1-4.5 4.5" '
            f'fill="none" stroke="{ink}" stroke-width="2.4" stroke-linecap="round"/>\n'
            f'    <rect x="15.5" y="23" width="5" height="5" fill="{gd}" stroke="{ink}" stroke-width="2.2"/>\n'
            f'    <rect x="11" y="27.5" width="14" height="4.5" rx="2" fill="{cream}" stroke="{ink}" stroke-width="2.2"/>\n'
        )
    else:  # bars / rocket chart
        inner = (
            f'    <rect x="5" y="19" width="7" height="12" rx="2" fill="{em}" stroke="{ink}" stroke-width="2.3"/>\n'
            f'    <rect x="14.5" y="12" width="7" height="19" rx="2" fill="{gd}" stroke="{ink}" stroke-width="2.3"/>\n'
            f'    <rect x="24" y="5" width="7" height="26" rx="2" fill="{cream}" stroke="{ink}" stroke-width="2.3"/>\n'
        )
    return g_open + inner + "  </g>\n"


def project_flat_illustration(kind: str, x: float, y: float, size: float, t: dict[str, str]) -> str:
    """Large chunky flat-shaded cartoon illustrations for projects without live screenshots (zero stickers/sparkles)."""
    s = size / 84.0
    ink = _ink(t)
    em = t["primary"]
    gd = t["secondary"]
    cream = "#FAFAF7"
    g_open = f'  <g transform="translate({x:.1f},{y:.1f}) scale({s:.3f})">\n'

    if kind == "flyer":
        # Chunky cartoon camera lens scanning a flyer card
        inner = (
            f'    <rect x="12" y="10" width="44" height="54" rx="7" fill="{cream}" stroke="{ink}" stroke-width="3"/>\n'
            f'    <rect x="20" y="20" width="28" height="10" rx="3" fill="{em}" stroke="{ink}" stroke-width="2.4"/>\n'
            f'    <line x1="20" y1="38" x2="46" y2="38" stroke="{ink}" stroke-width="3" stroke-linecap="round"/>\n'
            f'    <line x1="20" y1="47" x2="38" y2="47" stroke="{ink}" stroke-width="3" stroke-linecap="round"/>\n'
            f'    <rect x="38" y="34" width="38" height="32" rx="8" fill="{gd}" stroke="{ink}" stroke-width="3"/>\n'
            f'    <circle cx="57" cy="50" r="10" fill="{cream}" stroke="{ink}" stroke-width="2.8"/>\n'
            f'    <circle cx="57" cy="50" r="5" fill="{em}" stroke="{ink}" stroke-width="2.4"/>\n'
            f'    <rect x="46" y="29" width="12" height="6" rx="2.5" fill="{em}" stroke="{ink}" stroke-width="2.4"/>\n'
        )
    else:  # hollow / radar dish & underground signal wave
        inner = (
            f'    <path d="M22 68h36" stroke="{ink}" stroke-width="3.5" stroke-linecap="round"/>\n'
            f'    <path d="M40 44L29 68M40 44l11 24" stroke="{ink}" stroke-width="3.2" stroke-linecap="round"/>\n'
            f'    <path d="M20 26a26 26 0 0 0 36 36z" fill="{em}" stroke="{ink}" stroke-width="3" stroke-linejoin="round"/>\n'
            f'    <line x1="38" y1="44" x2="54" y2="28" stroke="{ink}" stroke-width="3.2" stroke-linecap="round"/>\n'
            f'    <circle cx="56" cy="26" r="5.5" fill="{gd}" stroke="{ink}" stroke-width="2.6"/>\n'
            f'    <path d="M54 14a16 16 0 0 1 16 16" fill="none" stroke="{gd}" stroke-width="3.5" stroke-linecap="round"/>\n'
            f'    <path d="M62 8a24 24 0 0 1 16 22" fill="none" stroke="{em}" stroke-width="3.5" stroke-linecap="round"/>\n'
        )
    return g_open + inner + "  </g>\n"
