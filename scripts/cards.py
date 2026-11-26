"""Render clean, human-crafted bentruong.dev SVGs with real photo/app previews + flat cartoon icons."""

from __future__ import annotations

import datetime as dt
from typing import Any

from svgkit import (
    MONO_FONT,
    SANS_FONT,
    approx_text_width,
    badge_cartoon_icon,
    blueprint_grid_defs,
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
    if theme == "dark":
        ink = "#06120D"
        chip_fills = ["#1C563F", "#5C451A", "#1B4E56", "#35492A"]
        chip_tc = "#F2F8F5"
        snap_tile = "#172D24"
    else:
        ink = "#13221B"
        chip_fills = ["#CFEAD9", "#F6E5B8", "#CCE8EC", "#DCE9CA"]
        chip_tc = "#102119"
        snap_tile = "#FFFFFF"

    def _tactile_chip(x: float, y: float, label: str, fill: str, ic: str, fs: float = 12, h: float = 31) -> tuple[str, float]:
        tw = approx_text_width(label, fs, bold=True)
        w = round(tw + 20 + 22)
        s = (
            f'  <rect x="{x + 2.5:.1f}" y="{y + 2.5:.1f}" width="{w}" height="{h}" rx="8" fill="{ink}"/>\n'
            f'  <rect x="{x:.1f}" y="{y:.1f}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{ink}" stroke-width="1.8"/>\n'
        )
        from svgkit import mini_cartoon_icon
        s += mini_cartoon_icon(ic, x + 8, y + (h - 16) / 2, 16, t)
        s += (
            f'  <text x="{x + 28 + tw / 2:.1f}" y="{y + h / 2 + fs * 0.35:.1f}" text-anchor="middle" '
            f'font-family="{SANS_FONT}" font-size="{fs}" font-weight="700" fill="{chip_tc}">{esc(label)}</text>\n'
        )
        return s, w

    pid = f"hero-grid-{theme}-{'p' if phone else 'd'}"
    defs = blueprint_grid_defs(pid, t, theme)

    if not phone:
        W, H = 880, 248
        body = surface_frame(W, H, t, radius=16, fill_key="bg", pattern_id=pid, theme=theme)

        # Left editorial column
        body += (
            f'  <text x="36" y="42" font-family="{MONO_FONT}" font-size="11.5" font-weight="700" '
            f'letter-spacing="1.2" fill="{t["secondary"]}">GEORGE MASON CS  ·  BENTRUONG.DEV</text>\n'
        )
        body += (
            f'  <text x="36" y="96" font-family="{SANS_FONT}" font-size="48" font-weight="800" '
            f'letter-spacing="-1.6" fill="{t["text"]}">{esc(profile["display_name"])}</text>\n'
        )
        body += (
            f'  <text x="36" y="128" font-family="{SANS_FONT}" font-size="19" font-weight="700" '
            f'fill="{t["primary"]}">{esc(profile["title"])}</text>\n'
        )
        body += (
            f'  <text x="36" y="156" font-family="{SANS_FONT}" font-size="14.5" '
            f'fill="{t["muted"]}">{esc(profile["tagline"])}</text>\n'
        )

        # 4 tactile botanical focus chips
        cx, cy = 36, 180
        for idx, tag in enumerate(profile["tags"]):
            ic = focus_icons[idx % len(focus_icons)]
            c_svg, cw = _tactile_chip(cx, cy, tag["label"], chip_fills[idx % len(chip_fills)], ic, fs=12, h=31)
            body += c_svg
            cx += cw + 9

        # Crisp vertical divider + tactile right Snapshot column
        dx = 590
        body += f'  <line x1="{dx}" y1="26" x2="{dx}" y2="{H - 26}" stroke="{t["divider"]}" stroke-width="1"/>\n'
        rx = dx + 22
        body += (
            f'  <text x="{rx}" y="41" font-family="{MONO_FONT}" font-size="10.5" font-weight="700" '
            f'letter-spacing="1.1" fill="{t["secondary"]}">SNAPSHOT</text>\n'
        )
        for idx, (icon_name, top_txt, sub_txt) in enumerate(snapshot):
            ry = 58 + idx * 56
            # Tactile mini icon box
            body += (
                f'  <rect x="{rx + 2.5}" y="{ry + 2.5}" width="38" height="38" rx="10" fill="{ink}"/>\n'
                f'  <rect x="{rx}" y="{ry}" width="38" height="38" rx="10" fill="{snap_tile}" stroke="{ink}" stroke-width="1.8"/>\n'
            )
            body += snapshot_cartoon_icon(icon_name, rx + 5, ry + 5, 28, t)
            body += (
                f'  <text x="{rx + 48}" y="{ry + 16}" font-family="{SANS_FONT}" font-size="13.5" '
                f'font-weight="700" fill="{t["text"]}">{esc(top_txt)}</text>\n'
            )
            body += (
                f'  <text x="{rx + 48}" y="{ry + 33}" font-family="{MONO_FONT}" font-size="11.5" '
                f'fill="{t["muted"]}">{esc(sub_txt)}</text>\n'
            )

        return svg_doc(W, H, defs, body, title=f"{profile['display_name']} — {profile['title']}")

    # Phone layout
    W, H = 440, 294
    body = surface_frame(W, H, t, radius=16, fill_key="bg", pattern_id=pid, theme=theme)

    body += (
        f'  <text x="24" y="36" font-family="{MONO_FONT}" font-size="10.5" font-weight="700" '
        f'letter-spacing="1.0" fill="{t["secondary"]}">GEORGE MASON CS · BENTRUONG.DEV</text>\n'
    )
    body += (
        f'  <text x="24" y="82" font-family="{SANS_FONT}" font-size="36" font-weight="800" '
        f'letter-spacing="-1.2" fill="{t["text"]}">{esc(profile["display_name"])}</text>\n'
    )
    body += (
        f'  <text x="24" y="110" font-family="{SANS_FONT}" font-size="17" font-weight="700" '
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
        c_svg, cw = _tactile_chip(cx, cy, tag["label"], chip_fills[idx % len(chip_fills)], ic, fs=12, h=30)
        if cx + cw > W - 20:
            cx = 24
            cy += 39
            c_svg, cw = _tactile_chip(cx, cy, tag["label"], chip_fills[idx % len(chip_fills)], ic, fs=12, h=30)
        body += c_svg
        cx += cw + 8

    return svg_doc(W, H, defs, body, title=f"{profile['display_name']} — {profile['title']}")


def render_badge(link: dict[str, Any], t: dict[str, str], theme: str = "dark") -> str:
    label = link["label"]
    icon = link.get("icon", "globe")
    lid = link["id"]
    is_primary = link.get("variant") == "primary"

    if theme == "dark":
        ink = "#06120D"
        palette = {"site": t["primary"], "resume": "#5C451A", "li": "#1B4E56", "mail": "#1C563F"}
        tc = "#06120D" if is_primary else "#FFFFFF"
    else:
        ink = "#13221B"
        palette = {"site": t["primary"], "resume": "#F6E5B8", "li": "#CCE8EC", "mail": "#CFEAD9"}
        tc = "#FFFFFF" if is_primary else "#102119"

    fill = palette.get(lid, t["paper"])
    lw = approx_text_width(label, 13.5, bold=True)
    W = round(14 + 20 + 8 + lw + 20)
    H = 44

    body = (
        f'  <rect x="4" y="4" width="{W - 7}" height="{H - 7}" rx="10" fill="{ink}"/>\n'
        f'  <rect x="1.5" y="1.5" width="{W - 7}" height="{H - 7}" rx="10" '
        f'fill="{fill}" stroke="{ink}" stroke-width="2"/>\n'
    )
    body += badge_cartoon_icon(icon, 13, 10, 20, t, on_primary=is_primary)
    body += (
        f'  <text x="41" y="25" font-family="{SANS_FONT}" font-size="13.5" '
        f'font-weight="700" fill="{tc}">{esc(label)}</text>\n'
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

    pid = f"gh-grid-{theme}-{'p' if phone else 'd'}"
    defs = blueprint_grid_defs(pid, t, theme)

    if not phone:
        W, H = 880, 244
        body = surface_frame(W, H, t, radius=16, fill_key="bg", pattern_id=pid, theme=theme)

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

        return svg_doc(W, H, defs, body, title="GitHub Activity Stats")

    # Phone layout (2x2 tactile cards + 3 stacked tactile mini-cards)
    W, H = 440, 448
    body = surface_frame(W, H, t, radius=16, fill_key="bg", pattern_id=pid, theme=theme)
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
    outer_pad = 14 if phone else 18
    pad_x = (16 if phone else 22) + outer_pad
    avail_w = W - pad_x * 2
    gap = 4 if (show_numbers and n_weeks <= 28) else 2.5
    cell = min((avail_w - gap * (n_weeks - 1)) / max(n_weeks, 1), 25.0)
    grid_w = n_weeks * cell + (n_weeks - 1) * gap
    grid_x = (W - grid_w) / 2
    grid_y = outer_pad + 72
    grid_h = 7 * cell + 6 * gap
    inner_h = int(72 + grid_h + 22)
    H = inner_h + outer_pad * 2 + 4

    ink = "#06120D" if theme == "dark" else "#13221B"
    pid = f"hm-grid-{graph_id}-{theme}-{'p' if phone else 'd'}"
    defs = blueprint_grid_defs(pid, t, theme)
    body = surface_frame(W, H, t, radius=16, fill_key="bg", pattern_id=pid, theme=theme)
    body += (
        f'  <rect x="{outer_pad + 4}" y="{outer_pad + 4}" width="{W - outer_pad * 2}" height="{inner_h}" '
        f'rx="13" fill="{ink}"/>\n'
        f'  <rect x="{outer_pad}" y="{outer_pad}" width="{W - outer_pad * 2}" height="{inner_h}" '
        f'rx="13" fill="{t["paper"]}" stroke="{ink}" stroke-width="2"/>\n'
    )

    tot_str = _fmt_num(total)
    tot_size = 18 if phone else 22
    tot_w = approx_text_width(tot_str, tot_size, bold=True)
    body += (
        f'  <text x="{pad_x}" y="{outer_pad + 34}" font-family="{SANS_FONT}" font-size="{tot_size}" '
        f'font-weight="800" fill="{t["text"]}">{esc(tot_str)}</text>\n'
    )
    body += (
        f'  <text x="{pad_x + tot_w + 8:.1f}" y="{outer_pad + 33}" font-family="{MONO_FONT}" '
        f'font-size="{11.5 if phone else 13}" fill="{t["muted"]}">{esc(subtitle)}</text>\n'
    )

    if not phone:
        lx = W - pad_x - 118
        ly = outer_pad + 21
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

    return svg_doc(W, H, defs, body, title=f"{tot_str} {subtitle}")


def render_project_card(
    proj: dict[str, Any],
    stars: int,
    t: dict[str, str],
    theme: str,
    phone: bool = False,
) -> str:
    """Tactile Forest-Studio 2x2 project cards (Sketch C) with rich botanical fills & crisp ink offset."""
    pid = proj["id"]
    overline = proj["overline"]
    if stars > 0:
        overline = f"{overline} · ★ {stars}"

    if theme == "dark":
        ink = "#06120D"
        fills = {"badminton": "#194836", "syllabus": "#18424A", "flyer": "#4B3917", "hollow": "#2B3D23"}
        tile_bg = "#0E1E17"
        chip_bg = "#102119"
        title_c = "#FFFFFF"
        desc_c = "#D5E8DE"
        over_c = t["secondary"]
    else:
        ink = "#13221B"
        fills = {"badminton": "#D4ECDD", "syllabus": "#CFE8EC", "flyer": "#F7E8C2", "hollow": "#E0ECD0"}
        tile_bg = "#FFFFFF"
        chip_bg = "#FAFAF7"
        title_c = "#102119"
        desc_c = "#2B4437"
        over_c = "#8A6A1E"

    fill = fills.get(pid, t["paper"])
    W, H = 432, 220
    body = (
        f'  <rect x="6" y="6" width="{W - 10}" height="{H - 10}" rx="15" fill="{ink}"/>\n'
        f'  <rect x="2" y="2" width="{W - 10}" height="{H - 10}" rx="15" fill="{fill}" stroke="{ink}" stroke-width="2.2"/>\n'
    )

    # Gold overline + corner arrow
    body += (
        f'  <text x="22" y="34" font-family="{MONO_FONT}" font-size="11" font-weight="700" '
        f'letter-spacing="0.9" fill="{over_c}">{esc(overline)}</text>\n'
    )
    body += badge_cartoon_icon("arrow_ne", W - 40, 20, 16, t)

    # Tactile anchored illustration tile on right
    tx, ty, ts = W - 122, 50, 96
    body += (
        f'  <rect x="{tx + 3}" y="{ty + 3}" width="{ts}" height="{ts}" rx="13" fill="{ink}"/>\n'
        f'  <rect x="{tx}" y="{ty}" width="{ts}" height="{ts}" rx="13" '
        f'fill="{tile_bg}" stroke="{ink}" stroke-width="2"/>\n'
    )
    body += project_flat_illustration(pid, tx + 10, ty + 10, 76, t)

    # Title + 3-line wrapped description
    body += (
        f'  <text x="22" y="66" font-family="{SANS_FONT}" font-size="20" font-weight="800" '
        f'letter-spacing="-0.4" fill="{title_c}">{esc(proj["name"])}</text>\n'
    )
    for idx, ln in enumerate(_wrap_text(proj["line"], 34)[:3]):
        body += (
            f'  <text x="22" y="{92 + idx * 19}" font-family="{SANS_FONT}" font-size="13" '
            f'fill="{desc_c}">{esc(ln)}</text>\n'
        )

    # Tactile mini tech chips along bottom
    px, py = 22, H - 50
    for tech in proj["chips"]:
        tw = approx_text_width(tech, 11.5, mono=True)
        cw = round(tw + 18)
        if px + cw > W - 24:
            break
        body += (
            f'  <rect x="{px + 2}" y="{py + 2}" width="{cw}" height="24" rx="6" fill="{ink}"/>\n'
            f'  <rect x="{px}" y="{py}" width="{cw}" height="24" rx="6" fill="{chip_bg}" stroke="{ink}" stroke-width="1.5"/>\n'
            f'  <text x="{px + cw / 2:.1f}" y="{py + 16}" text-anchor="middle" font-family="{MONO_FONT}" '
            f'font-size="11.5" font-weight="600" fill="{title_c}">{esc(tech)}</text>\n'
        )
        px += cw + 7

    return svg_doc(W, H, "", body, title=proj["name"])
