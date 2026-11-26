"""Render clean, human-crafted bentruong.dev SVGs with real photo/app previews + flat cartoon icons."""

from __future__ import annotations

import datetime as dt
from typing import Any

from svgkit import (
    MONO_FONT,
    SANS_FONT,
    approx_text_width,
    badge_cartoon_icon,
    chip,
    esc,
    load_data_uri,
    project_flat_illustration,
    snapshot_cartoon_icon,
    stat_cartoon_icon,
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
    focus_icons = ["fullstack", "agents", "ml", "dl"]
    snapshot = [
        ("grad", "B.S. CS '26 · 3.94 GPA", "M.S. ML starting Jan '27"),
        ("work", "SWE Intern @ Deepiri", "AI bug-tracing agent"),
        ("shuttle", "GMU Badminton App", "Founder · 500+ players"),
    ]

    if not phone:
        W, H = 880, 238
        body = surface_frame(W, H, t, radius=12, fill_key="bg")

        # Left editorial column
        body += (
            f'  <text x="36" y="42" font-family="{MONO_FONT}" font-size="11.5" font-weight="600" '
            f'letter-spacing="1.2" fill="{t["secondary"]}">GEORGE MASON CS  ·  BENTRUONG.DEV</text>\n'
        )
        body += (
            f'  <text x="36" y="96" font-family="{SANS_FONT}" font-size="48" font-weight="800" '
            f'letter-spacing="-1.6" fill="{t["text"]}">{esc(profile["display_name"])}</text>\n'
        )
        body += (
            f'  <text x="36" y="128" font-family="{SANS_FONT}" font-size="19" font-weight="600" '
            f'fill="{t["primary"]}">{esc(profile["title"])}</text>\n'
        )
        body += (
            f'  <text x="36" y="156" font-family="{SANS_FONT}" font-size="14.5" '
            f'fill="{t["muted"]}">{esc(profile["tagline"])}</text>\n'
        )

        # 4 focus chips with chunky flat cartoon icons
        cx, cy = 36, 178
        for idx, tag in enumerate(profile["tags"]):
            ic = focus_icons[idx % len(focus_icons)]
            c_svg, cw = chip(cx, cy, tag["label"], t, font_size=12, height=29, pad_x=10, icon_name=ic)
            body += c_svg
            cx += cw + 8

        # Crisp vertical hairline divider + right Snapshot column (no face, no logo)
        dx = 594
        body += f'  <line x1="{dx}" y1="28" x2="{dx}" y2="{H - 28}" stroke="{t["divider"]}" stroke-width="1"/>\n'
        rx = dx + 24
        body += (
            f'  <text x="{rx}" y="42" font-family="{MONO_FONT}" font-size="10.5" font-weight="700" '
            f'letter-spacing="1.1" fill="{t["secondary"]}">SNAPSHOT</text>\n'
        )
        for idx, (icon_name, top_txt, sub_txt) in enumerate(snapshot):
            ry = 62 + idx * 52
            body += snapshot_cartoon_icon(icon_name, rx, ry, 28, t)
            body += (
                f'  <text x="{rx + 38}" y="{ry + 12}" font-family="{SANS_FONT}" font-size="13.5" '
                f'font-weight="600" fill="{t["text"]}">{esc(top_txt)}</text>\n'
            )
            body += (
                f'  <text x="{rx + 38}" y="{ry + 29}" font-family="{MONO_FONT}" font-size="11.5" '
                f'fill="{t["muted"]}">{esc(sub_txt)}</text>\n'
            )

        return svg_doc(W, H, "", body, title=f"{profile['display_name']} — {profile['title']}")

    # Phone layout (clean open hero without duplicate face)
    W, H = 440, 282
    body = surface_frame(W, H, t, radius=12, fill_key="bg")

    body += (
        f'  <text x="24" y="36" font-family="{MONO_FONT}" font-size="10.5" font-weight="600" '
        f'letter-spacing="1.0" fill="{t["secondary"]}">GEORGE MASON CS · BENTRUONG.DEV</text>\n'
    )
    body += (
        f'  <text x="24" y="82" font-family="{SANS_FONT}" font-size="36" font-weight="800" '
        f'letter-spacing="-1.2" fill="{t["text"]}">{esc(profile["display_name"])}</text>\n'
    )
    body += (
        f'  <text x="24" y="110" font-family="{SANS_FONT}" font-size="17" font-weight="600" '
        f'fill="{t["primary"]}">{esc(profile["title"])}</text>\n'
    )
    for idx, line in enumerate(_wrap_text(profile["tagline"], 44)[:2]):
        body += (
            f'  <text x="24" y="{140 + idx * 20}" font-family="{SANS_FONT}" font-size="14" '
            f'fill="{t["muted"]}">{esc(line)}</text>\n'
        )

    cx, cy = 24, 192
    for idx, tag in enumerate(profile["tags"]):
        ic = focus_icons[idx % len(focus_icons)]
        c_svg, cw = chip(cx, cy, tag["label"], t, font_size=12, height=30, pad_x=10, icon_name=ic)
        if cx + cw > W - 20:
            cx = 24
            cy += 38
            c_svg, cw = chip(cx, cy, tag["label"], t, font_size=12, height=30, pad_x=10, icon_name=ic)
        body += c_svg
        cx += cw + 8

    return svg_doc(W, H, "", body, title=f"{profile['display_name']} — {profile['title']}")


def render_badge(link: dict[str, Any], t: dict[str, str]) -> str:
    label = link["label"]
    icon = link.get("icon", "globe")
    is_primary = link.get("variant") == "primary"

    lw = approx_text_width(label, 13.5, bold=True)
    W = round(14 + 20 + 8 + lw + 18)
    H = 40

    fill = t["primary"] if is_primary else t["paper"]
    stroke = t["primary"] if is_primary else t["divider"]
    tc = t["on_primary"] if is_primary else t["text"]

    body = (
        f'  <rect x="0.75" y="0.75" width="{W - 1.5}" height="{H - 1.5}" rx="8" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="1"/>\n'
    )
    body += badge_cartoon_icon(icon, 13, 10, 20, t, on_primary=is_primary)
    body += (
        f'  <text x="41" y="24.5" font-family="{SANS_FONT}" font-size="13.5" '
        f'font-weight="600" fill="{tc}">{esc(label)}</text>\n'
    )
    return svg_doc(W, H, "", body, title=label)


def render_section_header(index: str, title: str, right_note: str, t: dict[str, str], phone: bool = False) -> str:
    """Tactile Forest-Studio section header (Sketch C): gold index block with hard offset + bold heading."""
    W = 440 if phone else 880
    H = 52
    ink = "#06120D"
    body = (
        f'  <rect x="5" y="13" width="34" height="26" rx="7" fill="{ink}"/>\n'
        f'  <rect x="2" y="10" width="34" height="26" rx="7" fill="{t["secondary"]}" stroke="{ink}" stroke-width="2"/>\n'
        f'  <text x="19" y="27.5" text-anchor="middle" font-family="{MONO_FONT}" font-size="13" font-weight="800" fill="{ink}">{esc(index)}</text>\n'
        f'  <text x="48" y="31" font-family="{SANS_FONT}" font-size="{24 if phone else 26}" font-weight="800" '
        f'letter-spacing="-0.6" fill="{t["text"]}">{esc(title)}</text>\n'
    )
    if right_note and not phone:
        body += (
            f'  <text x="{W - 2}" y="29" text-anchor="end" font-family="{MONO_FONT}" '
            f'font-size="12" fill="{t["muted"]}">{esc(right_note)}</text>\n'
        )
    body += f'  <line x1="2" y1="48" x2="{W - 2}" y2="48" stroke="{t["divider"]}" stroke-width="1"/>\n'
    return svg_doc(W, H, "", body, title=title)


def render_github_stats(state: dict[str, Any], t: dict[str, str], theme: str, phone: bool = False) -> str:
    """Tactile Forest-Studio stats board (Sketch C) for both dark and light themes."""
    cur_streak = state["current_streak"]
    if cur_streak >= 2:
        slot2 = {
            "eyebrow": "CURRENT STREAK",
            "value": f"{cur_streak} days",
            "sub": _fmt_short_date(state["current_streak_start"]),
            "icon": "flame",
        }
    else:
        slot2 = {
            "eyebrow": "ACTIVE DAYS (1Y)",
            "value": f"{state['active_days_year']} days",
            "sub": "shipped in last year",
            "icon": "bolt",
        }

    long_streak = state["longest_streak"]
    long_label = f"{long_streak} day" if long_streak == 1 else f"{long_streak} days"

    cards = [
        {
            "eyebrow": "LAST 12 MONTHS",
            "value": _fmt_num(state["last_year_contributions"]),
            "sub": "total contributions",
            "icon": "calendar",
        },
        slot2,
        {
            "eyebrow": "LONGEST STREAK",
            "value": long_label,
            "sub": "personal best",
            "icon": "trophy",
        },
        {
            "eyebrow": f"SINCE {state['created_year']}",
            "value": _fmt_num(state["all_time_contributions"]),
            "sub": "all-time contributions",
            "icon": "bars",
        },
    ]

    if theme == "dark":
        ink = "#06120D"
        card_fills = ["#1C563F", "#5C451A", "#1B4E56", "#35492A"]
        mini_fills = ["#1B4E56", "#5C451A", "#1C563F"]
        eyebrow_c = "#E8F5EE"
        val_c = "#FFFFFF"
        sub_c = "#D5E8DE"
    else:
        ink = "#13221B"
        card_fills = ["#CFEAD9", "#F6E5B8", "#CCE8EC", "#DCE9CA"]
        mini_fills = ["#CCE8EC", "#F6E5B8", "#CFEAD9"]
        eyebrow_c = "#234031"
        val_c = "#102119"
        sub_c = "#2F4A3C"

    minis = [
        ("folder", _fmt_num(state["public_repos"]), "public repos"),
        ("star", _fmt_num(state["stars_earned"]), "stars earned"),
        ("bolt_sm", _fmt_num(state["active_days_year"]), "active days (1y)"),
    ]

    if not phone:
        W, H = 880, 240
        body = surface_frame(W, H, t, radius=16, fill_key="bg")

        gap = 14
        pad = 20
        cw = (W - pad * 2 - gap * 3) / 4
        ch = 134
        cy = 18

        for idx, c in enumerate(cards):
            cx = pad + idx * (cw + gap)
            body += (
                f'  <rect x="{cx + 4:.1f}" y="{cy + 4}" width="{cw:.1f}" height="{ch}" rx="14" fill="{ink}"/>\n'
                f'  <rect x="{cx:.1f}" y="{cy}" width="{cw:.1f}" height="{ch}" rx="14" '
                f'fill="{card_fills[idx]}" stroke="{ink}" stroke-width="2.2"/>\n'
            )
            body += stat_cartoon_icon(c["icon"], cx + cw - 50, cy + 14, 38, t)
            body += (
                f'  <text x="{cx + 16:.1f}" y="{cy + 30}" font-family="{MONO_FONT}" font-size="10.5" '
                f'font-weight="700" letter-spacing="0.8" fill="{eyebrow_c}" fill-opacity="0.85">{esc(c["eyebrow"])}</text>\n'
            )
            body += (
                f'  <text x="{cx + 16:.1f}" y="{cy + 84}" font-family="{SANS_FONT}" font-size="38" '
                f'font-weight="800" letter-spacing="-1.0" fill="{val_c}">{esc(c["value"])}</text>\n'
            )
            body += (
                f'  <text x="{cx + 16:.1f}" y="{cy + 111}" font-family="{SANS_FONT}" font-size="13" '
                f'fill="{sub_c}">{esc(c["sub"])}</text>\n'
            )

        # 3 tactile mini-cards across bottom
        fw = (W - pad * 2 - gap * 2) / 3
        fy = 172
        fh = 46
        for idx, (ic, val, lbl) in enumerate(minis):
            fx = pad + idx * (fw + gap)
            vw = approx_text_width(val, 22, bold=True)
            body += (
                f'  <rect x="{fx + 3:.1f}" y="{fy + 3}" width="{fw:.1f}" height="{fh}" rx="11" fill="{ink}"/>\n'
                f'  <rect x="{fx:.1f}" y="{fy}" width="{fw:.1f}" height="{fh}" rx="11" '
                f'fill="{mini_fills[idx]}" stroke="{ink}" stroke-width="2"/>\n'
            )
            body += badge_cartoon_icon(ic, fx + 16, fy + 13, 21, t)
            body += (
                f'  <text x="{fx + 46:.1f}" y="{fy + 30}" font-family="{SANS_FONT}" font-size="22" '
                f'font-weight="800" fill="{val_c}">{esc(val)}</text>\n'
            )
            body += (
                f'  <text x="{fx + 54 + vw:.1f}" y="{fy + 28.5}" font-family="{MONO_FONT}" font-size="12.5" '
                f'fill="{sub_c}">{esc(lbl)}</text>\n'
            )

        return svg_doc(W, H, "", body, title="GitHub Activity Stats")

    # Phone layout (2x2 tactile cards + 3 stacked tactile mini-cards)
    W, H = 440, 444
    body = surface_frame(W, H, t, radius=16, fill_key="bg")
    cw = 192
    ch = 116
    for idx, c in enumerate(cards):
        col = idx % 2
        row = idx // 2
        cx = 18 + col * (cw + 16)
        cy = 18 + row * (ch + 16)
        body += (
            f'  <rect x="{cx + 3.5}" y="{cy + 3.5}" width="{cw}" height="{ch}" rx="13" fill="{ink}"/>\n'
            f'  <rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="13" '
            f'fill="{card_fills[idx]}" stroke="{ink}" stroke-width="2"/>\n'
        )
        body += stat_cartoon_icon(c["icon"], cx + cw - 40, cy + 12, 30, t)
        body += (
            f'  <text x="{cx + 14}" y="{cy + 27}" font-family="{MONO_FONT}" font-size="10" '
            f'font-weight="700" letter-spacing="0.7" fill="{eyebrow_c}" fill-opacity="0.85">{esc(c["eyebrow"])}</text>\n'
        )
        body += (
            f'  <text x="{cx + 14}" y="{cy + 74}" font-family="{SANS_FONT}" font-size="31" '
            f'font-weight="800" letter-spacing="-0.8" fill="{val_c}">{esc(c["value"])}</text>\n'
        )
        body += (
            f'  <text x="{cx + 14}" y="{cy + 98}" font-family="{SANS_FONT}" font-size="12" '
            f'fill="{sub_c}">{esc(c["sub"])}</text>\n'
        )

    fy = 286
    for idx, (ic, val, lbl) in enumerate(minis):
        vw = approx_text_width(val, 20, bold=True)
        body += (
            f'  <rect x="21" y="{fy + 3}" width="{W - 38}" height="42" rx="10" fill="{ink}"/>\n'
            f'  <rect x="18" y="{fy}" width="{W - 38}" height="42" rx="10" '
            f'fill="{mini_fills[idx]}" stroke="{ink}" stroke-width="2"/>\n'
        )
        body += badge_cartoon_icon(ic, 32, fy + 11, 20, t)
        body += (
            f'  <text x="62" y="{fy + 27.5}" font-family="{SANS_FONT}" font-size="20" '
            f'font-weight="800" fill="{val_c}">{esc(val)}</text>\n'
        )
        body += (
            f'  <text x="{70 + vw:.1f}" y="{fy + 26.5}" font-family="{MONO_FONT}" font-size="12.5" '
            f'fill="{sub_c}">{esc(lbl)}</text>\n'
        )
        fy += 50

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
    """Uniform, balanced 2x2 project cards with anchored flat-shaded cartoon illustration tile."""
    pid = proj["id"]
    overline = proj["overline"]
    if stars > 0:
        overline = f"{overline} · ★ {stars}"

    W, H = 432, 210
    body = surface_frame(W, H, t, radius=12, fill_key="paper")

    # Plain gold overline + corner arrow
    body += (
        f'  <text x="22" y="34" font-family="{MONO_FONT}" font-size="11" font-weight="700" '
        f'letter-spacing="0.9" fill="{t["secondary"]}">{esc(overline)}</text>\n'
    )
    body += badge_cartoon_icon("arrow_ne", W - 36, 20, 16, t)

    # Anchored illustration tile on right
    tx, ty, ts = W - 118, 52, 96
    body += (
        f'  <rect x="{tx}" y="{ty}" width="{ts}" height="{ts}" rx="12" '
        f'fill="{t["bg"]}" stroke="{t["divider"]}" stroke-width="1"/>\n'
    )
    body += project_flat_illustration(pid, tx + 10, ty + 10, 76, t)

    # Title + 3-line wrapped description on left (guaranteed clear of tile)
    body += (
        f'  <text x="22" y="64" font-family="{SANS_FONT}" font-size="19" font-weight="700" '
        f'letter-spacing="-0.3" fill="{t["text"]}">{esc(proj["name"])}</text>\n'
    )
    for idx, ln in enumerate(_wrap_text(proj["line"], 35)[:3]):
        body += (
            f'  <text x="22" y="{90 + idx * 19}" font-family="{SANS_FONT}" font-size="13" '
            f'fill="{t["muted"]}">{esc(ln)}</text>\n'
        )

    # Clean neutral tech chips along bottom
    px, py = 22, H - 44
    for tech in proj["chips"]:
        c_svg, cw = chip(px, py, tech, t, font_size=11.5, height=24, pad_x=9, mono=True)
        if px + cw > W - 20:
            break
        body += c_svg
        px += cw + 6

    return svg_doc(W, H, "", body, title=proj["name"])
