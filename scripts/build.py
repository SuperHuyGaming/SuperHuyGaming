"""Build all profile SVG cards and README.md from profile.json and live GitHub stats."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from cards import (
    render_badge,
    render_github_stats,
    render_heatmap,
    render_hero,
    render_project_card,
    render_section_header,
)
from fetch import fetch_profile_stats
from svgkit import esc


ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
PROFILE_PATH = ROOT / "profile.json"
TOKENS_PATH = ROOT / "scripts" / "tokens.json"
README_PATH = ROOT / "README.md"


def _picture(stem: str, alt: str, width: str = "100%", has_phone: bool = True, height: str | None = None) -> str:
    size_attr = f'height="{height}"' if height else f'width="{width}"'
    sources = []
    if has_phone:
        sources.append(f'<source media="(prefers-color-scheme: dark) and (max-width: 600px)" srcset="assets/{stem}-phone-dark.svg">')
        sources.append(f'<source media="(max-width: 600px)" srcset="assets/{stem}-phone-light.svg">')
    sources.append(f'<source media="(prefers-color-scheme: dark)" srcset="assets/{stem}-dark.svg">')
    img = f'<img src="assets/{stem}-light.svg" {size_attr} alt="{esc(alt)}">'
    return "<picture>" + "".join(sources) + img + "</picture>"


def _write_svg(name: str, content: str) -> None:
    (ASSETS / name).write_text(content, encoding="utf-8")


def build() -> None:
    profile: dict[str, Any] = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    tokens: dict[str, dict[str, str]] = json.loads(TOKENS_PATH.read_text(encoding="utf-8"))
    state = fetch_profile_stats(profile)

    ASSETS.mkdir(parents=True, exist_ok=True)
    # Remove any stale SVG files from earlier designs
    for old in ASSETS.glob("*.svg"):
        old.unlink()

    for theme in ("light", "dark"):
        t = tokens[theme]
        _write_svg(f"hero-{theme}.svg", render_hero(profile, t, theme, phone=False))
        _write_svg(f"hero-phone-{theme}.svg", render_hero(profile, t, theme, phone=True))

        for link in profile["links"]:
            _write_svg(f"badge-{link['id']}-{theme}.svg", render_badge(link, t))

        _write_svg(f"label-activity-{theme}.svg", render_section_header("01", "Activity", "redrawn nightly via GitHub Actions", t, phone=False))
        _write_svg(f"label-activity-phone-{theme}.svg", render_section_header("01", "Activity", "", t, phone=True))

        _write_svg(f"github-{theme}.svg", render_github_stats(state, t, theme, phone=False))
        _write_svg(f"github-phone-{theme}.svg", render_github_stats(state, t, theme, phone=True))

        cal6 = state["calendar_6m"]
        _write_svg(
            f"graph-6m-{theme}.svg",
            render_heatmap(cal6["days"], cal6["total"], "contributions in the last 6 months", t, theme, "6m", show_numbers=True, phone=False),
        )
        _write_svg(
            f"graph-6m-phone-{theme}.svg",
            render_heatmap(cal6["days"], cal6["total"], "contributions in the last 6 months", t, theme, "6m", show_numbers=True, phone=True),
        )

        cal12 = state["calendar_12m"]
        _write_svg(
            f"graph-12m-{theme}.svg",
            render_heatmap(cal12["days"], cal12["total"], "contributions in the last 12 months", t, theme, "12m", show_numbers=False, phone=False),
        )
        _write_svg(
            f"graph-12m-phone-{theme}.svg",
            render_heatmap(cal12["days"], cal12["total"], "contributions in the last 12 months", t, theme, "12m", show_numbers=True, phone=True),
        )

        for yr, cal in state["yearly"].items():
            _write_svg(
                f"graph-{yr}-{theme}.svg",
                render_heatmap(cal["days"], cal["total"], f"contributions in {yr}", t, theme, yr, show_numbers=False, phone=False),
            )
            _write_svg(
                f"graph-{yr}-phone-{theme}.svg",
                render_heatmap(cal["days"], cal["total"], f"contributions in {yr}", t, theme, yr, show_numbers=False, phone=True),
            )

        _write_svg(f"label-work-{theme}.svg", render_section_header("02", "Work", "featured full-stack & AI projects", t, phone=False))
        _write_svg(f"label-work-phone-{theme}.svg", render_section_header("02", "Work", "", t, phone=True))

        repo_stars = state.get("repo_stars", {})
        for proj in profile["projects"]:
            stars = int(repo_stars.get(proj["repo"], 0))
            _write_svg(f"project-{proj['id']}-{theme}.svg", render_project_card(proj, stars, t, theme, phone=False))
            _write_svg(f"project-{proj['id']}-phone-{theme}.svg", render_project_card(proj, stars, t, theme, phone=True))

    blocks: list[str] = []

    hero_pic = _picture("hero", f"{profile['display_name']} — {profile['title']}. {profile['tagline']}")
    blocks.append(f'<a href="{profile["domain_url"]}">{hero_pic}</a>')

    badge_lines = ['<p align="center">']
    for link in profile["links"]:
        b_pic = _picture(f"badge-{link['id']}", link["label"], has_phone=False, height="38")
        badge_lines.append(f'<a href="{link["url"]}">{b_pic}</a>')
    badge_lines.append("</p>")
    blocks.append("\n".join(badge_lines))

    blocks.append(_picture("label-activity", "01 Activity"))

    gh_alt = (
        f"GitHub activity: {state['last_year_contributions']:,} contributions in the last year, "
        f"{state['current_streak']}-day current streak, {state['longest_streak']}-day longest streak, "
        f"{state['all_time_contributions']:,} contributions since {state['created_year']}, "
        f"{state['public_repos']} public repos, {state['stars_earned']} stars earned."
    )
    blocks.append(_picture("github", gh_alt))
    blocks.append(_picture("graph-6m", f"{state['calendar_6m']['total']:,} contributions in the last 6 months"))

    alt_12m = f"{state['calendar_12m']['total']:,} contributions in the last 12 months"
    blocks.append(
        f"<details><summary>Last 12 months: {state['calendar_12m']['total']:,} contributions</summary>\n\n"
        f"{_picture('graph-12m', alt_12m)}\n\n"
        f"</details>"
    )
    for yr in sorted(state["yearly"].keys(), reverse=True):
        yr_tot = state["yearly"][yr]["total"]
        yr_alt = f"{yr_tot:,} contributions in {yr}"
        blocks.append(
            f"<details><summary>{yr}: {yr_tot:,} contributions</summary>\n\n"
            f"{_picture(f'graph-{yr}', yr_alt)}\n\n"
            f"</details>"
        )

    blocks.append(_picture("label-work", "02 Work"))
    proj_lines = ['<p align="center">']
    for proj in profile["projects"]:
        p_pic = _picture(f"project-{proj['id']}", f"{proj['name']}: {proj['line']}", width="49%")
        proj_lines.append(f'<a href="{proj["url"]}">{p_pic}</a>')
    proj_lines.append("</p>")
    blocks.append("\n".join(proj_lines))

    live_links = " · ".join(
        f'<a href="{p["live"]}">{esc(p["name"])} (Live)</a>'
        for p in profile["projects"]
        if p.get("live")
    )
    more_links = " · ".join(f'<a href="{m["url"]}">{esc(m["name"])}</a>' for m in profile["more"])
    blocks.append(
        f'<p align="center"><sub>Live apps: {live_links}<br>'
        f'More work: {more_links}</sub></p>'
    )
    blocks.append(
        f'<p align="center"><sub>Styled after <a href="{profile["domain_url"]}">{esc(profile["domain"])}</a> · '
        f'redrawn every night by GitHub Actions</sub></p>'
    )

    README_PATH.write_text("\n\n".join(blocks) + "\n", encoding="utf-8")
    print(f"Built {len(list(ASSETS.glob('*.svg')))} SVG assets and README.md for {profile['user']}.")


if __name__ == "__main__":
    build()
