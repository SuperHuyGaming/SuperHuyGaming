"""Render all dark/light and desktop/phone SVG cards in bentruong.dev's Emerald & Gold sticker system."""

from __future__ import annotations

import datetime as dt
from typing import Any

from svgkit import (
    MONO_FONT,
    SANS_FONT,
    approx_text_width,
    badge_cartoon_icon,
    chip,
    dot_field_defs,
    esc,
    gold_grad_defs,
    hero_cartoon_scene,
    icon_svg,
    mini_chip_icon,
    project_cartoon_icon,
    radial_glow_defs,
    section_emblem,
    stat_cartoon_icon,
    sticker_palette,
    surface_frame,
    svg_doc,
)


MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

TAG_ICONS = {
    "Full-Stack Apps": "fullstack",
    "AI Agents": "agents",
    "Machine Learning": "ml",
    "Deep Learning": "dl",
}


def _fmt_num(n: int) -> str:
    return f"{n:,}"


def _fmt_date(iso_date: str | None) -> str:
    if not iso_date:
        return "today"
    d = dt.date.fromisoformat(iso_date)
    return f"{d.day} {MONTH_NAMES[d.month - 1]} {d.year}"


def _fmt_short_date(iso_date: str | None) -> str:
    if not iso_date:
        return "starting today"
    d = dt.date.fromisoformat(iso_date)
    return f"since {d.day} {MONTH_NAMES[d.month - 1]}"


def _wrap_text(text: str, max_chars: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur = ""
    for w in words:
        cand = f"{cur} {w}".strip()
        if len(cand) <= max_chars or not cur:
            cur = cand
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def _sticker_pill(
    x: float,
    y: float,
    text: str,
    t: dict[str, str],
    theme: str,
    icon_name: str | None = None,
    font_size: float = 11.5,
    height: float = 28,
    pad_x: float = 11,
    mono: bool = True,
    accent: str | None = None,
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
        fill, stroke, tc = t["paper"], t["divider"], t["muted"]

    shadow_op = "0.85" if theme == "dark" else "0.16"
    svg = (
        f'  <rect x="{x + 1.8:.1f}" y="{y + 2.0:.1f}" width="{w}" height="{height}" rx="9" '
        f'fill="{p["shadow"]}" fill-opacity="{shadow_op}"/>\n'
        f'  <rect x="{x:.1f}" y="{y:.1f}" width="{w}" height="{height}" rx="9" '
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


def render_hero(profile: dict[str, Any], t: dict[str, str], theme: str, phone: bool = False) -> str:
    vp = "p" if phone else "d"
    pid = f"hero-dots-{theme}-{vp}"
    gid1 = f"hero-glow-em-{theme}-{vp}"
    gid2 = f"hero-glow-gd-{theme}-{vp}"
    gold_id = f"hero-gold-{theme}-{vp}"
    defs = (
        dot_field_defs(pid, t["dot"], step=24, r=1.2, opacity=0.50 if theme == "dark" else 0.40)
        + radial_glow_defs(gid1, t["primary"], cx="82%", cy="26%", r="52%", opacity=0.18 if theme == "dark" else 0.10)
        + radial_glow_defs(gid2, t["secondary"], cx="70%", cy="82%", r="44%", opacity=0.14 if theme == "dark" else 0.08)
        + gold_grad_defs(gold_id, t["gold_a"], t["gold_b"])
    )
    p = sticker_palette(t, theme)

    if not phone:
        W, H = 880, 260
        body = surface_frame(
            W, H, t, theme=theme, pattern_id=pid, glow_id=gid1, glow2_id=gid2, radius=16, fill_key="bg"
        )

        # Left segmented emerald & gold accent bar
        body += f'  <rect x="1.5" y="24" width="4" height="{H - 86}" rx="2" fill="{t["primary"]}"/>\n'
        body += f'  <rect x="1.5" y="{H - 56}" width="4" height="28" rx="2" fill="url(#{gold_id})"/>\n'

        # Top live status pill
        status_text = "BENTRUONG.DEV · GEORGE MASON CS"
        sw = round(24 + approx_text_width(status_text, 11, mono=True, bold=True) + 14)
        body += (
            f'  <rect x="35.8" y="24.0" width="{sw}" height="24" rx="12" '
            f'fill="{p["shadow"]}" fill-opacity="{"0.85" if theme=="dark" else "0.14"}"/>\n'
            f'  <rect x="34" y="22" width="{sw}" height="24" rx="12" '
            f'fill="{t["primary_soft"]}" stroke="{t["secondary"]}" stroke-width="1.3"/>\n'
            f'  <circle cx="46" cy="34" r="4" fill="{t["primary"]}"/>\n'
            f'  <circle cx="46" cy="34" r="2" fill="{t["gold_a"]}"/>\n'
            f'  <text x="56" y="38" font-family="{MONO_FONT}" font-size="11" font-weight="700" '
            f'letter-spacing="0.9" fill="{t["secondary"]}">{status_text}</text>\n'
        )

        # Name + playful brushed-gold underline swoosh (clear of 'g' descender)
        body += (
            f'  <text x="34" y="95" font-family="{SANS_FONT}" font-size="46" font-weight="800" '
            f'letter-spacing="-1.4" fill="{t["text"]}">{esc(profile["display_name"])}</text>\n'
            f'  <path d="M36 112 Q145 107 278 112" fill="none" stroke="url(#{gold_id})" '
            f'stroke-width="4.2" stroke-linecap="round"/>\n'
        )

        # Role + tagline
        body += (
            f'  <text x="34" y="138" font-family="{SANS_FONT}" font-size="19" font-weight="700" '
            f'fill="{t["primary"]}">{esc(profile["title"])}</text>\n'
            f'  <text x="34" y="164" font-family="{SANS_FONT}" font-size="14.5" font-weight="500" '
            f'fill="{t["muted"]}">{esc(profile["tagline"])}</text>\n'
        )

        # 4 sticker focus chips with original multi-element cartoon mini-icons
        px, py = 34, 186
        for idx, tag in enumerate(profile["tags"]):
            label = tag["label"]
            accent = "primary" if idx == 0 else ("secondary" if idx == 2 else None)
            icon_name = TAG_ICONS.get(label, "ml")
            c_svg, cw = chip(
                px, py, label, t, theme=theme, font_size=11.5, height=29, pad_x=10, accent=accent, icon_name=icon_name
            )
            body += c_svg
            px += cw + 8

        # Open right cartoon scene (no BT monogram anywhere!)
        body += hero_cartoon_scene(t, theme, phone=False)

        # Crisp clickable domain sticker pill at bottom-right of scene
        dom_text = f"{profile['domain']} \u2197"
        dw = round(26 + approx_text_width(dom_text, 12, mono=True, bold=True) + 12)
        dx, dy = W - 26 - dw, 204
        body += (
            f'  <rect x="{dx + 2.5:.1f}" y="{dy + 2.5:.1f}" width="{dw}" height="30" rx="15" '
            f'fill="{p["shadow"]}" fill-opacity="{"0.90" if theme=="dark" else "0.20"}"/>\n'
            f'  <rect x="{dx:.1f}" y="{dy:.1f}" width="{dw}" height="30" rx="15" '
            f'fill="{t["paper"]}" stroke="{t["primary"]}" stroke-width="1.6"/>\n'
            f'  <circle cx="{dx + 14:.1f}" cy="{dy + 15:.1f}" r="3.5" fill="{t["gold_a"]}" stroke="{p["ink"]}" stroke-width="1"/>\n'
            f'  <text x="{dx + 24:.1f}" y="{dy + 19.2:.1f}" font-family="{MONO_FONT}" font-size="12" '
            f'font-weight="700" fill="{t["text"]}">{esc(profile["domain"])} &#x2197;</text>\n'
        )

        return svg_doc(W, H, defs, body, title=f"{profile['display_name']} — {profile['title']}")

    # Phone layout (440 x 344)
    W, H = 440, 344
    body = surface_frame(
        W, H, t, theme=theme, pattern_id=pid, glow_id=gid1, glow2_id=gid2, radius=16, fill_key="bg"
    )
    body += f'  <rect x="1.5" y="20" width="4" height="{H - 76}" rx="2" fill="{t["primary"]}"/>\n'
    body += f'  <rect x="1.5" y="{H - 50}" width="4" height="24" rx="2" fill="url(#{gold_id})"/>\n'

    # Phone cartoon illustrations (top-right AI Buddy + bottom-right Neural Cube)
    body += hero_cartoon_scene(t, theme, phone=True)

    # Top-left status pill
    p_status = "BENTRUONG.DEV"
    psw = round(22 + approx_text_width(p_status, 10.5, mono=True, bold=True) + 12)
    body += (
        f'  <rect x="23.5" y="21.5" width="{psw}" height="22" rx="11" '
        f'fill="{p["shadow"]}" fill-opacity="{"0.85" if theme=="dark" else "0.14"}"/>\n'
        f'  <rect x="22" y="20" width="{psw}" height="22" rx="11" '
        f'fill="{t["primary_soft"]}" stroke="{t["secondary"]}" stroke-width="1.2"/>\n'
        f'  <circle cx="33" cy="31" r="3.5" fill="{t["primary"]}"/>\n'
        f'  <text x="42" y="34.5" font-family="{MONO_FONT}" font-size="10.5" font-weight="700" '
        f'letter-spacing="0.8" fill="{t["secondary"]}">{p_status}</text>\n'
    )

    body += (
        f'  <text x="22" y="81" font-family="{SANS_FONT}" font-size="34" font-weight="800" '
        f'letter-spacing="-1.0" fill="{t["text"]}">{esc(profile["display_name"])}</text>\n'
        f'  <path d="M24 95 Q105 90 198 95" fill="none" stroke="url(#{gold_id})" '
        f'stroke-width="3.6" stroke-linecap="round"/>\n'
    )
    body += (
        f'  <text x="22" y="119" font-family="{SANS_FONT}" font-size="17" font-weight="700" '
        f'fill="{t["primary"]}">{esc(profile["title"])}</text>\n'
    )
    for idx, line in enumerate(_wrap_text(profile["tagline"], 42)[:2]):
        body += (
            f'  <text x="22" y="{146 + idx * 21}" font-family="{SANS_FONT}" font-size="13.5" '
            f'fill="{t["muted"]}">{esc(line)}</text>\n'
        )

    # 2-row focus chips with mini cartoon icons
    px, py = 22, 198
    for idx, tag in enumerate(profile["tags"]):
        label = tag["label"]
        accent = "primary" if idx == 0 else ("secondary" if idx == 2 else None)
        icon_name = TAG_ICONS.get(label, "ml")
        c_svg, cw = chip(
            px, py, label, t, theme=theme, font_size=11.5, height=28, pad_x=10, accent=accent, icon_name=icon_name
        )
        # Keep row 2 well clear of bottom-right cube (x=346) by wrapping onto row 2 at idx >= 2 or overflow
        max_row_x = 330 if py > 220 else (W - 22)
        if px + cw > max_row_x or idx == 2:
            px = 22
            py += 36
            c_svg, cw = chip(
                px, py, label, t, theme=theme, font_size=11.5, height=28, pad_x=10, accent=accent, icon_name=icon_name
            )
        body += c_svg
        px += cw + 8

    # Domain sticker pill bottom-left
    dom_text = f"{profile['domain']} \u2197"
    dw = round(24 + approx_text_width(dom_text, 11.5, mono=True, bold=True) + 12)
    dx, dy = 22, 286
    body += (
        f'  <rect x="{dx + 2.2:.1f}" y="{dy + 2.2:.1f}" width="{dw}" height="28" rx="14" '
        f'fill="{p["shadow"]}" fill-opacity="{"0.90" if theme=="dark" else "0.18"}"/>\n'
        f'  <rect x="{dx:.1f}" y="{dy:.1f}" width="{dw}" height="28" rx="14" '
        f'fill="{t["paper"]}" stroke="{t["primary"]}" stroke-width="1.5"/>\n'
        f'  <circle cx="{dx + 13:.1f}" cy="{dy + 14:.1f}" r="3.2" fill="{t["gold_a"]}" stroke="{p["ink"]}" stroke-width="1"/>\n'
        f'  <text x="{dx + 22:.1f}" y="{dy + 18:.1f}" font-family="{MONO_FONT}" font-size="11.5" '
        f'font-weight="700" fill="{t["text"]}">{esc(profile["domain"])} &#x2197;</text>\n'
    )

    return svg_doc(W, H, defs, body, title=f"{profile['display_name']} — {profile['title']}")


def render_badge(link: dict[str, Any], t: dict[str, str], theme: str = "light") -> str:
    label = link["label"]
    icon = link.get("icon", "globe")
    is_primary = link.get("variant") == "primary"
    p = sticker_palette(t, theme)

    lw = approx_text_width(label, 13.5, bold=True)
    W = round(12 + 24 + 9 + lw + 18 + 4)
    H = 44

    fill = t["primary"] if is_primary else t["paper"]
    stroke = t["gold_a"] if is_primary else t["primary"]
    tc = t["on_primary"] if is_primary else t["text"]
    shadow_op = "0.95" if theme == "dark" else "0.22"

    body = (
        f'  <rect x="4" y="4" width="{W - 5}" height="{H - 5}" rx="12" '
        f'fill="{p["shadow"]}" fill-opacity="{shadow_op}"/>\n'
        f'  <rect x="1" y="1" width="{W - 5}" height="{H - 5}" rx="12" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="1.6"/>\n'
    )
    body += badge_cartoon_icon(icon, 11.5, 8.5, 24, t, theme, on_primary=is_primary)
    body += (
        f'  <text x="43" y="25.5" font-family="{SANS_FONT}" font-size="13.5" '
        f'font-weight="700" fill="{tc}">{esc(label)}</text>\n'
    )
    return svg_doc(W, H, "", body, title=label)


def render_section_header(
    index: str,
    title: str,
    right_note: str,
    t: dict[str, str],
    theme: str = "light",
    phone: bool = False,
) -> str:
    W = 440 if phone else 880
    H = 64 if phone else 68
    vp = "p" if phone else "d"
    gold_id = f"hdr-{index}-gold-{theme}-{vp}"
    defs = gold_grad_defs(gold_id, t["gold_a"], t["gold_b"])
    p = sticker_palette(t, theme)

    body = surface_frame(
        W, H, t, theme=theme, radius=14, fill_key="bg", stroke_key="divider", stroke_width=1.5, shadow_dx=3.5, shadow_dy=3.5
    )

    # Large cartoon emblem on left
    kind = "activity" if index == "01" else "work"
    em_size = 38 if phone else 42
    em_y = (H - 4 - em_size) / 2
    body += section_emblem(kind, 14 if not phone else 12, em_y, em_size, t, theme)

    # Gold index pill
    ix = 60 if phone else 68
    iy = 16 if phone else 17
    body += (
        f'  <rect x="{ix + 1.5}" y="{iy + 2}" width="32" height="26" rx="8" '
        f'fill="{p["shadow"]}" fill-opacity="{"0.85" if theme=="dark" else "0.18"}"/>\n'
        f'  <rect x="{ix}" y="{iy}" width="32" height="26" rx="8" '
        f'fill="url(#{gold_id})" stroke="{p["ink"]}" stroke-width="1.4"/>\n'
        f'  <text x="{ix + 16}" y="{iy + 17}" text-anchor="middle" font-family="{MONO_FONT}" '
        f'font-size="12" font-weight="800" fill="{p["ink"]}">{esc(index)}</text>\n'
    )

    # Bold title
    tx = ix + 44
    body += (
        f'  <text x="{tx}" y="{iy + 19}" font-family="{SANS_FONT}" font-size="{20 if phone else 22}" '
        f'font-weight="800" letter-spacing="-0.4" fill="{t["text"]}">{esc(title)}</text>\n'
    )

    # Decorative emerald & gold dash accent
    title_w = approx_text_width(title, 20 if phone else 22, bold=True)
    rule_x1 = tx + title_w + 14
    if phone:
        rule_x2 = W - 18
    else:
        right_pill_w = 0
        if right_note:
            note_w = approx_text_width(right_note, 11.5, mono=True, bold=True)
            right_pill_w = round(10 + 16 + 6 + note_w + 12)
        rule_x2 = W - 24 - right_pill_w - 14

    if rule_x2 - rule_x1 > 28:
        cy_line = iy + 13
        body += (
            f'  <line x1="{rule_x1:.1f}" y1="{cy_line}" x2="{rule_x2:.1f}" y2="{cy_line}" '
            f'stroke="{t["primary"]}" stroke-opacity="0.45" stroke-width="2" stroke-dasharray="4 6" stroke-linecap="round"/>\n'
        )

    if right_note and not phone:
        note_icon = "clock" if index == "01" else "star"
        pill_svg, pw = _sticker_pill(0, 0, right_note, t, theme, icon_name=note_icon, font_size=11.5, height=28, pad_x=10)
        # Re-render at exact right position
        pill_svg, _ = _sticker_pill(
            W - 18 - pw, 17, right_note, t, theme, icon_name=note_icon, font_size=11.5, height=28, pad_x=10, accent="secondary" if index == "02" else None
        )
        body += pill_svg

    return svg_doc(W, H, defs, body, title=title)


def render_github_stats(state: dict[str, Any], t: dict[str, str], theme: str, phone: bool = False) -> str:
    cur_streak = state["current_streak"]
    cur_label = f"{cur_streak} day" if cur_streak == 1 else f"{cur_streak} days"
    cur_sub = _fmt_short_date(state["current_streak_start"]) if cur_streak > 0 else "starting today"

    long_streak = state["longest_streak"]
    long_label = f"{long_streak} day" if long_streak == 1 else f"{long_streak} days"

    cards = [
        {
            "eyebrow": "LAST 12 MONTHS",
            "value": _fmt_num(state["last_year_contributions"]),
            "sub": "total contributions",
            "accent": t["primary"],
            "fill": t["primary_soft"],
            "border": t["primary"],
            "icon": "12m",
        },
        {
            "eyebrow": "CURRENT STREAK",
            "value": cur_label,
            "sub": cur_sub,
            "accent": t["primary"],
            "fill": t["paper"],
            "border": t["primary"],
            "icon": "streak",
        },
        {
            "eyebrow": "LONGEST STREAK",
            "value": long_label,
            "sub": "personal best",
            "accent": t["secondary"],
            "fill": t["secondary_soft"],
            "border": t["secondary"],
            "icon": "longest",
        },
        {
            "eyebrow": f"SINCE {state['created_year']}",
            "value": _fmt_num(state["all_time_contributions"]),
            "sub": "all-time contributions",
            "accent": t["secondary"],
            "fill": t["paper"],
            "border": t["secondary"],
            "icon": "alltime",
        },
    ]

    vp = "p" if phone else "d"
    pid = f"stats-dots-{theme}-{vp}"
    gid = f"stats-glow-{theme}-{vp}"
    defs = (
        dot_field_defs(pid, t["dot"], step=28, r=1.1, opacity=0.35 if theme == "dark" else 0.25)
        + radial_glow_defs(gid, t["primary"], cx="50%", cy="15%", r="70%", opacity=0.10 if theme == "dark" else 0.05)
    )
    p = sticker_palette(t, theme)
    sub_shadow_op = "0.90" if theme == "dark" else "0.18"

    if not phone:
        W, H = 880, 216
        body = surface_frame(W, H, t, theme=theme, pattern_id=pid, glow_id=gid, radius=16, fill_key="bg")

        gap = 14
        pad = 20
        cw = (W - pad * 2 - 4 - gap * 3) / 4
        ch = 118
        cy = 18

        for idx, c in enumerate(cards):
            cx = pad + idx * (cw + gap)
            body += (
                f'  <rect x="{cx + 3:.1f}" y="{cy + 3.5:.1f}" width="{cw - 3:.1f}" height="{ch}" rx="12" '
                f'fill="{p["shadow"]}" fill-opacity="{sub_shadow_op}"/>\n'
                f'  <rect x="{cx:.1f}" y="{cy}" width="{cw - 3:.1f}" height="{ch}" rx="12" '
                f'fill="{c["fill"]}" stroke="{c["border"]}" stroke-width="1.5"/>\n'
                f'  <rect x="{cx + 14:.1f}" y="{cy + ch - 4:.1f}" width="38" height="3" rx="1.5" '
                f'fill="{c["accent"]}"/>\n'
            )
            # Large top-right cartoon icon (clear of eyebrow and numeral)
            body += stat_cartoon_icon(c["icon"], cx + cw - 52, cy + 12, 38, t, theme)

            body += (
                f'  <text x="{cx + 14:.1f}" y="{cy + 27}" font-family="{MONO_FONT}" font-size="10" '
                f'font-weight="700" letter-spacing="0.6" fill="{c["accent"]}">{esc(c["eyebrow"])}</text>\n'
            )
            body += (
                f'  <text x="{cx + 14:.1f}" y="{cy + 74}" font-family="{SANS_FONT}" font-size="30" '
                f'font-weight="800" letter-spacing="-0.8" fill="{t["text"]}">{esc(c["value"])}</text>\n'
            )
            body += (
                f'  <text x="{cx + 14:.1f}" y="{cy + 100}" font-family="{SANS_FONT}" font-size="12.5" '
                f'font-weight="500" fill="{t["muted"]}">{esc(c["sub"])}</text>\n'
            )

        # Footer sticker pill row
        footer_items = [
            ("repo", f"{state['public_repos']} public repos", "primary"),
            ("star", f"{state['stars_earned']} stars earned", "secondary"),
            ("bolt", f"{state['active_days_year']} active days (1y)", "primary"),
            ("clock", f"updated {_fmt_date(state['fetched_at'])}", None),
        ]
        pills = []
        total_pw = 0
        for ic, lbl, acc in footer_items:
            _, pw = _sticker_pill(0, 0, lbl, t, theme, icon_name=ic, font_size=11.5, height=30, pad_x=11, accent=acc)
            pills.append((ic, lbl, acc, pw))
            total_pw += pw
        total_pw += 12 * (len(pills) - 1)
        fx = (W - 4 - total_pw) / 2
        fy = 158
        for ic, lbl, acc, pw in pills:
            p_svg, _ = _sticker_pill(fx, fy, lbl, t, theme, icon_name=ic, font_size=11.5, height=30, pad_x=11, accent=acc)
            body += p_svg
            fx += pw + 12

        return svg_doc(W, H, defs, body, title="GitHub Activity Stats")

    # Phone layout (2x2 grid, 440 x 344)
    W, H = 440, 344
    body = surface_frame(W, H, t, theme=theme, pattern_id=pid, glow_id=gid, radius=16, fill_key="bg")
    cw = 191
    ch = 112
    for idx, c in enumerate(cards):
        col = idx % 2
        row = idx // 2
        cx = 18 + col * (cw + 14)
        cy = 18 + row * (ch + 14)
        body += (
            f'  <rect x="{cx + 3:.1f}" y="{cy + 3.5:.1f}" width="{cw - 3:.1f}" height="{ch}" rx="12" '
            f'fill="{p["shadow"]}" fill-opacity="{sub_shadow_op}"/>\n'
            f'  <rect x="{cx:.1f}" y="{cy}" width="{cw - 3:.1f}" height="{ch}" rx="12" '
            f'fill="{c["fill"]}" stroke="{c["border"]}" stroke-width="1.5"/>\n'
            f'  <rect x="{cx + 12:.1f}" y="{cy + ch - 4:.1f}" width="32" height="3" rx="1.5" fill="{c["accent"]}"/>\n'
        )
        body += stat_cartoon_icon(c["icon"], cx + cw - 45, cy + 10, 34, t, theme)
        body += (
            f'  <text x="{cx + 12}" y="{cy + 25}" font-family="{MONO_FONT}" font-size="9.5" '
            f'font-weight="700" letter-spacing="0.5" fill="{c["accent"]}">{esc(c["eyebrow"])}</text>\n'
        )
        body += (
            f'  <text x="{cx + 12}" y="{cy + 70}" font-family="{SANS_FONT}" font-size="27" '
            f'font-weight="800" fill="{t["text"]}">{esc(c["value"])}</text>\n'
        )
        body += (
            f'  <text x="{cx + 12}" y="{cy + 94}" font-family="{SANS_FONT}" font-size="11.5" '
            f'font-weight="500" fill="{t["muted"]}">{esc(c["sub"])}</text>\n'
        )

    phone_items = [
        ("repo", f"{state['public_repos']} repos", "primary"),
        ("star", f"{state['stars_earned']} stars", "secondary"),
        ("bolt", f"{state['active_days_year']} active days", "primary"),
    ]
    pills = []
    total_pw = 0
    for ic, lbl, acc in phone_items:
        _, pw = _sticker_pill(0, 0, lbl, t, theme, icon_name=ic, font_size=11, height=28, pad_x=9, accent=acc)
        pills.append((ic, lbl, acc, pw))
        total_pw += pw
    total_pw += 8 * (len(pills) - 1)
    fx = (W - 4 - total_pw) / 2
    fy = 282
    for ic, lbl, acc, pw in pills:
        p_svg, _ = _sticker_pill(fx, fy, lbl, t, theme, icon_name=ic, font_size=11, height=28, pad_x=9, accent=acc)
        body += p_svg
        fx += pw + 8

    return svg_doc(W, H, defs, body, title="GitHub Activity Stats")


def _cell_level(count: int, max_count: int) -> int:
    if count <= 0:
        return 0
    if max_count <= 4:
        return min(4, count)
    ratio = count / max(max_count, 1)
    if ratio <= 0.18:
        return 1
    if ratio <= 0.42:
        return 2
    if ratio <= 0.72:
        return 3
    return 4


def render_heatmap(
    days: list[dict[str, Any]],
    total: int,
    subtitle: str,
    t: dict[str, str],
    theme: str,
    graph_id: str,
    show_numbers: bool = True,
    phone: bool = False,
) -> str:
    vp = "p" if phone else "d"
    gid = f"graph-{graph_id}-glow-{theme}-{vp}"
    defs = radial_glow_defs(gid, t["primary"], cx="12%", cy="18%", r="45%", opacity=0.09 if theme == "dark" else 0.05)

    sorted_days = sorted(days, key=lambda d: d["date"])
    if not sorted_days:
        W, H = (440, 100) if phone else (880, 100)
        body = surface_frame(W, H, t, theme=theme, glow_id=gid, radius=14, fill_key="paper")
        body += stat_cartoon_icon("heatmap", 18, 28, 32, t, theme)
        body += (
            f'  <text x="60" y="50" font-family="{SANS_FONT}" font-size="16" '
            f'font-weight="700" fill="{t["muted"]}">0 {esc(subtitle)}</text>\n'
        )
        return svg_doc(W, H, defs, body, title=f"0 {subtitle}")

    if phone and len(sorted_days) > 112:
        sorted_days = sorted_days[-112:]
        total = sum(d["count"] for d in sorted_days)
        if "6 months" in subtitle or "12 months" in subtitle:
            subtitle = "contributions in the last 16 weeks"

    first_dt = dt.date.fromisoformat(sorted_days[0]["date"])
    lead_pad = (first_dt.weekday() + 1) % 7
    padded: list[dict[str, Any] | None] = [None] * lead_pad + list(sorted_days)
    weeks: list[list[dict[str, Any] | None]] = [
        padded[i : i + 7] for i in range(0, len(padded), 7)
    ]
    n_weeks = len(weeks)
    max_count = max((d["count"] for d in sorted_days), default=0)

    W = 440 if phone else 880
    pad_x = 18 if phone else 26
    avail_w = W - pad_x * 2 - 4
    gap = 4 if (show_numbers and n_weeks <= 28) else 2.5
    cell = min((avail_w - gap * (n_weeks - 1)) / max(n_weeks, 1), 26.0)
    grid_w = n_weeks * cell + (n_weeks - 1) * gap
    grid_x = (W - 4 - grid_w) / 2
    grid_y = 84
    grid_h = 7 * cell + 6 * gap
    H = int(grid_y + grid_h + 26)

    body = surface_frame(W, H, t, theme=theme, glow_id=gid, radius=14, fill_key="paper")

    # Header cartoon commit-matrix gem icon + total + subtitle
    icon_sz = 28 if phone else 32
    icon_x = 16 if phone else 22
    icon_y = 14 if phone else 15
    body += stat_cartoon_icon("heatmap", icon_x, icon_y, icon_sz, t, theme)

    tot_str = _fmt_num(total)
    tot_size = 18 if phone else 21
    tot_w = approx_text_width(tot_str, tot_size, bold=True)
    text_x = icon_x + icon_sz + 10
    body += (
        f'  <text x="{text_x}" y="37" font-family="{SANS_FONT}" font-size="{tot_size}" '
        f'font-weight="800" fill="{t["text"]}">{esc(tot_str)}</text>\n'
    )
    body += (
        f'  <text x="{text_x + tot_w + 8:.1f}" y="36" font-family="{MONO_FONT}" '
        f'font-size="{11 if phone else 13}" fill="{t["muted"]}">{esc(subtitle)}</text>\n'
    )

    if not phone:
        lx = W - pad_x - 122
        ly = 24
        body += (
            f'  <text x="{lx - 6}" y="{ly + 10}" text-anchor="end" font-family="{MONO_FONT}" '
            f'font-size="11" fill="{t["muted"]}">Less</text>\n'
        )
        for lvl in range(5):
            body += (
                f'  <rect x="{lx + lvl * 16}" y="{ly}" width="12" height="12" rx="3" '
                f'fill="{t[f"cell{lvl}"]}"/>\n'
            )
        body += (
            f'  <text x="{lx + 84}" y="{ly + 10}" font-family="{MONO_FONT}" '
            f'font-size="11" fill="{t["muted"]}">More</text>\n'
        )

    # Month labels
    last_month = -1
    last_label_x = -100.0
    for wi, wk in enumerate(weeks):
        first_real = next((d for d in wk if d is not None), None)
        if not first_real:
            continue
        m = int(first_real["date"][5:7])
        if m != last_month:
            mx = grid_x + wi * (cell + gap)
            if mx - last_label_x >= 34:
                body += (
                    f'  <text x="{mx:.1f}" y="{grid_y - 11}" font-family="{MONO_FONT}" '
                    f'font-size="{11 if phone else 12}" fill="{t["muted"]}">{MONTH_NAMES[m - 1]}</text>\n'
                )
                last_label_x = mx
            last_month = m

    rx = 4 if cell >= 18 else 2.5
    draw_nums = show_numbers and cell >= 18
    for wi, wk in enumerate(weeks):
        cx = grid_x + wi * (cell + gap)
        for di, item in enumerate(wk):
            if item is None:
                continue
            cy = grid_y + di * (cell + gap)
            cnt = item["count"]
            lvl = _cell_level(cnt, max_count)
            body += (
                f'  <rect x="{cx:.1f}" y="{cy:.1f}" width="{cell:.1f}" height="{cell:.1f}" '
                f'rx="{rx}" fill="{t[f"cell{lvl}"]}"/>\n'
            )
            if draw_nums:
                if cnt == 0:
                    tc = t["cell_text_dim"]
                    fs = 9.5
                else:
                    tc = t["cell_text_dark"] if lvl >= 3 else t["cell_text_light"]
                    fs = 9.5 if cnt < 100 else 8.0
                body += (
                    f'  <text x="{cx + cell / 2:.1f}" y="{cy + cell / 2 + fs * 0.35:.1f}" '
                    f'text-anchor="middle" font-family="{MONO_FONT}" font-size="{fs}" '
                    f'font-weight="{"700" if cnt > 0 else "400"}" fill="{tc}">{cnt}</text>\n'
                )

    return svg_doc(W, H, defs, body, title=f"{tot_str} {subtitle}")


def render_project_card(
    proj: dict[str, Any],
    stars: int,
    t: dict[str, str],
    theme: str,
    phone: bool = False,
) -> str:
    W = 432
    H = 246 if phone else 232
    vp = "p" if phone else "d"
    proj_id = proj["id"]
    gid = f"proj-{proj_id}-glow-{theme}-{vp}"
    gold_id = f"proj-{proj_id}-gold-{theme}-{vp}"
    glow_color = t["primary"] if proj_id in ("badminton", "flyer") else t["secondary"]
    defs = (
        radial_glow_defs(gid, glow_color, cx="82%", cy="28%", r="52%", opacity=0.16 if theme == "dark" else 0.09)
        + gold_grad_defs(gold_id, t["gold_a"], t["gold_b"])
    )
    p = sticker_palette(t, theme)

    body = surface_frame(
        W, H, t, theme=theme, glow_id=gid, radius=15, fill_key="paper", stroke_key="divider", stroke_width=1.5
    )

    # Bottom dual-tone emerald + gold signature stripe
    body += f'  <rect x="22" y="{H - 9.5}" width="54" height="3.5" rx="1.75" fill="{t["primary"]}"/>\n'
    body += f'  <rect x="82" y="{H - 9.5}" width="24" height="3.5" rx="1.75" fill="url(#{gold_id})"/>\n'

    # Overline gold sticker pill in upper-left
    overline = proj["overline"]
    if stars > 0:
        overline = f"{overline} · ★ {stars}"
    ov_fs = 10.5 if phone else 10.0
    ov_w = round(16 + approx_text_width(overline, ov_fs, mono=True, bold=True))
    body += (
        f'  <rect x="22" y="18" width="{ov_w}" height="22" rx="7" '
        f'fill="{t["secondary_soft"]}" stroke="{t["secondary"]}" stroke-width="1.2"/>\n'
        f'  <text x="30" y="32.5" font-family="{MONO_FONT}" font-size="{ov_fs}" font-weight="700" '
        f'letter-spacing="0.6" fill="{t["secondary"]}">{esc(overline)}</text>\n'
    )

    # Top-right arrow badge (strictly clear of the 88x88 illustration below it)
    ax, ay = W - 38, 15
    body += (
        f'  <rect x="{ax}" y="{ay}" width="22" height="22" rx="7" '
        f'fill="{t["primary_soft"]}" stroke="{t["primary"]}" stroke-width="1.2"/>\n'
    )
    body += icon_svg("arrow_ne", ax + 3, ay + 3, 16, t["primary"])

    # Dedicated upper-right cartoon illustration stage (x=304..392, y=40..128)
    body += project_cartoon_icon(
        proj_id,
        304,
        40,
        88,
        t,
        theme,
        stroke_boost=0.35 if phone else 0.0,
    )

    # Left text zone safely bounded inside x=22..294 (max width 272px)
    title_fs = 20.0 if phone else 18.5
    name_lines = _wrap_text(proj["name"], 23 if phone else 25)[:2]
    title_y = 66
    for idx, nl in enumerate(name_lines):
        body += (
            f'  <text x="22" y="{title_y + idx * 23}" font-family="{SANS_FONT}" font-size="{title_fs}" '
            f'font-weight="800" letter-spacing="-0.3" fill="{t["text"]}">{esc(nl)}</text>\n'
        )

    desc_y = title_y + len(name_lines) * 23 + 4
    desc_fs = 13.5 if phone else 13.0
    desc_lines = _wrap_text(proj["line"], 34 if phone else 36)
    for idx, ln in enumerate(desc_lines):
        body += (
            f'  <text x="22" y="{desc_y + idx * (19 if phone else 18)}" font-family="{SANS_FONT}" '
            f'font-size="{desc_fs}" font-weight="500" fill="{t["muted"]}">{esc(ln)}</text>\n'
        )

    # Bottom full-width tech chip strip — wraps cleanly onto 2 rows, never drops chips
    chip_fs = 11.5 if phone else 11.0
    chip_h = 25 if phone else 24
    px = 22
    py = max(154 if not phone else 162, desc_y + len(desc_lines) * (19 if phone else 18) + 6)
    for idx, tech in enumerate(proj["chips"]):
        acc = "primary" if idx == 0 else None
        c_svg, cw = chip(px, py, tech, t, theme=theme, font_size=chip_fs, height=chip_h, pad_x=9, mono=True, accent=acc)
        if px + cw > W - 22 and px > 22:
            px = 22
            py += chip_h + 6
            c_svg, cw = chip(px, py, tech, t, theme=theme, font_size=chip_fs, height=chip_h, pad_x=9, mono=True, accent=acc)
        body += c_svg
        px += cw + 6

    return svg_doc(W, H, defs, body, title=proj["name"])
