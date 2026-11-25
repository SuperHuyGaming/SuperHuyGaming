"""Render all dark/light and desktop/phone SVG cards for the GitHub profile."""

from __future__ import annotations

import datetime as dt
from typing import Any

from svgkit import (
    DISPLAY_FONT,
    MONO_FONT,
    approx_text_width,
    board_frame,
    dot_grid_defs,
    esc,
    icon_svg,
    pill,
    sticker_rect,
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
        return "start today!"
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
    defs = dot_grid_defs(pid, t["dot"], step=24, r=1.4, opacity=0.45)

    if not phone:
        W, H = 880, 222
        body = board_frame(W, H, t, pid)

        # Monogram sticker on the left with dual-layer orange + ink offset
        mx, my, ms = 36, 42, 74
        body += f'  <rect x="{mx + 6}" y="{my + 6}" width="{ms}" height="{ms}" rx="18" fill="{t["pop"]}" stroke="{t["line"]}" stroke-width="2"/>\n'
        body += sticker_rect(mx, my, ms, ms, "#fbf6ee", t["line"], rx=18, shadow=0, stroke_w=2.5)
        body += (
            f'  <text x="{mx + ms / 2:.1f}" y="{my + 52:.1f}" text-anchor="middle" '
            f'font-family="{DISPLAY_FONT}" font-size="46" font-weight="800" fill="#22201c">'
            f'{esc(profile["monogram"])}</text>\n'
        )

        # Headline: Hi, I'm [Huy]
        hx, hy = 138, 86
        body += (
            f'  <text x="{hx}" y="{hy}" font-family="{DISPLAY_FONT}" font-size="44" '
            f'font-weight="800" letter-spacing="-0.8" fill="{t["text"]}">Hi, I&#x27;m</text>\n'
        )
        name_text = profile["display_name"]
        name_w = round(approx_text_width(name_text, 42, bold=True) + 34)
        nx, ny = hx + 150, 42
        body += sticker_rect(nx, ny, name_w, 56, t["yt"], t["line"], rx=13, shadow=4, stroke_w=2)
        body += (
            f'  <text x="{nx + name_w / 2:.1f}" y="{ny + 42:.1f}" text-anchor="middle" '
            f'font-family="{DISPLAY_FONT}" font-size="42" font-weight="800" '
            f'fill="{t["text"]}">{esc(name_text)}</text>\n'
        )

        # Tilted domain sticker top-right
        dom = profile["domain"]
        dw = round(approx_text_width(dom, 15, mono=True, bold=True) + 28)
        dx, dy = W - dw - 34, 30
        body += f'  <g transform="rotate(4 {dx + dw / 2:.1f} {dy + 19:.1f})">\n'
        body += sticker_rect(dx, dy, dw, 38, t["pop"], t["line"], rx=10, shadow=3.5, stroke_w=2)
        body += (
            f'    <text x="{dx + dw / 2:.1f}" y="{dy + 24:.1f}" text-anchor="middle" '
            f'font-family="{MONO_FONT}" font-size="15" font-weight="700" '
            f'fill="{t["on_pop"]}">{esc(dom)}</text>\n'
        )
        body += "  </g>\n"

        # Tagline
        body += (
            f'  <text x="{hx}" y="128" font-family="{DISPLAY_FONT}" font-size="16.5" '
            f'font-weight="500" fill="{t["muted"]}">{esc(profile["tagline"])}</text>\n'
        )

        # 4 colored tag pills
        px = hx
        py = 152
        for tag in profile["tags"]:
            p_svg, pw = pill(
                px, py, tag["label"], t[tag["tint"]], t["text"], t["line"],
                font_size=13, height=30, pad_x=13, rx=8, shadow=2.5, bold=True
            )
            body += p_svg
            px += pw + 12

        return svg_doc(W, H, defs, body, title=f"Hi, I'm {profile['display_name']}")

    # Phone layout
    W, H = 440, 290
    body = board_frame(W, H, t, pid)

    mx, my, ms = 24, 24, 56
    body += f'  <rect x="{mx + 5}" y="{my + 5}" width="{ms}" height="{ms}" rx="14" fill="{t["pop"]}" stroke="{t["line"]}" stroke-width="2"/>\n'
    body += sticker_rect(mx, my, ms, ms, "#fbf6ee", t["line"], rx=14, shadow=0, stroke_w=2.2)
    body += (
        f'  <text x="{mx + ms / 2:.1f}" y="{my + 40:.1f}" text-anchor="middle" '
        f'font-family="{DISPLAY_FONT}" font-size="34" font-weight="800" fill="#22201c">'
        f'{esc(profile["monogram"])}</text>\n'
    )

    # Domain badge top-right
    dom = profile["domain"]
    dw = round(approx_text_width(dom, 13, mono=True, bold=True) + 22)
    dx, dy = W - dw - 24, 30
    body += f'  <g transform="rotate(3 {dx + dw / 2:.1f} {dy + 16:.1f})">\n'
    body += sticker_rect(dx, dy, dw, 32, t["pop"], t["line"], rx=9, shadow=3, stroke_w=1.8)
    body += (
        f'    <text x="{dx + dw / 2:.1f}" y="{dy + 21:.1f}" text-anchor="middle" '
        f'font-family="{MONO_FONT}" font-size="13" font-weight="700" '
        f'fill="{t["on_pop"]}">{esc(dom)}</text>\n'
    )
    body += "  </g>\n"

    # Headline
    body += (
        f'  <text x="24" y="130" font-family="{DISPLAY_FONT}" font-size="36" '
        f'font-weight="800" fill="{t["text"]}">Hi, I&#x27;m</text>\n'
    )
    name_text = profile["display_name"]
    name_w = round(approx_text_width(name_text, 34, bold=True) + 26)
    body += sticker_rect(146, 94, name_w, 46, t["yt"], t["line"], rx=11, shadow=3.5, stroke_w=2)
    body += (
        f'  <text x="{146 + name_w / 2:.1f}" y="128" text-anchor="middle" '
        f'font-family="{DISPLAY_FONT}" font-size="34" font-weight="800" '
        f'fill="{t["text"]}">{esc(name_text)}</text>\n'
    )

    # Wrapped tagline
    lines = _wrap_text(profile["tagline"], 42)
    for idx, line in enumerate(lines[:2]):
        body += (
            f'  <text x="24" y="{166 + idx * 22}" font-family="{DISPLAY_FONT}" '
            f'font-size="15" font-weight="500" fill="{t["muted"]}">{esc(line)}</text>\n'
        )

    # Tags (2 rows)
    px, py = 24, 210
    for tag in profile["tags"]:
        p_svg, pw = pill(
            px, py, tag["label"], t[tag["tint"]], t["text"], t["line"],
            font_size=12.5, height=28, pad_x=11, rx=8, shadow=2, bold=True
        )
        if px + pw > W - 20:
            px = 24
            py += 36
            p_svg, pw = pill(
                px, py, tag["label"], t[tag["tint"]], t["text"], t["line"],
                font_size=12.5, height=28, pad_x=11, rx=8, shadow=2, bold=True
            )
        body += p_svg
        px += pw + 10

    return svg_doc(W, H, defs, body, title=f"Hi, I'm {profile['display_name']}")


def render_badge(link: dict[str, Any], t: dict[str, str]) -> str:
    label = link["label"]
    handle = link.get("handle", "")
    icon = link.get("icon", "globe")
    fill = t[link["tint"]]

    lw = approx_text_width(label, 14, bold=True)
    hw = approx_text_width(handle, 12.5, mono=True) + 10 if handle else 0
    W = round(20 + 18 + 8 + lw + hw + 18)
    H = 44

    body = sticker_rect(2, 2, W - 7, H - 7, fill, t["line"], rx=10, shadow=3.5, stroke_w=1.8)
    body += icon_svg(icon, 14, 11, 18, t["text"], accent=t["pop"])
    tx = 39
    body += (
        f'  <text x="{tx}" y="25.5" font-family="{DISPLAY_FONT}" font-size="14" '
        f'font-weight="700" fill="{t["text"]}">{esc(label)}</text>\n'
    )
    if handle:
        hx = tx + lw + 8
        body += (
            f'  <text x="{hx:.1f}" y="25" font-family="{MONO_FONT}" font-size="12.5" '
            f'font-weight="500" fill="{t["muted"]}">{esc(handle)}</text>\n'
        )
    return svg_doc(W, H, "", body, title=f"{label} {handle}".strip())


def render_github_stats(state: dict[str, Any], t: dict[str, str], theme: str, phone: bool = False) -> str:
    pid = f"gh-dots-{theme}-{'p' if phone else 'd'}"
    defs = dot_grid_defs(pid, t["dot"], step=24, r=1.4, opacity=0.45)

    cur_streak = state["current_streak"]
    cur_label = f"{cur_streak} day" if cur_streak == 1 else f"{cur_streak} days"
    cur_sub = _fmt_short_date(state["current_streak_start"]) if cur_streak > 0 else "building momentum"

    long_streak = state["longest_streak"]
    long_label = f"{long_streak} day" if long_streak == 1 else f"{long_streak} days"

    big_cards = [
        {
            "value": _fmt_num(state["last_year_contributions"]),
            "line1": "contributions in",
            "line2": "the last year",
            "tint": "lx",
            "icon": "calendar",
        },
        {
            "value": cur_label,
            "line1": "current streak,",
            "line2": cur_sub,
            "tint": "li",
            "icon": "flame",
        },
        {
            "value": long_label,
            "line1": "longest streak",
            "line2": "ever",
            "tint": "rd",
            "icon": "trophy",
        },
        {
            "value": _fmt_num(state["all_time_contributions"]),
            "line1": "contributions",
            "line2": f"since {state['created_year']}",
            "tint": "x",
            "icon": "bars",
        },
    ]

    small_pills = [
        {"value": _fmt_num(state["public_repos"]), "label": "public repos", "tint": "bd", "icon": "folder"},
        {"value": _fmt_num(state["stars_earned"]), "label": "stars earned", "tint": "yt", "icon": "star"},
        {"value": _fmt_num(state["active_days_year"]), "label": "active days (1y)", "tint": "li", "icon": "bolt"},
    ]

    updated = f"redrawn every night · {_fmt_date(state['fetched_at'])}"

    if not phone:
        W, H = 880, 316
        body = board_frame(W, H, t, pid)

        body += (
            f'  <text x="28" y="44" font-family="{DISPLAY_FONT}" font-size="24" '
            f'font-weight="800" fill="{t["text"]}">On GitHub</text>\n'
        )
        body += (
            f'  <text x="{W - 28}" y="42" text-anchor="end" font-family="{MONO_FONT}" '
            f'font-size="13" fill="{t["muted"]}">{esc(updated)}</text>\n'
        )

        # 4 big cards in one row
        gap = 16
        cw = (W - 56 - gap * 3) / 4
        ch = 152
        cy = 64
        for idx, c in enumerate(big_cards):
            cx = 28 + idx * (cw + gap)
            body += sticker_rect(cx, cy, cw, ch, t[c["tint"]], t["line"], rx=16, shadow=4, stroke_w=2)
            body += icon_svg(c["icon"], cx + cw - 36, cy + 14, 22, t["line"], accent=t["pop"])
            body += (
                f'  <text x="{cx + 18:.1f}" y="{cy + 78:.1f}" font-family="{DISPLAY_FONT}" '
                f'font-size="34" font-weight="800" letter-spacing="-0.6" '
                f'fill="{t["text"]}">{esc(c["value"])}</text>\n'
            )
            body += (
                f'  <text x="{cx + 18:.1f}" y="{cy + 106:.1f}" font-family="{MONO_FONT}" '
                f'font-size="13.5" fill="{t["muted"]}">{esc(c["line1"])}</text>\n'
            )
            body += (
                f'  <text x="{cx + 18:.1f}" y="{cy + 126:.1f}" font-family="{MONO_FONT}" '
                f'font-size="13.5" fill="{t["muted"]}">{esc(c["line2"])}</text>\n'
            )

        # 3 small pills below
        py = 236
        ph = 52
        pw_list = [235, 235, 322]
        px = 28
        for idx, sp in enumerate(small_pills):
            pw = pw_list[idx]
            body += sticker_rect(px, py, pw, ph, t[sp["tint"]], t["line"], rx=14, shadow=3.5, stroke_w=2)
            body += icon_svg(sp["icon"], px + 16, py + 15, 22, t["line"], accent=t["pop"])
            val_w = approx_text_width(sp["value"], 23, bold=True)
            body += (
                f'  <text x="{px + 48}" y="{py + 34}" font-family="{DISPLAY_FONT}" '
                f'font-size="24" font-weight="800" fill="{t["text"]}">{esc(sp["value"])}</text>\n'
            )
            body += (
                f'  <text x="{px + 56 + val_w:.1f}" y="{py + 32}" font-family="{MONO_FONT}" '
                f'font-size="14" fill="{t["muted"]}">{esc(sp["label"])}</text>\n'
            )
            px += pw + 16

        return svg_doc(W, H, defs, body, title="On GitHub stats")

    # Phone layout (2x2 grid + 3 stacked pills)
    W, H = 440, 560
    body = board_frame(W, H, t, pid)
    body += (
        f'  <text x="22" y="40" font-family="{DISPLAY_FONT}" font-size="22" '
        f'font-weight="800" fill="{t["text"]}">On GitHub</text>\n'
    )
    body += (
        f'  <text x="22" y="60" font-family="{MONO_FONT}" font-size="12" '
        f'fill="{t["muted"]}">{esc(updated)}</text>\n'
    )

    cw = 190
    ch = 132
    for idx, c in enumerate(big_cards):
        col = idx % 2
        row = idx // 2
        cx = 22 + col * (cw + 16)
        cy = 78 + row * (ch + 16)
        body += sticker_rect(cx, cy, cw, ch, t[c["tint"]], t["line"], rx=14, shadow=3.5, stroke_w=2)
        body += icon_svg(c["icon"], cx + cw - 32, cy + 12, 20, t["line"], accent=t["pop"])
        body += (
            f'  <text x="{cx + 14}" y="{cy + 66}" font-family="{DISPLAY_FONT}" '
            f'font-size="28" font-weight="800" fill="{t["text"]}">{esc(c["value"])}</text>\n'
        )
        body += (
            f'  <text x="{cx + 14}" y="{cy + 92}" font-family="{MONO_FONT}" '
            f'font-size="12.5" fill="{t["muted"]}">{esc(c["line1"])}</text>\n'
        )
        body += (
            f'  <text x="{cx + 14}" y="{cy + 110}" font-family="{MONO_FONT}" '
            f'font-size="12.5" fill="{t["muted"]}">{esc(c["line2"])}</text>\n'
        )

    py = 382
    for sp in small_pills:
        body += sticker_rect(22, py, W - 44, 46, t[sp["tint"]], t["line"], rx=12, shadow=3, stroke_w=1.8)
        body += icon_svg(sp["icon"], 36, py + 13, 20, t["line"], accent=t["pop"])
        val_w = approx_text_width(sp["value"], 20, bold=True)
        body += (
            f'  <text x="66" y="{py + 30}" font-family="{DISPLAY_FONT}" '
            f'font-size="21" font-weight="800" fill="{t["text"]}">{esc(sp["value"])}</text>\n'
        )
        body += (
            f'  <text x="{74 + val_w:.1f}" y="{py + 29}" font-family="{MONO_FONT}" '
            f'font-size="13.5" fill="{t["muted"]}">{esc(sp["label"])}</text>\n'
        )
        py += 56

    return svg_doc(W, H, defs, body, title="On GitHub stats")


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
    pid = f"hm-dots-{graph_id}-{theme}-{'p' if phone else 'd'}"
    defs = dot_grid_defs(pid, t["dot"], step=24, r=1.4, opacity=0.45)

    # Group days into Sunday-aligned weeks
    sorted_days = sorted(days, key=lambda d: d["date"])
    if not sorted_days:
        W, H = (440, 120) if phone else (880, 120)
        body = board_frame(W, H, t, pid)
        body += (
            f'  <text x="32" y="66" font-family="{DISPLAY_FONT}" font-size="20" '
            f'font-weight="700" fill="{t["muted"]}">0 {esc(subtitle)}</text>\n'
        )
        return svg_doc(W, H, defs, body, title=f"0 {subtitle}")

    # On phone, show at most the last 16 weeks for 6m/12m so cells remain legible
    if phone and len(sorted_days) > 112:
        sorted_days = sorted_days[-112:]
        total = sum(d["count"] for d in sorted_days)
        if "6 months" in subtitle or "12 months" in subtitle:
            subtitle = "contributions in the last 16 weeks"

    first_dt = dt.date.fromisoformat(sorted_days[0]["date"])
    # Sunday = 0 .. Saturday = 6
    lead_pad = (first_dt.weekday() + 1) % 7
    padded: list[dict[str, Any] | None] = [None] * lead_pad + list(sorted_days)
    weeks: list[list[dict[str, Any] | None]] = [
        padded[i : i + 7] for i in range(0, len(padded), 7)
    ]
    n_weeks = len(weeks)
    max_count = max((d["count"] for d in sorted_days), default=0)

    W = 440 if phone else 880
    inner_x = 18 if phone else 26
    inner_y = 18 if phone else 22
    inner_w = W - inner_x * 2

    grid_pad_x = 16 if phone else 22
    avail_w = inner_w - grid_pad_x * 2
    gap = 4 if (show_numbers and n_weeks <= 28) else 2.5
    cell = (avail_w - gap * (n_weeks - 1)) / max(n_weeks, 1)
    cell = min(cell, 26.0)
    grid_w = n_weeks * cell + (n_weeks - 1) * gap
    grid_x = inner_x + (inner_w - grid_w) / 2
    grid_y = inner_y + 74
    grid_h = 7 * cell + 6 * gap
    inner_h = int(grid_y - inner_y + grid_h + 22)
    H = inner_h + inner_y * 2

    body = board_frame(W, H, t, pid)
    body += sticker_rect(inner_x, inner_y, inner_w, inner_h, t["surface"], t["line"], rx=16, shadow=4, stroke_w=1.8)

    # Header total + subtitle
    tot_str = _fmt_num(total)
    tot_size = 19 if phone else 22
    tot_w = approx_text_width(tot_str, tot_size, bold=True)
    body += (
        f'  <text x="{inner_x + grid_pad_x}" y="{inner_y + 34}" font-family="{DISPLAY_FONT}" '
        f'font-size="{tot_size}" font-weight="800" fill="{t["text"]}">{esc(tot_str)}</text>\n'
    )
    body += (
        f'  <text x="{inner_x + grid_pad_x + tot_w + 8:.1f}" y="{inner_y + 33}" '
        f'font-family="{MONO_FONT}" font-size="{11.5 if phone else 14}" '
        f'fill="{t["muted"]}">{esc(subtitle)}</text>\n'
    )

    # Compact legend top-right (desktop)
    if not phone:
        lx = inner_x + inner_w - grid_pad_x - 122
        ly = inner_y + 21
        body += (
            f'  <text x="{lx - 6}" y="{ly + 11}" text-anchor="end" font-family="{MONO_FONT}" '
            f'font-size="11" fill="{t["muted"]}">Less</text>\n'
        )
        for lvl in range(5):
            body += (
                f'  <rect x="{lx + lvl * 16}" y="{ly}" width="12" height="12" rx="3" '
                f'fill="{t[f"cell{lvl}"]}"/>\n'
            )
        body += (
            f'  <text x="{lx + 84}" y="{ly + 11}" font-family="{MONO_FONT}" '
            f'font-size="11" fill="{t["muted"]}">More</text>\n'
        )

    # Month labels across the top of the grid
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
                    f'  <text x="{mx:.1f}" y="{grid_y - 10:.1f}" font-family="{MONO_FONT}" '
                    f'font-size="{11 if phone else 12.5}" fill="{t["muted"]}">'
                    f'{MONTH_NAMES[m - 1]}</text>\n'
                )
                last_label_x = mx
            last_month = m

    # Cells
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
            fill = t[f"cell{lvl}"]
            body += (
                f'  <rect x="{cx:.1f}" y="{cy:.1f}" width="{cell:.1f}" height="{cell:.1f}" '
                f'rx="{rx}" fill="{fill}"/>\n'
            )
            if draw_nums:
                if cnt == 0:
                    tc = t["cell_text_dim"]
                    fs = 9.5
                else:
                    tc = t["cell_text_dark"] if (theme == "dark" and lvl >= 3) or (theme == "light" and lvl >= 3) else t["cell_text_light"]
                    fs = 9.5 if cnt < 100 else 8.0
                body += (
                    f'  <text x="{cx + cell / 2:.1f}" y="{cy + cell / 2 + fs * 0.35:.1f}" '
                    f'text-anchor="middle" font-family="{MONO_FONT}" font-size="{fs}" '
                    f'font-weight="{"700" if cnt > 0 else "400"}" fill="{tc}">{cnt}</text>\n'
                )

    return svg_doc(W, H, defs, body, title=f"{tot_str} {subtitle}")


def render_section_label(title: str, subtitle: str, t: dict[str, str], theme: str, phone: bool = False) -> str:
    pid = f"lbl-dots-{theme}-{'p' if phone else 'd'}"
    defs = dot_grid_defs(pid, t["dot"], step=24, r=1.4, opacity=0.45)
    W = 440 if phone else 880
    H = 68 if phone else 64
    body = board_frame(W, H, t, pid, radius=14)
    body += (
        f'  <text x="24" y="{36 if phone else 40}" font-family="{DISPLAY_FONT}" '
        f'font-size="{20 if phone else 23}" font-weight="800" fill="{t["text"]}">{esc(title)}</text>\n'
    )
    if phone:
        body += (
            f'  <text x="24" y="55" font-family="{MONO_FONT}" font-size="11.5" '
            f'fill="{t["muted"]}">{esc(subtitle)}</text>\n'
        )
    else:
        body += (
            f'  <text x="{W - 24}" y="39" text-anchor="end" font-family="{MONO_FONT}" '
            f'font-size="13" fill="{t["muted"]}">{esc(subtitle)}</text>\n'
        )
    return svg_doc(W, H, defs, body, title=title)


def render_project_card(
    proj: dict[str, Any],
    stars: int,
    t: dict[str, str],
    theme: str,
    phone: bool = False,
) -> str:
    pid = f"proj-{proj['id']}-{theme}-{'p' if phone else 'd'}"
    defs = dot_grid_defs(pid, t["dot"], step=22, r=1.3, opacity=0.4)
    W, H = (432, 224) if not phone else (432, 228)

    body = board_frame(W, H, t, pid, radius=16)
    body += sticker_rect(18, 18, W - 36, H - 36, t["surface"], t["line"], rx=14, shadow=4, stroke_w=1.8)

    # Row 1: Color dot + project name (full width, never collides)
    body += f'  <circle cx="42" cy="48" r="7" fill="{t[proj["tint"]]}" stroke="{t["line"]}" stroke-width="1.8"/>\n'
    body += (
        f'  <text x="58" y="54" font-family="{DISPLAY_FONT}" font-size="19.5" '
        f'font-weight="800" fill="{t["text"]}">{esc(proj["name"])}</text>\n'
    )

    # Row 2: Compact status/metric badge right below title
    badge = proj["badge"]
    if stars > 0 and "★" not in badge:
        badge = f"{badge} · ★ {stars}"
    bw = round(approx_text_width(badge, 11, mono=True, bold=True) + 18)
    bx, by = 36, 66
    body += sticker_rect(bx, by, bw, 23, t[proj["tint"]], t["line"], rx=7, shadow=2, stroke_w=1.4)
    body += (
        f'  <text x="{bx + bw / 2:.1f}" y="{by + 15.5:.1f}" text-anchor="middle" '
        f'font-family="{MONO_FONT}" font-size="11" font-weight="700" '
        f'fill="{t["text"]}">{esc(badge)}</text>\n'
    )

    # Row 3: Description (wrapped 2 lines)
    lines = _wrap_text(proj["line"], 46)
    for idx, ln in enumerate(lines[:2]):
        body += (
            f'  <text x="36" y="{115 + idx * 21}" font-family="{DISPLAY_FONT}" '
            f'font-size="14.5" font-weight="500" fill="{t["muted"]}">{esc(ln)}</text>\n'
        )

    # Row 4: Tech chips along bottom
    px = 36
    py = H - 62
    for label, tint in proj["chips"]:
        c_svg, cw = pill(
            px, py, label, t[tint], t["text"], t["line"],
            font_size=11.5, height=25, pad_x=10, rx=7, shadow=2, mono=True, bold=True
        )
        if px + cw > W - 30:
            break
        body += c_svg
        px += cw + 8

    return svg_doc(W, H, defs, body, title=proj["name"])
