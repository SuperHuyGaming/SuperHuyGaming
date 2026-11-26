"""Pure-Python SVG drawing primitives and original cartoon sticker artwork for bentruong.dev."""

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
    defs_block = f"  <defs>\n{defs}  </defs>\n" if defs else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" fill="none" role="img">\n'
        f"{title_tag}"
        f"{defs_block}"
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


def clip_rect_defs(cid: str, x: float, y: float, w: float, h: float, rx: float) -> str:
    return (
        f'    <clipPath id="{cid}">\n'
        f'      <rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx:.1f}"/>\n'
        f"    </clipPath>\n"
    )


def sticker_palette(t: dict[str, str], theme: str) -> dict[str, str]:
    """Map tokens.json colors to cartoon ink, die-cut rim, emerald/gold layers, and shadow."""
    is_dark = theme == "dark"
    return {
        "ink": t["deep"],
        "rim": t["text"] if is_dark else t["paper"],
        "shadow": t["deep"] if is_dark else t["primary_dark"],
        "shadow_op": "0.95" if is_dark else "0.22",
        "em_dark": t["primary_dark"],
        "em": t["primary"],
        "em_mid": t["cell2"],
        "em_light": t["cell1"] if not is_dark else t["primary"],
        "em_soft": t["primary_soft"],
        "gold_dark": t["gold_b"],
        "gold": t["secondary"],
        "gold_light": t["gold_a"],
        "gold_soft": t["secondary_soft"],
        "shine": t["text"] if is_dark else t["paper"],
        "cream": t["text"] if is_dark else t["bg"],
    }


def surface_frame(
    width: int,
    height: int,
    t: dict[str, str],
    theme: str = "light",
    pattern_id: str | None = None,
    glow_id: str | None = None,
    glow2_id: str | None = None,
    radius: int = 14,
    fill_key: str = "bg",
    stroke_key: str = "divider",
    stroke_width: float = 1.5,
    shadow_dx: float = 4.0,
    shadow_dy: float = 4.0,
) -> str:
    """Sticker-depth card frame whose shadow stays strictly inside [0, width] x [0, height]."""
    p = sticker_palette(t, theme)
    cw = width - shadow_dx - 2
    ch = height - shadow_dy - 2
    out = (
        f'  <rect x="{1 + shadow_dx:.1f}" y="{1 + shadow_dy:.1f}" width="{cw:.1f}" height="{ch:.1f}" '
        f'rx="{radius}" fill="{p["shadow"]}" fill-opacity="{p["shadow_op"]}"/>\n'
        f'  <rect x="1" y="1" width="{cw:.1f}" height="{ch:.1f}" '
        f'rx="{radius}" fill="{t[fill_key]}" stroke="{t[stroke_key]}" stroke-width="{stroke_width}"/>\n'
    )
    if pattern_id:
        out += (
            f'  <rect x="1.5" y="1.5" width="{cw - 1:.1f}" height="{ch - 1:.1f}" '
            f'rx="{radius}" fill="url(#{pattern_id})"/>\n'
        )
    if glow_id:
        out += (
            f'  <rect x="1.5" y="1.5" width="{cw - 1:.1f}" height="{ch - 1:.1f}" '
            f'rx="{radius}" fill="url(#{glow_id})"/>\n'
        )
    if glow2_id:
        out += (
            f'  <rect x="1.5" y="1.5" width="{cw - 1:.1f}" height="{ch - 1:.1f}" '
            f'rx="{radius}" fill="url(#{glow2_id})"/>\n'
        )
    return out


def chip(
    x: float,
    y: float,
    text: str,
    t: dict[str, str],
    theme: str = "light",
    font_size: float = 12,
    height: float = 28,
    pad_x: float = 11,
    mono: bool = False,
    accent: str | None = None,
    icon_name: str | None = None,
) -> tuple[str, float]:
    p = sticker_palette(t, theme)
    tw = approx_text_width(text, font_size, mono=mono, bold=True)
    icon_w = 15.0 if icon_name else 0.0
    icon_gap = 6.0 if icon_name else 0.0
    w = round(pad_x * 2 + icon_w + icon_gap + tw)
    font = MONO_FONT if mono else SANS_FONT

    if accent == "primary":
        fill, stroke, tc = t["primary_soft"], t["primary"], t["primary"]
    elif accent == "secondary":
        fill, stroke, tc = t["secondary_soft"], t["secondary"], t["secondary"]
    else:
        fill, stroke, tc = t["paper"], t["divider"], t["text"]

    shadow_op = "0.85" if theme == "dark" else "0.18"
    svg = (
        f'  <rect x="{x + 1.8:.1f}" y="{y + 2.0:.1f}" width="{w}" height="{height}" rx="8" '
        f'fill="{p["shadow"]}" fill-opacity="{shadow_op}"/>\n'
        f'  <rect x="{x:.1f}" y="{y:.1f}" width="{w}" height="{height}" rx="8" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="1.3"/>\n'
    )
    if icon_name:
        svg += mini_chip_icon(icon_name, x + pad_x - 1, y + (height - icon_w) / 2, icon_w, t, theme)
        tx = x + pad_x + icon_w + icon_gap
        anchor = "start"
    else:
        tx = x + w / 2
        anchor = "middle"

    svg += (
        f'  <text x="{tx:.1f}" y="{y + height / 2 + font_size * 0.35:.1f}" '
        f'text-anchor="{anchor}" font-family="{font}" font-size="{font_size}" '
        f'font-weight="600" fill="{tc}">{esc(text)}</text>\n'
    )
    return svg, w


def _sparkle(cx: float, cy: float, r: float, fill: str, stroke: str | None = None) -> str:
    ri = r * 0.32
    pts = (
        f"{cx:.1f},{cy - r:.1f} {cx + ri:.1f},{cy - ri:.1f} "
        f"{cx + r:.1f},{cy:.1f} {cx + ri:.1f},{cy + ri:.1f} "
        f"{cx:.1f},{cy + r:.1f} {cx - ri:.1f},{cy + ri:.1f} "
        f"{cx - r:.1f},{cy:.1f} {cx - ri:.1f},{cy - ri:.1f}"
    )
    st = f' stroke="{stroke}" stroke-width="1.2" stroke-linejoin="round"' if stroke else ""
    return f'    <polygon points="{pts}" fill="{fill}"{st}/>\n'


def mini_chip_icon(name: str, x: float, y: float, size: float, t: dict[str, str], theme: str) -> str:
    """Original 16x16 multi-element cartoon icons for hero focus chips and stats footer pills."""
    p = sticker_palette(t, theme)
    s = size / 16.0
    ink = p["ink"]
    out = f'  <g transform="translate({x:.1f},{y:.1f}) scale({s:.4f})">\n'

    if name == "fullstack":
        out += (
            f'    <rect x="1.5" y="2.5" width="13" height="11" rx="2.5" fill="{p["cream"]}" stroke="{ink}" stroke-width="1.5"/>\n'
            f'    <path d="M1.5 5.5h13" stroke="{ink}" stroke-width="1.4"/>\n'
            f'    <rect x="2.2" y="3.2" width="11.6" height="2" rx="1" fill="{p["em"]}"/>\n'
            f'    <circle cx="4" cy="4.2" r="0.8" fill="{p["gold_light"]}"/>\n'
            f'    <path d="M5.5 8L3.8 9.6 5.5 11.2M10.5 8l1.7 1.6-1.7 1.6M8.7 7.5l-1.4 4.2" stroke="{p["em_dark"] if theme=="light" else p["em"]}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>\n'
        )
    elif name == "agents":
        ant_stroke = p["rim"] if theme == "dark" else ink
        out += (
            f'    <line x1="8" y1="1.5" x2="8" y2="4" stroke="{ant_stroke}" stroke-width="1.6" stroke-linecap="round"/>\n'
            f'    <circle cx="8" cy="1.8" r="1.4" fill="{p["gold_light"]}" stroke="{ink}" stroke-width="1.2"/>\n'
            f'    <rect x="2" y="4" width="12" height="10" rx="3.2" fill="{p["em"]}" stroke="{ant_stroke if theme=="dark" else ink}" stroke-width="1.3"/>\n'
            f'    <rect x="3.8" y="6" width="8.4" height="5" rx="1.8" fill="{ink}"/>\n'
            f'    <circle cx="6.2" cy="8.5" r="1.1" fill="{p["gold_light"]}"/>\n'
            f'    <circle cx="9.8" cy="8.5" r="1.1" fill="{p["gold_light"]}"/>\n'
            f'    <path d="M6.4 12.2h3.2" stroke="{p["gold_light"]}" stroke-width="1.3" stroke-linecap="round"/>\n'
        )
    elif name == "ml":
        line_stroke = p["rim"] if theme == "dark" else ink
        out += (
            f'    <line x1="4" y1="5" x2="12" y2="4" stroke="{line_stroke}" stroke-width="1.6"/>\n'
            f'    <line x1="4" y1="5" x2="9" y2="12" stroke="{line_stroke}" stroke-width="1.6"/>\n'
            f'    <line x1="12" y1="4" x2="9" y2="12" stroke="{line_stroke}" stroke-width="1.6"/>\n'
            f'    <circle cx="4" cy="5" r="2.6" fill="{p["em"]}" stroke="{ink}" stroke-width="1.3"/>\n'
            f'    <circle cx="12" cy="4" r="2.4" fill="{p["gold_light"]}" stroke="{ink}" stroke-width="1.3"/>\n'
            f'    <circle cx="9" cy="12" r="2.5" fill="{p["em_mid"]}" stroke="{ink}" stroke-width="1.3"/>\n'
        )
    elif name == "dl":
        edge_stroke = p["rim"] if theme == "dark" else ink
        out += (
            f'    <polygon points="8,9 14,11.5 8,14 2,11.5" fill="{p["em_mid"] if theme=="dark" else p["em_dark"]}" stroke="{edge_stroke}" stroke-width="1.1" stroke-linejoin="round"/>\n'
            f'    <polygon points="8,5.8 14,8.3 8,10.8 2,8.3" fill="{p["em"]}" stroke="{edge_stroke}" stroke-width="1.1" stroke-linejoin="round"/>\n'
            f'    <polygon points="8,2.5 14,5 8,7.5 2,5" fill="{p["gold_light"]}" stroke="{edge_stroke}" stroke-width="1.1" stroke-linejoin="round"/>\n'
        )
    elif name == "repo":
        out += (
            f'    <path d="M1.5 4.2c0-1 .8-1.7 1.8-1.7h3.2l1.4 1.5h4.8c1 0 1.8.8 1.8 1.8v6.4c0 1-.8 1.8-1.8 1.8H3.3c-1 0-1.8-.8-1.8-1.8V4.2z" fill="{p["em"]}" stroke="{ink}" stroke-width="1.4" stroke-linejoin="round"/>\n'
            f'    <rect x="3.5" y="6.2" width="9" height="5.5" rx="1" fill="{p["gold_light"]}" stroke="{ink}" stroke-width="1.1"/>\n'
        )
    elif name == "star":
        out += (
            f'    <polygon points="8,1.3 10.1,5.5 14.7,6.1 11.3,9.3 12.2,13.9 8,11.7 3.8,13.9 4.7,9.3 1.3,6.1 5.9,5.5" '
            f'fill="{p["gold_light"]}" stroke="{ink}" stroke-width="1.4" stroke-linejoin="round"/>\n'
            f'    <circle cx="6.7" cy="6.4" r="0.9" fill="{p["shine"]}"/>\n'
        )
    elif name == "bolt":
        out += (
            f'    <polygon points="9.2,1.2 3.2,8.8 7.5,8.8 6.4,14.8 12.8,6.8 8.3,6.8" '
            f'fill="{p["gold_light"]}" stroke="{ink}" stroke-width="1.4" stroke-linejoin="round"/>\n'
        )
    elif name == "clock":
        out += (
            f'    <circle cx="8" cy="8" r="6.2" fill="{p["em_soft"]}" stroke="{ink}" stroke-width="1.4"/>\n'
            f'    <circle cx="8" cy="8" r="4.4" fill="{p["gold_light"]}" stroke="{ink}" stroke-width="1.1"/>\n'
            f'    <path d="M8 5v3.2l2.2 1.4" stroke="{ink}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>\n'
        )
    else:
        out += f'    <circle cx="8" cy="8" r="5" fill="{p["em"]}" stroke="{ink}" stroke-width="1.5"/>\n'

    return out + "  </g>\n"


def badge_cartoon_icon(name: str, x: float, y: float, size: float, t: dict[str, str], theme: str, on_primary: bool = False) -> str:
    """Original 24x24 multi-element cartoon sticker icons for link badges."""
    p = sticker_palette(t, theme)
    s = size / 24.0
    ink = p["ink"]
    rim = p["rim"]
    out = f'  <g transform="translate({x:.1f},{y:.1f}) scale({s:.4f})">\n'

    if name == "globe":
        # Glossy emerald/mint globe + brushed-gold orbital ring + sparkles
        ocean = p["em_light"] if on_primary else p["em"]
        land = p["gold_light"] if on_primary else p["em_mid"]
        out += (
            f'    <circle cx="12" cy="12" r="9.5" fill="{rim}"/>\n'
            f'    <circle cx="12" cy="12" r="8.2" fill="{ocean}" stroke="{ink}" stroke-width="1.8"/>\n'
            f'    <path d="M7.5 7.5c1.8-.8 3.6.3 3.2 2-.4 1.5-2.1 2-1.8 3.6.3 1.4 2.1 2.2 1.2 4.2-1.8-.5-3.4-1.8-4.2-3.5-.7-1.6-.4-4.7 1.6-6.3z" fill="{land}" stroke="{ink}" stroke-width="1.2" stroke-linejoin="round"/>\n'
            f'    <path d="M13.5 6.8c2 .7 3.8 2.4 4.2 4.6-1.4.4-2.5-.2-3.2 1-.6 1 .5 2.4-.5 3.6-1.2-1.2-1.8-3-1-4.8.7-1.5-.3-2.9.5-4.4z" fill="{land}" stroke="{ink}" stroke-width="1.2" stroke-linejoin="round"/>\n'
            f'    <ellipse cx="12" cy="12" rx="10.8" ry="3.6" transform="rotate(-22 12 12)" fill="none" stroke="{p["gold_light"]}" stroke-width="2.1"/>\n'
            f'    <ellipse cx="12" cy="12" rx="10.8" ry="3.6" transform="rotate(-22 12 12)" fill="none" stroke="{ink}" stroke-width="0.9" stroke-dasharray="18 20"/>\n'
            f'    <path d="M7.8 6.8a5.6 5.6 0 0 1 4.2-1.4" stroke="{p["shine"]}" stroke-width="1.6" stroke-linecap="round"/>\n'
        )
        out += _sparkle(20.2, 4.5, 2.4, p["gold_light"], ink)
    elif name == "doc":
        # Folded cream scroll/resume + emerald header + brushed-gold wax-star seal
        out += (
            f'    <path d="M5 2.5h9.5l4.5 4.5v14.5H5V2.5z" fill="{rim}" stroke="{rim}" stroke-width="2.2" stroke-linejoin="round"/>\n'
            f'    <path d="M5 2.5h9.5l4.5 4.5v14.5H5V2.5z" fill="{p["cream"]}" stroke="{ink}" stroke-width="1.8" stroke-linejoin="round"/>\n'
            f'    <path d="M14.5 2.5v4.5H19" fill="{p["em_light"]}" stroke="{ink}" stroke-width="1.6" stroke-linejoin="round"/>\n'
            f'    <rect x="7" y="5.5" width="5.5" height="2.4" rx="1" fill="{p["em"]}"/>\n'
            f'    <path d="M7.5 10.5h8.5M7.5 13.5h6.5M7.5 16.5h4.5" stroke="{ink}" stroke-width="1.6" stroke-linecap="round"/>\n'
            f'    <circle cx="16.8" cy="17.2" r="4.1" fill="{p["gold_light"]}" stroke="{ink}" stroke-width="1.5"/>\n'
            f'    <circle cx="16.8" cy="17.2" r="2.2" fill="{p["gold"]}"/>\n'
        )
    elif name == "linkedin":
        # 3D-beveled emerald-and-gold sticker tile + crisp 'in' + spark
        out += (
            f'    <rect x="2.5" y="2.5" width="19" height="19" rx="5" fill="{rim}"/>\n'
            f'    <rect x="4" y="4.5" width="17.5" height="17.5" rx="4.5" fill="{p["gold_dark"]}" stroke="{ink}" stroke-width="1.4"/>\n'
            f'    <rect x="2.8" y="2.8" width="17.5" height="17.5" rx="4.5" fill="{p["em"]}" stroke="{ink}" stroke-width="1.8"/>\n'
            f'    <path d="M5 5.4h4.5" stroke="{p["shine"]}" stroke-width="1.4" stroke-linecap="round"/>\n'
            f'    <circle cx="7.4" cy="8.2" r="1.4" fill="{p["gold_light"]}" stroke="{ink}" stroke-width="0.9"/>\n'
            f'    <path d="M7.4 11.1v5.2" stroke="{p["shine"]}" stroke-width="2.2" stroke-linecap="round"/>\n'
            f'    <path d="M11.2 16.3v-5.2M11.2 13.2c0-1.5 1.1-2.3 2.4-2.3 1.3 0 2.2.9 2.2 2.5v2.9" '
            f'stroke="{p["shine"]}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>\n'
        )
        out += _sparkle(19.8, 4.2, 2.3, p["gold_light"], ink)
    elif name == "mail":
        # Open envelope with gold-tipped letter card popping out + swoosh
        out += (
            f'    <rect x="2.5" y="6.5" width="19" height="14" rx="3" fill="{rim}"/>\n'
            f'    <path d="M5.5 3.5h13v8.5h-13z" fill="{p["gold_light"]}" stroke="{ink}" stroke-width="1.7" stroke-linejoin="round"/>\n'
            f'    <path d="M8 6.5h8M8 9h5" stroke="{ink}" stroke-width="1.4" stroke-linecap="round"/>\n'
            f'    <rect x="2.8" y="8" width="18.4" height="12.5" rx="2.8" fill="{p["cream"]}" stroke="{ink}" stroke-width="1.8"/>\n'
            f'    <path d="M3.2 8.8l8.8 6.4 8.8-6.4" fill="{p["em_soft"]}" stroke="{ink}" stroke-width="1.8" stroke-linejoin="round"/>\n'
            f'    <circle cx="17.8" cy="16.8" r="2.2" fill="{p["em"]}" stroke="{ink}" stroke-width="1.2"/>\n'
        )
    else:
        out += (
            f'    <circle cx="12" cy="12" r="7.5" fill="{p["em"]}" stroke="{ink}" stroke-width="1.9"/>\n'
            f'    <path d="M8 16L16 8M10 8h6v6" stroke="{p["shine"]}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>\n'
        )

    return out + "  </g>\n"


def icon_svg(name: str, x: float, y: float, size: float, color: str) -> str:
    """Compact crisp icon helper (e.g., arrow_ne)."""
    s = size / 24.0
    if name == "arrow_ne":
        return (
            f'  <g transform="translate({x:.1f},{y:.1f}) scale({s:.3f})">\n'
            f'    <path d="M7 17L17 7M9 7h8v8" stroke="{color}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>\n'
            f"  </g>\n"
        )
    return (
        f'  <g transform="translate({x:.1f},{y:.1f}) scale({s:.3f})">\n'
        f'    <circle cx="12" cy="12" r="7" stroke="{color}" stroke-width="2"/>\n'
        f"  </g>\n"
    )


def section_emblem(kind: str, x: float, y: float, size: float, t: dict[str, str], theme: str) -> str:
    """Large 42x42 multi-element cartoon sticker emblems for 01 Activity and 02 Work headers."""
    p = sticker_palette(t, theme)
    s = size / 48.0
    ink = p["ink"]
    rim = p["rim"]
    out = f'  <g transform="translate({x:.1f},{y:.1f}) scale({s:.4f})">\n'

    if kind == "activity":
        # Emerald commit-grid tile + gold lightning bolt + sparkles
        out += (
            f'    <rect x="4" y="7" width="34" height="34" rx="9" fill="{rim}" stroke="{rim}" stroke-width="4"/>\n'
            f'    <rect x="6" y="9" width="34" height="34" rx="8" fill="{p["shadow"]}" fill-opacity="{p["shadow_op"]}"/>\n'
            f'    <rect x="4" y="7" width="34" height="34" rx="8" fill="{p["em_dark"]}" stroke="{ink}" stroke-width="2.3"/>\n'
            f'    <rect x="9.5" y="12.5" width="9.5" height="9.5" rx="2.5" fill="{p["em_mid"]}" stroke="{ink}" stroke-width="1.6"/>\n'
            f'    <rect x="22.5" y="12.5" width="9.5" height="9.5" rx="2.5" fill="{p["em_light"]}" stroke="{ink}" stroke-width="1.6"/>\n'
            f'    <rect x="9.5" y="25.5" width="9.5" height="9.5" rx="2.5" fill="{p["em_light"]}" stroke="{ink}" stroke-width="1.6"/>\n'
            f'    <rect x="22.5" y="25.5" width="9.5" height="9.5" rx="2.5" fill="{p["gold_light"]}" stroke="{ink}" stroke-width="1.6"/>\n'
            f'    <polygon points="33,2 21,22 29.5,22 26,44 43,19 33.5,19" fill="{rim}" stroke="{rim}" stroke-width="3.2" stroke-linejoin="round"/>\n'
            f'    <polygon points="33,2 21,22 29.5,22 26,44 43,19 33.5,19" fill="{p["gold_light"]}" stroke="{ink}" stroke-width="2.2" stroke-linejoin="round"/>\n'
            f'    <path d="M31.5 7.5l-5.5 11" stroke="{p["shine"]}" stroke-width="1.8" stroke-linecap="round"/>\n'
        )
        out += _sparkle(9, 7, 3.6, p["gold_light"], ink)
    else:
        # 02 Work: Gold builder toolbox / craft badge + emerald code card & gear
        out += (
            f'    <rect x="5" y="15" width="38" height="27" rx="7" fill="{rim}" stroke="{rim}" stroke-width="4"/>\n'
            f'    <circle cx="34" cy="14" r="9.5" fill="{rim}"/>\n'
            f'    <circle cx="34" cy="14" r="8" fill="{p["em"]}" stroke="{ink}" stroke-width="2.2"/>\n'
            f'    <circle cx="34" cy="14" r="3" fill="{p["gold_light"]}" stroke="{ink}" stroke-width="1.6"/>\n'
            f'    <rect x="11" y="5" width="18" height="17" rx="3.5" transform="rotate(-10 20 13)" fill="{p["cream"]}" stroke="{ink}" stroke-width="2.1"/>\n'
            f'    <path d="M13 11l3 2.5-3 2.5M18 16h5" stroke="{p["em_dark"] if theme=="light" else p["em"]}" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/>\n'
            f'    <rect x="7" y="18" width="36" height="25" rx="6" fill="{p["shadow"]}" fill-opacity="{p["shadow_op"]}"/>\n'
            f'    <rect x="5" y="16" width="36" height="25" rx="6" fill="{p["gold_light"]}" stroke="{ink}" stroke-width="2.3"/>\n'
            f'    <rect x="5" y="24" width="36" height="17" rx="5" fill="{p["gold"]}" stroke="{ink}" stroke-width="2.2"/>\n'
            f'    <rect x="19" y="21" width="8" height="6.5" rx="2" fill="{p["em"]}" stroke="{ink}" stroke-width="1.8"/>\n'
            f'    <path d="M9 19.5h8" stroke="{p["shine"]}" stroke-width="1.8" stroke-linecap="round"/>\n'
        )
        out += _sparkle(41, 35, 3.3, p["gold_light"], ink)

    return out + "  </g>\n"


def stat_cartoon_icon(kind: str, x: float, y: float, size: float, t: dict[str, str], theme: str) -> str:
    """Large 34-42px multi-element cartoon icons for the 4 GitHub stat sub-cards & heatmap header."""
    p = sticker_palette(t, theme)
    s = size / 44.0
    ink = p["ink"]
    rim = p["rim"]
    out = f'  <g transform="translate({x:.1f},{y:.1f}) scale({s:.4f})">\n'

    if kind == "12m":
        # Commit calendar + sprout
        out += (
            f'    <rect x="4" y="8" width="34" height="31" rx="7" fill="{rim}" stroke="{rim}" stroke-width="3.6"/>\n'
            f'    <rect x="6" y="10" width="34" height="31" rx="7" fill="{p["shadow"]}" fill-opacity="{p["shadow_op"]}"/>\n'
            f'    <rect x="4" y="8" width="34" height="31" rx="7" fill="{p["cream"]}" stroke="{ink}" stroke-width="2.2"/>\n'
            f'    <path d="M4 15c0-3.9 3.1-7 7-7h20c3.9 0 7 3.1 7 7v2H4v-2z" fill="{p["em"]}" stroke="{ink}" stroke-width="2.2"/>\n'
            f'    <rect x="11" y="4" width="4.5" height="7" rx="2.2" fill="{p["gold_light"]}" stroke="{ink}" stroke-width="1.8"/>\n'
            f'    <rect x="26.5" y="4" width="4.5" height="7" rx="2.2" fill="{p["gold_light"]}" stroke="{ink}" stroke-width="1.8"/>\n'
            f'    <rect x="9.5" y="21" width="6.5" height="6.5" rx="1.8" fill="{p["em_light"]}" stroke="{ink}" stroke-width="1.4"/>\n'
            f'    <rect x="18.8" y="21" width="6.5" height="6.5" rx="1.8" fill="{p["em"]}" stroke="{ink}" stroke-width="1.4"/>\n'
            f'    <rect x="28" y="21" width="5.5" height="6.5" rx="1.8" fill="{p["gold_light"]}" stroke="{ink}" stroke-width="1.4"/>\n'
            f'    <rect x="9.5" y="29.5" width="6.5" height="5.5" rx="1.8" fill="{p["em"]}" stroke="{ink}" stroke-width="1.4"/>\n'
            f'    <rect x="18.8" y="29.5" width="6.5" height="5.5" rx="1.8" fill="{p["gold_light"]}" stroke="{ink}" stroke-width="1.4"/>\n'
        )
        out += _sparkle(37, 8, 4.2, p["gold_light"], ink)
    elif kind == "streak":
        # Layered emerald-gold cartoon flame + embers
        out += (
            f'    <path d="M23 3c4 8 13 12 13 22 0 8.5-6.2 14.5-14 14.5S8 33.5 8 25c0-5 2.5-9.5 6-13 .5 3.2 2.2 5 4 5.5C17 11 19 6 23 3z" '
            f'fill="{rim}" stroke="{rim}" stroke-width="4.2" stroke-linejoin="round"/>\n'
            f'    <path d="M23 3c4 8 13 12 13 22 0 8.5-6.2 14.5-14 14.5S8 33.5 8 25c0-5 2.5-9.5 6-13 .5 3.2 2.2 5 4 5.5C17 11 19 6 23 3z" '
            f'fill="{p["gold_light"]}" stroke="{ink}" stroke-width="2.3" stroke-linejoin="round"/>\n'
            f'    <path d="M22.5 14.5c3.5 4.8 7.5 8 7.5 13.5 0 4.8-3.6 8.5-8 8.5s-8-3.7-8-8.5c0-3 1.4-5.5 3.4-7.5.5 2 1.8 3 3 3.2-.2-3.5.6-6.5 2.1-9.2z" '
            f'fill="{p["em"]}" stroke="{ink}" stroke-width="1.9" stroke-linejoin="round"/>\n'
            f'    <ellipse cx="22" cy="30" rx="3.4" ry="4.4" fill="{p["shine"]}"/>\n'
            f'    <circle cx="9" cy="11" r="2.3" fill="{p["gold_light"]}" stroke="{ink}" stroke-width="1.3"/>\n'
            f'    <circle cx="37" cy="13" r="1.9" fill="{p["em_light"]}" stroke="{ink}" stroke-width="1.3"/>\n'
        )
    elif kind == "longest":
        # Chunky 3D-shaded brushed-gold trophy + emerald gem
        out += (
            f'    <path d="M11 7h22v11c0 6.5-4.8 11.5-11 11.5S11 24.5 11 18V7z" fill="{rim}" stroke="{rim}" stroke-width="4.5" stroke-linejoin="round"/>\n'
            f'    <path d="M11 10H6.5c-2 0-3 1.5-3 3.5 0 3.2 2.5 5.8 7.5 6" fill="none" stroke="{ink}" stroke-width="4.2" stroke-linecap="round"/>\n'
            f'    <path d="M11 10H6.5c-2 0-3 1.5-3 3.5 0 3.2 2.5 5.8 7.5 6" fill="none" stroke="{p["gold_light"]}" stroke-width="2.2" stroke-linecap="round"/>\n'
            f'    <path d="M33 10h4.5c2 0 3 1.5 3 3.5 0 3.2-2.5 5.8-7.5 6" fill="none" stroke="{ink}" stroke-width="4.2" stroke-linecap="round"/>\n'
            f'    <path d="M33 10h4.5c2 0 3 1.5 3 3.5 0 3.2-2.5 5.8-7.5 6" fill="none" stroke="{p["gold_light"]}" stroke-width="2.2" stroke-linecap="round"/>\n'
            f'    <rect x="19" y="28" width="6" height="6" fill="{p["gold"]}" stroke="{ink}" stroke-width="2"/>\n'
            f'    <rect x="13" y="34" width="18" height="5.5" rx="2.5" fill="{p["em_dark"]}" stroke="{ink}" stroke-width="2.1"/>\n'
            f'    <path d="M11 7h22v11c0 6.5-4.8 11.5-11 11.5S11 24.5 11 18V7z" fill="{p["gold_light"]}" stroke="{ink}" stroke-width="2.3" stroke-linejoin="round"/>\n'
            f'    <polygon points="22,11.5 26.5,16 22,20.5 17.5,16" fill="{p["em"]}" stroke="{ink}" stroke-width="1.6" stroke-linejoin="round"/>\n'
            f'    <path d="M14.5 10.5v5.5" stroke="{p["shine"]}" stroke-width="1.8" stroke-linecap="round"/>\n'
        )
        out += _sparkle(36, 6, 3.6, p["gold_light"], ink)
    elif kind == "alltime":
        # Rising bar chart + upward arrow + peak gold star
        out += (
            f'    <rect x="5" y="24" width="8.5" height="15" rx="2.5" fill="{rim}" stroke="{rim}" stroke-width="3.2"/>\n'
            f'    <rect x="17" y="17" width="8.5" height="22" rx="2.5" fill="{rim}" stroke="{rim}" stroke-width="3.2"/>\n'
            f'    <rect x="29" y="10" width="8.5" height="29" rx="2.5" fill="{rim}" stroke="{rim}" stroke-width="3.2"/>\n'
            f'    <rect x="5" y="24" width="8.5" height="15" rx="2.5" fill="{p["em_mid"]}" stroke="{ink}" stroke-width="2.1"/>\n'
            f'    <rect x="17" y="17" width="8.5" height="22" rx="2.5" fill="{p["em"]}" stroke="{ink}" stroke-width="2.1"/>\n'
            f'    <rect x="29" y="10" width="8.5" height="29" rx="2.5" fill="{p["gold_light"]}" stroke="{ink}" stroke-width="2.1"/>\n'
            f'    <path d="M7 18L20 9l11-4" fill="none" stroke="{ink}" stroke-width="3.8" stroke-linecap="round" stroke-linejoin="round"/>\n'
            f'    <path d="M7 18L20 9l11-4" fill="none" stroke="{p["gold_light"]}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>\n'
        )
        out += _sparkle(35, 6, 4.6, p["gold_light"], ink)
    else:
        # Heatmap commit-matrix gem
        out += (
            f'    <rect x="5" y="6" width="32" height="32" rx="8" fill="{rim}" stroke="{rim}" stroke-width="3.6"/>\n'
            f'    <rect x="7" y="8" width="32" height="32" rx="7" fill="{p["shadow"]}" fill-opacity="{p["shadow_op"]}"/>\n'
            f'    <rect x="5" y="6" width="32" height="32" rx="7" fill="{p["em_dark"]}" stroke="{ink}" stroke-width="2.2"/>\n'
            f'    <rect x="10" y="11" width="6" height="6" rx="1.6" fill="{p["em_mid"]}"/>\n'
            f'    <rect x="18" y="11" width="6" height="6" rx="1.6" fill="{p["em_light"]}"/>\n'
            f'    <rect x="26" y="11" width="6" height="6" rx="1.6" fill="{p["gold_light"]}"/>\n'
            f'    <rect x="10" y="19" width="6" height="6" rx="1.6" fill="{p["em_light"]}"/>\n'
            f'    <rect x="18" y="19" width="6" height="6" rx="1.6" fill="{p["gold_light"]}"/>\n'
            f'    <rect x="26" y="19" width="6" height="6" rx="1.6" fill="{p["em"]}"/>\n'
            f'    <rect x="10" y="27" width="6" height="6" rx="1.6" fill="{p["em"]}"/>\n'
            f'    <rect x="18" y="27" width="6" height="6" rx="1.6" fill="{p["em_light"]}"/>\n'
            f'    <rect x="26" y="27" width="6" height="6" rx="1.6" fill="{p["em_mid"]}"/>\n'
        )
        out += _sparkle(37, 7, 4.2, p["gold_light"], ink)

    return out + "  </g>\n"


def project_cartoon_icon(proj_id: str, x: float, y: float, size: float, t: dict[str, str], theme: str, stroke_boost: float = 0.0) -> str:
    """Original 96x96 multi-element cartoon sticker illustrations for the 4 featured project cards."""
    p = sticker_palette(t, theme)
    s = size / 96.0
    ink = p["ink"]
    rim = p["rim"]
    sw = 2.5 + stroke_boost
    out = f'  <g transform="translate({x:.1f},{y:.1f}) scale({s:.4f})">\n'

    # Soft tilted die-cut sticker backdrop plate shared across project illustrations
    out += (
        f'    <rect x="10" y="11" width="78" height="78" rx="22" transform="rotate(-4 49 50)" '
        f'fill="{p["shadow"]}" fill-opacity="{p["shadow_op"]}"/>\n'
        f'    <rect x="7" y="8" width="78" height="78" rx="22" transform="rotate(-4 46 47)" '
        f'fill="{t["primary_soft"] if proj_id in ("badminton", "flyer") else t["secondary_soft"]}" '
        f'stroke="{rim}" stroke-width="3.2"/>\n'
    )

    if proj_id == "badminton":
        # Crossed Emerald & Gold Badminton Racket + Chunky Feathered Shuttlecock + swooshes
        out += (
            f'    <g transform="rotate(-32 42 50)">\n'
            f'      <ellipse cx="42" cy="30" rx="19" ry="23" fill="{rim}" stroke="{rim}" stroke-width="4"/>\n'
            f'      <ellipse cx="42" cy="30" rx="17.5" ry="21.5" fill="{p["cream"]}" fill-opacity="0.7" stroke="{ink}" stroke-width="{sw + 2.2}"/>\n'
            f'      <ellipse cx="42" cy="30" rx="17.5" ry="21.5" fill="none" stroke="{p["em"]}" stroke-width="{sw + 0.4}"/>\n'
            f'      <path d="M32 14v32M37 10v40M42 9v42M47 10v40M52 14v32" stroke="{p["gold"]}" stroke-width="1.3"/>\n'
            f'      <path d="M26 22h32M25 28h34M25 34h34M27 40h30" stroke="{p["em_dark"] if theme=="light" else p["em_mid"]}" stroke-width="1.3"/>\n'
            f'      <rect x="39.5" y="51" width="5" height="20" fill="{p["gold_light"]}" stroke="{ink}" stroke-width="2"/>\n'
            f'      <rect x="37.5" y="69" width="9" height="17" rx="3" fill="{p["em_dark"]}" stroke="{ink}" stroke-width="2.2"/>\n'
            f'      <path d="M37.5 74l9 3M37.5 79l9 3" stroke="{p["gold_light"]}" stroke-width="1.8"/>\n'
            f'    </g>\n'
            f'    <g transform="translate(46, 40) rotate(22 20 20)">\n'
            f'      <polygon points="8,4 32,4 25,25 15,25" fill="{rim}" stroke="{rim}" stroke-width="4" stroke-linejoin="round"/>\n'
            f'      <polygon points="8,4 32,4 25,25 15,25" fill="{p["cream"]}" stroke="{ink}" stroke-width="{sw}" stroke-linejoin="round"/>\n'
            f'      <path d="M13 4l4 21M20 4v21M27 4l-4 21" stroke="{p["em"]}" stroke-width="1.6"/>\n'
            f'      <rect x="13.5" y="23" width="13" height="4.5" rx="1.5" fill="{p["em"]}" stroke="{ink}" stroke-width="1.8"/>\n'
            f'      <path d="M14 27.5c0 5.5 2.7 8.5 6 8.5s6-3 6-8.5z" fill="{p["gold_light"]}" stroke="{ink}" stroke-width="{sw}"/>\n'
            f'    </g>\n'
            f'    <path d="M15 22c4-5 10-7 16-6" stroke="{p["gold_light"]}" stroke-width="2.4" stroke-linecap="round"/>\n'
        )
        out += _sparkle(77, 22, 4.8, p["gold_light"], ink)
    elif proj_id == "syllabus":
        # Stacked Emerald & Gold Textbooks + Oversized Glossy Magnifying Glass
        out += (
            f'    <rect x="15" y="52" width="52" height="17" rx="4" fill="{p["em_dark"]}" stroke="{ink}" stroke-width="{sw}"/>\n'
            f'    <rect x="22" y="55.5" width="41" height="10" rx="2" fill="{p["cream"]}" stroke="{ink}" stroke-width="1.5"/>\n'
            f'    <rect x="18" y="34" width="50" height="18" rx="4" fill="{p["gold"]}" stroke="{ink}" stroke-width="{sw}"/>\n'
            f'    <rect x="25" y="37.5" width="39" height="11" rx="2" fill="{p["cream"]}" stroke="{ink}" stroke-width="1.5"/>\n'
            f'    <path d="M29 41h24M29 45h16" stroke="{p["em_dark"]}" stroke-width="1.7" stroke-linecap="round"/>\n'
            f'    <path d="M55 49l19 19" stroke="{rim}" stroke-width="9" stroke-linecap="round"/>\n'
            f'    <path d="M55 49l19 19" stroke="{ink}" stroke-width="7.5" stroke-linecap="round"/>\n'
            f'    <path d="M55 49l19 19" stroke="{p["gold_light"]}" stroke-width="4" stroke-linecap="round"/>\n'
            f'    <circle cx="42" cy="36" r="20" fill="{rim}" stroke="{rim}" stroke-width="3"/>\n'
            f'    <circle cx="42" cy="36" r="17.5" fill="{p["em_soft"]}" stroke="{ink}" stroke-width="{sw + 0.5}"/>\n'
            f'    <circle cx="42" cy="36" r="14" fill="{p["em_light"]}" fill-opacity="0.35" stroke="{p["gold_light"]}" stroke-width="2.4"/>\n'
            f'    <path d="M34 32h15M34 37h11M34 42h8" stroke="{ink}" stroke-width="2" stroke-linecap="round"/>\n'
            f'    <path d="M32 26a11 11 0 0 1 11-3" stroke="{p["shine"]}" stroke-width="2.6" stroke-linecap="round"/>\n'
        )
        out += _sparkle(75, 22, 5.0, p["gold_light"], ink)
    elif proj_id == "flyer":
        # Cartoon AI Vision Lens/Scanner + Tilted Tournament Bracket Flyer Poster
        out += (
            f'    <g transform="rotate(6 56 54)">\n'
            f'      <rect x="30" y="30" width="44" height="50" rx="5" fill="{rim}" stroke="{rim}" stroke-width="3"/>\n'
            f'      <rect x="30" y="30" width="44" height="50" rx="5" fill="{p["cream"]}" stroke="{ink}" stroke-width="{sw}"/>\n'
            f'      <rect x="35" y="35" width="34" height="9" rx="2.5" fill="{p["em"]}" stroke="{ink}" stroke-width="1.5"/>\n'
            f'      <path d="M37 52h10v8h-10M37 68h10v6h-10M47 56h8v15h-8M55 63h9" fill="none" stroke="{ink}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>\n'
            f'      <circle cx="64" cy="63" r="4.5" fill="{p["gold_light"]}" stroke="{ink}" stroke-width="1.5"/>\n'
            f'    </g>\n'
            f'    <polygon points="34,36 74,44 74,53 26,44" fill="{p["em_light"]}" fill-opacity="0.45"/>\n'
            f'    <path d="M24 41l48 8" stroke="{p["em"]}" stroke-width="2.4" stroke-dasharray="4 3" stroke-linecap="round"/>\n'
            f'    <rect x="13" y="16" width="38" height="28" rx="9" fill="{rim}" stroke="{rim}" stroke-width="3"/>\n'
            f'    <rect x="13" y="16" width="38" height="28" rx="9" fill="{p["em_dark"]}" stroke="{ink}" stroke-width="{sw}"/>\n'
            f'    <circle cx="32" cy="30" r="10.5" fill="{p["gold_light"]}" stroke="{ink}" stroke-width="2.1"/>\n'
            f'    <circle cx="32" cy="30" r="5.8" fill="{p["em"]}" stroke="{ink}" stroke-width="1.8"/>\n'
            f'    <circle cx="29.5" cy="27.5" r="2.2" fill="{p["shine"]}"/>\n'
        )
        out += _sparkle(76, 18, 4.6, p["gold_light"], ink)
    else:
        # Hollow Signal: Early-Warning Radar Dish / Mesh Beacon + Concentric Signal Arcs + Mesh Nodes
        out += (
            f'    <path d="M46 32a18 18 0 0 1 18 18" fill="none" stroke="{p["em"]}" stroke-width="3" stroke-linecap="round"/>\n'
            f'    <path d="M46 21a29 29 0 0 1 29 29" fill="none" stroke="{p["gold_light"]}" stroke-width="3" stroke-linecap="round"/>\n'
            f'    <path d="M46 11a39 39 0 0 1 39 39" fill="none" stroke="{p["em_mid"]}" stroke-width="2.4" stroke-dasharray="5 4" stroke-linecap="round"/>\n'
            f'    <path d="M24 78l11-26 11 26" fill="none" stroke="{ink}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>\n'
            f'    <path d="M24 78l11-26 11 26" fill="none" stroke="{p["gold"]}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>\n'
            f'    <path d="M18 35c-5 10-1 23 9 28s23 1 28-9z" fill="{rim}" stroke="{rim}" stroke-width="3.5" stroke-linejoin="round"/>\n'
            f'    <path d="M18 35c-5 10-1 23 9 28s23 1 28-9z" fill="{p["em"]}" stroke="{ink}" stroke-width="{sw}" stroke-linejoin="round"/>\n'
            f'    <line x1="36" y1="45" x2="47" y2="34" stroke="{ink}" stroke-width="3" stroke-linecap="round"/>\n'
            f'    <circle cx="47" cy="34" r="5" fill="{p["gold_light"]}" stroke="{ink}" stroke-width="2"/>\n'
            f'    <line x1="63" y1="22" x2="77" y2="35" stroke="{ink}" stroke-width="1.8" stroke-dasharray="2.5 2.5"/>\n'
            f'    <circle cx="77" cy="35" r="5.5" fill="{p["em_light"]}" stroke="{ink}" stroke-width="1.9"/>\n'
            f'    <polygon points="73,63 81,71 73,79 65,71" fill="{p["gold_light"]}" stroke="{ink}" stroke-width="2" stroke-linejoin="round"/>\n'
            f'    <path d="M73 67.5v4M73 74.2v.6" stroke="{ink}" stroke-width="2" stroke-linecap="round"/>\n'
        )
        out += _sparkle(22, 20, 4.2, p["gold_light"], ink)

    return out + "  </g>\n"


def hero_cartoon_scene(t: dict[str, str], theme: str, phone: bool = False) -> str:
    """Original multi-element cartoon scene for the Hero card (zero BT monogram or replacement initials)."""
    p = sticker_palette(t, theme)
    ink = p["ink"]
    rim = p["rim"]

    if not phone:
        # Open right-side stage on 880x260 desktop hero (x=535..862, y=16..242)
        out = (
            f'  <path d="M564 176 C600 66, 735 38, 818 68" fill="none" stroke="{t["secondary"]}" '
            f'stroke-opacity="0.45" stroke-width="1.8" stroke-dasharray="5 5"/>\n'
            f'  <path d="M582 184 C640 206, 730 165, 796 86" fill="none" stroke="{t["primary"]}" '
            f'stroke-opacity="0.38" stroke-width="1.8" stroke-dasharray="4 5"/>\n'
        )

        # 1) Centerpiece (~140x126 at x=614, y=38): Emerald & Gold Retro-Terminal AI Buddy
        out += (
            f'  <g transform="translate(614,38)">\n'
            f'    <line x1="68" y1="6" x2="68" y2="24" stroke="{ink}" stroke-width="3.6" stroke-linecap="round"/>\n'
            f'    <circle cx="68" cy="7" r="6" fill="{p["gold_light"]}" stroke="{ink}" stroke-width="2.4"/>\n'
            f'    <rect x="14" y="22" width="108" height="84" rx="20" fill="{rim}" stroke="{rim}" stroke-width="5"/>\n'
            f'    <rect x="18" y="26" width="108" height="84" rx="20" fill="{p["shadow"]}" fill-opacity="{p["shadow_op"]}"/>\n'
            f'    <rect x="14" y="22" width="108" height="84" rx="20" fill="{p["em"]}" stroke="{ink}" stroke-width="2.8"/>\n'
            f'    <path d="M26 28h28" stroke="{p["shine"]}" stroke-width="2.4" stroke-linecap="round" opacity="0.7"/>\n'
            f'    <rect x="24" y="33" width="88" height="54" rx="12" fill="{ink}" stroke="{p["gold_light"]}" stroke-width="2.2"/>\n'
            f'    <path d="M44 56c2.5-5 8.5-5 11 0M79 56c2.5-5 8.5-5 11 0" fill="none" stroke="{p["em_light"]}" stroke-width="3.2" stroke-linecap="round"/>\n'
            f'    <path d="M58 66c5 5.5 13 5.5 18 0" fill="none" stroke="{p["gold_light"]}" stroke-width="2.8" stroke-linecap="round"/>\n'
            f'    <circle cx="38" cy="64" r="3.8" fill="{p["gold"]}" fill-opacity="0.7"/>\n'
            f'    <circle cx="96" cy="64" r="3.8" fill="{p["gold"]}" fill-opacity="0.7"/>\n'
            f'    <path d="M32 41l12-4" stroke="{p["shine"]}" stroke-width="2" stroke-linecap="round" opacity="0.5"/>\n'
            f'    <rect x="30" y="94" width="52" height="6" rx="3" fill="{p["em_dark"]}" stroke="{ink}" stroke-width="1.5"/>\n'
            f'    <circle cx="94" cy="97" r="3.4" fill="{p["gold_light"]}" stroke="{ink}" stroke-width="1.4"/>\n'
            f'    <circle cx="105" cy="97" r="3.4" fill="{p["em_light"]}" stroke="{ink}" stroke-width="1.4"/>\n'
            f'    <rect x="26" y="106" width="84" height="12" rx="6" fill="{p["gold_light"]}" stroke="{ink}" stroke-width="2.4"/>\n'
            f'    <rect x="4" y="48" width="10" height="26" rx="5" fill="{p["gold_light"]}" stroke="{ink}" stroke-width="2.2"/>\n'
            f'    <rect x="122" y="48" width="10" height="26" rx="5" fill="{p["gold_light"]}" stroke="{ink}" stroke-width="2.2"/>\n'
            f'  </g>\n'
        )

        # 2) Top-Right (~68x68 at x=770, y=22): Isometric Gold & Emerald Neural Cube
        out += (
            f'  <g transform="translate(770,22)">\n'
            f'    <polygon points="34,6 60,19 60,49 34,62 8,49 8,19" fill="{rim}" stroke="{rim}" stroke-width="4.5" stroke-linejoin="round"/>\n'
            f'    <polygon points="34,6 60,19 34,32 8,19" fill="{p["gold_light"]}" stroke="{ink}" stroke-width="2.3" stroke-linejoin="round"/>\n'
            f'    <polygon points="8,19 34,32 34,62 8,49" fill="{p["em"]}" stroke="{ink}" stroke-width="2.3" stroke-linejoin="round"/>\n'
            f'    <polygon points="60,19 34,32 34,62 60,49" fill="{p["em_dark"]}" stroke="{ink}" stroke-width="2.3" stroke-linejoin="round"/>\n'
            f'    <circle cx="34" cy="19" r="3.2" fill="{p["shine"]}" stroke="{ink}" stroke-width="1.3"/>\n'
            f'    <circle cx="20" cy="40" r="3.2" fill="{p["gold_light"]}" stroke="{ink}" stroke-width="1.3"/>\n'
            f'    <circle cx="48" cy="40" r="3.2" fill="{p["em_light"]}" stroke="{ink}" stroke-width="1.3"/>\n'
            f'  </g>\n'
        )
        out += f'  <g transform="translate(756,14)">\n{_sparkle(6, 6, 4.5, p["gold_light"], ink)}  </g>\n'
        out += f'  <g transform="translate(830,78)">\n{_sparkle(6, 6, 4.0, p["em_light"], ink)}  </g>\n'

        # 3) Bottom-Left of stage (~66x66 at x=538, y=144): Cartoon Rocket-Shuttlecock
        out += (
            f'  <g transform="translate(538,144) rotate(-26 32 32)">\n'
            f'    <polygon points="14,10 50,10 40,38 24,38" fill="{rim}" stroke="{rim}" stroke-width="4" stroke-linejoin="round"/>\n'
            f'    <polygon points="14,10 50,10 40,38 24,38" fill="{p["cream"]}" stroke="{ink}" stroke-width="2.3" stroke-linejoin="round"/>\n'
            f'    <path d="M21 10l6 28M32 10v28M43 10l-6 28" stroke="{p["em"]}" stroke-width="1.8"/>\n'
            f'    <rect x="22" y="36" width="20" height="6" rx="2" fill="{p["em"]}" stroke="{ink}" stroke-width="2"/>\n'
            f'    <path d="M22.5 42c0 8.5 4 13 9.5 13s9.5-4.5 9.5-13z" fill="{p["gold_light"]}" stroke="{ink}" stroke-width="2.3"/>\n'
            f'    <path d="M10 18l-6 4M12 28l-7 2" stroke="{p["gold_light"]}" stroke-width="2.2" stroke-linecap="round"/>\n'
            f'  </g>\n'
        )
        out += f'  <g transform="translate(596,176)">\n{_sparkle(6, 6, 4.2, p["gold_light"], ink)}  </g>\n'
        return out

    # Phone hero cartoon elements:
    # 1) Top-right (x=324, y=22): Compact AI Terminal Buddy (~92x86)
    out = (
        f'  <g transform="translate(326,22) scale(0.68)">\n'
        f'    <line x1="68" y1="6" x2="68" y2="24" stroke="{ink}" stroke-width="4" stroke-linecap="round"/>\n'
        f'    <circle cx="68" cy="7" r="6.5" fill="{p["gold_light"]}" stroke="{ink}" stroke-width="2.6"/>\n'
        f'    <rect x="14" y="22" width="108" height="84" rx="20" fill="{rim}" stroke="{rim}" stroke-width="5.5"/>\n'
        f'    <rect x="18" y="26" width="108" height="84" rx="20" fill="{p["shadow"]}" fill-opacity="{p["shadow_op"]}"/>\n'
        f'    <rect x="14" y="22" width="108" height="84" rx="20" fill="{p["em"]}" stroke="{ink}" stroke-width="3"/>\n'
        f'    <rect x="24" y="33" width="88" height="54" rx="12" fill="{ink}" stroke="{p["gold_light"]}" stroke-width="2.4"/>\n'
        f'    <path d="M44 56c2.5-5 8.5-5 11 0M79 56c2.5-5 8.5-5 11 0" fill="none" stroke="{p["em_light"]}" stroke-width="3.6" stroke-linecap="round"/>\n'
        f'    <path d="M58 66c5 5.5 13 5.5 18 0" fill="none" stroke="{p["gold_light"]}" stroke-width="3" stroke-linecap="round"/>\n'
        f'    <rect x="26" y="106" width="84" height="12" rx="6" fill="{p["gold_light"]}" stroke="{ink}" stroke-width="2.6"/>\n'
        f'    <rect x="4" y="48" width="10" height="26" rx="5" fill="{p["gold_light"]}" stroke="{ink}" stroke-width="2.4"/>\n'
        f'    <rect x="122" y="48" width="10" height="26" rx="5" fill="{p["gold_light"]}" stroke="{ink}" stroke-width="2.4"/>\n'
        f'  </g>\n'
    )
    out += f'  <g transform="translate(314,18)">\n{_sparkle(6, 6, 4.2, p["gold_light"], ink)}  </g>\n'

    # 2) Bottom-right corner of phone hero (x=344, y=266): Isometric Neural Cube + sparkle
    out += (
        f'  <g transform="translate(346,264) scale(0.95)">\n'
        f'    <polygon points="34,6 60,19 60,49 34,62 8,49 8,19" fill="{rim}" stroke="{rim}" stroke-width="4.5" stroke-linejoin="round"/>\n'
        f'    <polygon points="34,6 60,19 34,32 8,19" fill="{p["gold_light"]}" stroke="{ink}" stroke-width="2.3" stroke-linejoin="round"/>\n'
        f'    <polygon points="8,19 34,32 34,62 8,49" fill="{p["em"]}" stroke="{ink}" stroke-width="2.3" stroke-linejoin="round"/>\n'
        f'    <polygon points="60,19 34,32 34,62 60,49" fill="{p["em_dark"]}" stroke="{ink}" stroke-width="2.3" stroke-linejoin="round"/>\n'
        f'    <circle cx="34" cy="19" r="3.2" fill="{p["shine"]}" stroke="{ink}" stroke-width="1.3"/>\n'
        f'    <circle cx="20" cy="40" r="3.2" fill="{p["gold_light"]}" stroke="{ink}" stroke-width="1.3"/>\n'
        f'    <circle cx="48" cy="40" r="3.2" fill="{p["em_light"]}" stroke="{ink}" stroke-width="1.3"/>\n'
        f'  </g>\n'
    )
    return out
