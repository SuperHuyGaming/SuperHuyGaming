"""Render all dark/light and desktop/phone SVG cards matching bentruong.dev's design system."""

from __future__ import annotations

import datetime as dt
from typing import Any

from svgkit import (
    MONO_FONT,
    SANS_FONT,
    approx_text_width,
    bt_logo_mark,
    chip,
    dot_field_defs,
    esc,
    gold_grad_defs,
    icon_svg,
    radial_glow_defs,
    surface_frame,
    svg_doc,
)


MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


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


def render_hero(profile: dict[str, Any], t: dict[str, str], theme: str, phone: bool = False) -> str:
    pid = f"hero-dots-{theme}-{'p' if phone else 'd'}"
    gid = f"hero-glow-{theme}-{'p' if phone else 'd'}"
    gold_id = f"bt-gold-{theme}-{'p' if phone else 'd'}"
    defs = (
        dot_field_defs(pid, t["dot"], step=28, r=1.15, opacity=0.45 if theme == "dark" else 0.35)
        + radial_glow_defs(gid, t["primary"], cx="86%", cy="26%", r="56%", opacity=0.14 if theme == "dark" else 0.08)
        + gold_grad_defs(gold_id, t["gold_a"], t["gold_b"])
    )

    if not phone:
        W, H = 880, 232
        body = surface_frame(W, H, t, pattern_id=pid, glow_id=gid, radius=12, fill_key="bg")

        # Left vertical emerald accent bar
        body += f'  <rect x="0.75" y="24" width="3" height="{H - 48}" rx="1.5" fill="{t["primary"]}"/>\n'

        # Top eyebrow + domain status
        body += f'  <circle cx="40" cy="36" r="3.5" fill="{t["primary"]}"/>\n'
        body += (
            f'  <text x="52" y="40" font-family="{MONO_FONT}" font-size="11.5" font-weight="600" '
            f'letter-spacing="1.2" fill="{t["secondary"]}">BENTRUONG.DEV · GEORGE MASON CS</text>\n'
        )

        # Big tight-tracked name (matching Hero.jsx)
        body += (
            f'  <text x="36" y="96" font-family="{SANS_FONT}" font-size="48" font-weight="800" '
            f'letter-spacing="-1.6" fill="{t["text"]}">{esc(profile["display_name"])}</text>\n'
        )

        # Emerald title
        body += (
            f'  <text x="36" y="128" font-family="{SANS_FONT}" font-size="19" font-weight="600" '
            f'fill="{t["primary"]}">{esc(profile["title"])}</text>\n'
        )

        # Muted intro
        body += (
            f'  <text x="36" y="156" font-family="{SANS_FONT}" font-size="15" font-weight="400" '
            f'fill="{t["muted"]}">{esc(profile["tagline"])}</text>\n'
        )

        # 4 clean MUI-style outlined focus chips
        px, py = 36, 178
        for idx, tag in enumerate(profile["tags"]):
            accent = "primary" if idx == 0 else None
            c_svg, cw = chip(px, py, tag["label"], t, font_size=12.5, height=28, pad_x=12, accent=accent)
            body += c_svg
            px += cw + 8

        # Right side: BT gold-bordered logo mark from bentruong.dev
        body += bt_logo_mark(W - 146, 56, 106, gold_id, profile["monogram"])
        body += (
            f'  <text x="{W - 93}" y="182" text-anchor="middle" font-family="{MONO_FONT}" '
            f'font-size="11.5" font-weight="500" fill="{t["muted"]}">{esc(profile["domain"])} &#x2197;</text>\n'
        )

        return svg_doc(W, H, defs, body, title=f"{profile['display_name']} — {profile['title']}")

    # Phone layout
    W, H = 440, 296
    body = surface_frame(W, H, t, pattern_id=pid, glow_id=gid, radius=12, fill_key="bg")
    body += f'  <rect x="0.75" y="20" width="3" height="{H - 40}" rx="1.5" fill="{t["primary"]}"/>\n'

    body += bt_logo_mark(W - 84, 24, 60, gold_id, profile["monogram"])

    body += f'  <circle cx="28" cy="36" r="3" fill="{t["primary"]}"/>\n'
    body += (
        f'  <text x="38" y="40" font-family="{MONO_FONT}" font-size="10.5" font-weight="600" '
        f'letter-spacing="1.0" fill="{t["secondary"]}">BENTRUONG.DEV</text>\n'
    )
    body += (
        f'  <text x="24" y="88" font-family="{SANS_FONT}" font-size="36" font-weight="800" '
        f'letter-spacing="-1.2" fill="{t["text"]}">{esc(profile["display_name"])}</text>\n'
    )
    body += (
        f'  <text x="24" y="116" font-family="{SANS_FONT}" font-size="17" font-weight="600" '
        f'fill="{t["primary"]}">{esc(profile["title"])}</text>\n'
    )
    for idx, line in enumerate(_wrap_text(profile["tagline"], 44)[:2]):
        body += (
            f'  <text x="24" y="{146 + idx * 21}" font-family="{SANS_FONT}" font-size="14" '
            f'fill="{t["muted"]}">{esc(line)}</text>\n'
        )

    px, py = 24, 200
    for idx, tag in enumerate(profile["tags"]):
        accent = "primary" if idx == 0 else None
        c_svg, cw = chip(px, py, tag["label"], t, font_size=12, height=28, pad_x=11, accent=accent)
        if px + cw > W - 20:
            px = 24
            py += 36
            c_svg, cw = chip(px, py, tag["label"], t, font_size=12, height=28, pad_x=11, accent=accent)
        body += c_svg
        px += cw + 8

    return svg_doc(W, H, defs, body, title=f"{profile['display_name']} — {profile['title']}")


def render_badge(link: dict[str, Any], t: dict[str, str]) -> str:
    label = link["label"]
    icon = link.get("icon", "globe")
    is_primary = link.get("variant") == "primary"

    lw = approx_text_width(label, 13.5, bold=True)
    W = round(16 + 16 + 8 + lw + 18)
    H = 38

    fill = t["primary"] if is_primary else t["paper"]
    stroke = t["primary"] if is_primary else t["divider"]
    tc = t["on_primary"] if is_primary else t["text"]
    ic = t["on_primary"] if is_primary else t["primary"]

    body = (
        f'  <rect x="0.75" y="0.75" width="{W - 1.5}" height="{H - 1.5}" rx="8" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="1"/>\n'
    )
    body += icon_svg(icon, 14, 11, 16, ic)
    body += (
        f'  <text x="38" y="23.5" font-family="{SANS_FONT}" font-size="13.5" '
        f'font-weight="600" fill="{tc}">{esc(label)}</text>\n'
    )
    return svg_doc(W, H, "", body, title=label)


def render_section_header(index: str, title: str, right_note: str, t: dict[str, str], phone: bool = False) -> str:
    W = 440 if phone else 880
    H = 44
    body = (
        f'  <text x="4" y="24" font-family="{MONO_FONT}" font-size="12" font-weight="700" '
        f'letter-spacing="1.2" fill="{t["secondary"]}">{esc(index)}</text>\n'
        f'  <text x="32" y="25" font-family="{SANS_FONT}" font-size="20" font-weight="700" '
        f'letter-spacing="-0.4" fill="{t["text"]}">{esc(title)}</text>\n'
    )
    if right_note and not phone:
        body += (
            f'  <text x="{W - 4}" y="24" text-anchor="end" font-family="{MONO_FONT}" '
            f'font-size="12" fill="{t["muted"]}">{esc(right_note)}</text>\n'
        )
    body += f'  <line x1="4" y1="38" x2="{W - 4}" y2="38" stroke="{t["divider"]}" stroke-width="1"/>\n'
    body += f'  <line x1="4" y1="38" x2="72" y2="38" stroke="{t["primary"]}" stroke-width="2"/>\n'
    return svg_doc(W, H, "", body, title=title)


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
        },
        {
            "eyebrow": "CURRENT STREAK",
            "value": cur_label,
            "sub": cur_sub,
            "accent": t["primary"],
        },
        {
            "eyebrow": "LONGEST STREAK",
            "value": long_label,
            "sub": "personal best",
            "accent": t["secondary"],
        },
        {
            "eyebrow": f"SINCE {state['created_year']}",
            "value": _fmt_num(state["all_time_contributions"]),
            "sub": "all-time contributions",
            "accent": t["secondary"],
        },
    ]

    footer = (
        f"{state['public_repos']} public repos  ·  "
        f"{state['stars_earned']} stars earned  ·  "
        f"{state['active_days_year']} active days (1y)  ·  "
        f"updated {_fmt_date(state['fetched_at'])}"
    )

    if not phone:
        W, H = 880, 178
        body = surface_frame(W, H, t, radius=12, fill_key="bg")

        gap = 14
        pad = 20
        cw = (W - pad * 2 - gap * 3) / 4
        ch = 110
        cy = 20

        for idx, c in enumerate(cards):
            cx = pad + idx * (cw + gap)
            body += (
                f'  <rect x="{cx:.1f}" y="{cy}" width="{cw:.1f}" height="{ch}" rx="10" '
                f'fill="{t["paper"]}" stroke="{t["divider"]}" stroke-width="1"/>\n'
            )
            # Subtle bottom accent line
            body += (
                f'  <rect x="{cx + 16:.1f}" y="{cy + ch - 3}" width="32" height="2.5" rx="1.25" '
                f'fill="{c["accent"]}"/>\n'
            )
            body += (
                f'  <text x="{cx + 16:.1f}" y="{cy + 26}" font-family="{MONO_FONT}" font-size="10.5" '
                f'font-weight="700" letter-spacing="0.9" fill="{c["accent"]}">{esc(c["eyebrow"])}</text>\n'
            )
            body += (
                f'  <text x="{cx + 16:.1f}" y="{cy + 66}" font-family="{SANS_FONT}" font-size="31" '
                f'font-weight="800" letter-spacing="-0.8" fill="{t["text"]}">{esc(c["value"])}</text>\n'
            )
            body += (
                f'  <text x="{cx + 16:.1f}" y="{cy + 90}" font-family="{SANS_FONT}" font-size="12.5" '
                f'fill="{t["muted"]}">{esc(c["sub"])}</text>\n'
            )

        # Clean summary strip below
        body += (
            f'  <text x="{W / 2:.1f}" y="156" text-anchor="middle" font-family="{MONO_FONT}" '
            f'font-size="12" fill="{t["muted"]}">{esc(footer)}</text>\n'
        )
        return svg_doc(W, H, "", body, title="GitHub Activity Stats")

    # Phone layout (2x2 grid)
    W, H = 440, 294
    body = surface_frame(W, H, t, radius=12, fill_key="bg")
    cw = 194
    ch = 104
    for idx, c in enumerate(cards):
        col = idx % 2
        row = idx // 2
        cx = 18 + col * (cw + 16)
        cy = 18 + row * (ch + 14)
        body += (
            f'  <rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="10" '
            f'fill="{t["paper"]}" stroke="{t["divider"]}" stroke-width="1"/>\n'
        )
        body += f'  <rect x="{cx + 14}" y="{cy + ch - 3}" width="28" height="2.5" rx="1.25" fill="{c["accent"]}"/>\n'
        body += (
            f'  <text x="{cx + 14}" y="{cy + 24}" font-family="{MONO_FONT}" font-size="10" '
            f'font-weight="700" letter-spacing="0.8" fill="{c["accent"]}">{esc(c["eyebrow"])}</text>\n'
        )
        body += (
            f'  <text x="{cx + 14}" y="{cy + 62}" font-family="{SANS_FONT}" font-size="28" '
            f'font-weight="800" fill="{t["text"]}">{esc(c["value"])}</text>\n'
        )
        body += (
            f'  <text x="{cx + 14}" y="{cy + 84}" font-family="{SANS_FONT}" font-size="12" '
            f'fill="{t["muted"]}">{esc(c["sub"])}</text>\n'
        )

    short_footer = f"{state['public_repos']} repos · {state['stars_earned']} stars · {state['active_days_year']} active days"
    body += (
        f'  <text x="{W / 2:.1f}" y="274" text-anchor="middle" font-family="{MONO_FONT}" '
        f'font-size="11.5" fill="{t["muted"]}">{esc(short_footer)}</text>\n'
    )
    return svg_doc(W, H, "", body, title="GitHub Activity Stats")


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
    sorted_days = sorted(days, key=lambda d: d["date"])
    if not sorted_days:
        W, H = (440, 96) if phone else (880, 96)
        body = surface_frame(W, H, t, radius=12, fill_key="paper")
        body += (
            f'  <text x="24" y="54" font-family="{SANS_FONT}" font-size="16" '
            f'font-weight="600" fill="{t["muted"]}">0 {esc(subtitle)}</text>\n'
        )
        return svg_doc(W, H, "", body, title=f"0 {subtitle}")

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
    avail_w = W - pad_x * 2
    gap = 4 if (show_numbers and n_weeks <= 28) else 2.5
    cell = min((avail_w - gap * (n_weeks - 1)) / max(n_weeks, 1), 26.0)
    grid_w = n_weeks * cell + (n_weeks - 1) * gap
    grid_x = (W - grid_w) / 2
    grid_y = 76
    grid_h = 7 * cell + 6 * gap
    H = int(grid_y + grid_h + 24)

    body = surface_frame(W, H, t, radius=12, fill_key="paper")

    # Header total + subtitle
    tot_str = _fmt_num(total)
    tot_size = 18 if phone else 20
    tot_w = approx_text_width(tot_str, tot_size, bold=True)
    body += (
        f'  <text x="{pad_x}" y="36" font-family="{SANS_FONT}" font-size="{tot_size}" '
        f'font-weight="700" fill="{t["text"]}">{esc(tot_str)}</text>\n'
    )
    body += (
        f'  <text x="{pad_x + tot_w + 8:.1f}" y="35" font-family="{MONO_FONT}" '
        f'font-size="{11.5 if phone else 13}" fill="{t["muted"]}">{esc(subtitle)}</text>\n'
    )

    if not phone:
        lx = W - pad_x - 118
        ly = 23
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
                    f'  <text x="{mx:.1f}" y="{grid_y - 10}" font-family="{MONO_FONT}" '
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

    return svg_doc(W, H, "", body, title=f"{tot_str} {subtitle}")


def render_project_card(
    proj: dict[str, Any],
    stars: int,
    t: dict[str, str],
    theme: str,
    phone: bool = False,
) -> str:
    W, H = 432, 198
    body = surface_frame(W, H, t, radius=12, fill_key="paper")

    # Bottom emerald signature bar (matching SmallProject in Projects.jsx)
    body += f'  <rect x="24" y="{H - 3.5}" width="64" height="3" rx="1.5" fill="{t["primary"]}"/>\n'

    # Gold uppercase overline + star count + top-right arrow
    overline = proj["overline"]
    if stars > 0:
        overline = f"{overline} · ★ {stars}"
    body += (
        f'  <text x="24" y="34" font-family="{MONO_FONT}" font-size="11" font-weight="700" '
        f'letter-spacing="0.9" fill="{t["secondary"]}">{esc(overline)}</text>\n'
    )
    body += icon_svg("arrow_ne", W - 38, 20, 16, t["muted"])

    # Project title
    body += (
        f'  <text x="24" y="66" font-family="{SANS_FONT}" font-size="20" font-weight="700" '
        f'letter-spacing="-0.3" fill="{t["text"]}">{esc(proj["name"])}</text>\n'
    )

    # Description (2 lines)
    for idx, ln in enumerate(_wrap_text(proj["line"], 48)[:2]):
        body += (
            f'  <text x="24" y="{94 + idx * 21}" font-family="{SANS_FONT}" font-size="13.5" '
            f'fill="{t["muted"]}">{esc(ln)}</text>\n'
        )

    # Outlined MUI-style tech chips
    px, py = 24, H - 52
    for tech in proj["chips"]:
        c_svg, cw = chip(px, py, tech, t, font_size=11.5, height=24, pad_x=9, mono=True)
        if px + cw > W - 20:
            break
        body += c_svg
        px += cw + 6

    return svg_doc(W, H, "", body, title=proj["name"])
