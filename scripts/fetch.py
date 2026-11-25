"""Fetch live GitHub profile stats and contribution calendars using stdlib only."""

from __future__ import annotations

import datetime as dt
import json
import os
import subprocess
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
STATE_PATH = ROOT / "scripts" / "state.json"


def _get_token() -> str:
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN") or ""
    if token:
        return token.strip()
    try:
        out = subprocess.check_output(
            ["gh", "auth", "token"], stderr=subprocess.DEVNULL, text=True
        )
        return out.strip()
    except Exception:
        return ""


def _graphql(query: str, variables: dict[str, Any], token: str) -> dict[str, Any]:
    body = json.dumps({"query": query, "variables": variables}).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "SuperHuyGaming-Profile-Builder",
        "Accept": "application/vnd.github+json",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(
        "https://api.github.com/graphql", data=body, headers=headers, method="POST"
    )
    with urllib.request.urlopen(req, timeout=25) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    if "errors" in payload:
        raise RuntimeError(f"GraphQL error: {payload['errors']}")
    return payload["data"]


def _fetch_calendar_range(
    login: str, start_iso: str, end_iso: str, token: str
) -> dict[str, Any]:
    query = """
    query($login: String!, $from: DateTime!, $to: DateTime!) {
      user(login: $login) {
        contributionsCollection(from: $from, to: $to) {
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                date
                contributionCount
              }
            }
          }
        }
      }
    }
    """
    data = _graphql(
        query, {"login": login, "from": start_iso, "to": end_iso}, token
    )
    cal = data["user"]["contributionsCollection"]["contributionCalendar"]
    days: list[dict[str, Any]] = []
    for week in cal["weeks"]:
        for d in week["contributionDays"]:
            days.append({"date": d["date"], "count": int(d["contributionCount"])})
    return {"total": int(cal["totalContributions"]), "days": days}


def _compute_streaks(all_days: list[dict[str, Any]], today: dt.date) -> dict[str, Any]:
    by_date: dict[dt.date, int] = {}
    for item in all_days:
        d = dt.date.fromisoformat(item["date"])
        by_date[d] = max(by_date.get(d, 0), int(item["count"]))

    if not by_date:
        return {
            "current_streak": 0,
            "current_streak_start": None,
            "longest_streak": 0,
        }

    # Longest streak across all fetched days
    sorted_dates = sorted(by_date.keys())
    longest = 0
    run = 0
    prev_date: dt.date | None = None
    for d in sorted_dates:
        if d > today:
            continue
        if by_date[d] > 0:
            if prev_date is not None and (d - prev_date).days == 1:
                run += 1
            else:
                run = 1
            if run > longest:
                longest = run
        else:
            run = 0
        prev_date = d

    # Current streak: allow today to be 0 if user hasn't committed yet today
    cursor = today
    if by_date.get(cursor, 0) == 0:
        cursor = today - dt.timedelta(days=1)

    current = 0
    start_date: dt.date | None = None
    while by_date.get(cursor, 0) > 0:
        current += 1
        start_date = cursor
        cursor -= dt.timedelta(days=1)

    return {
        "current_streak": current,
        "current_streak_start": start_date.isoformat() if start_date else None,
        "longest_streak": longest,
    }


def fetch_profile_stats(profile: dict[str, Any]) -> dict[str, Any]:
    login = profile["user"]
    token = _get_token()
    if not token:
        if STATE_PATH.exists():
            return json.loads(STATE_PATH.read_text(encoding="utf-8"))
        raise RuntimeError(
            "No GITHUB_TOKEN found and no cached scripts/state.json available."
        )

    today = dt.datetime.now(dt.timezone.utc).date()
    overview_query = """
    query($login: String!) {
      user(login: $login) {
        createdAt
        followers { totalCount }
        repositories(first: 100, ownerAffiliations: OWNER, privacy: PUBLIC) {
          totalCount
          nodes {
            name
            stargazerCount
            isFork
          }
        }
        contributionsCollection {
          contributionYears
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                date
                contributionCount
              }
            }
          }
        }
      }
    }
    """
    data = _graphql(overview_query, {"login": login}, token)
    user = data["user"]

    repos = user["repositories"]["nodes"]
    public_repos = int(user["repositories"]["totalCount"])
    stars_total = sum(int(r["stargazerCount"]) for r in repos)
    repo_stars = {r["name"]: int(r["stargazerCount"]) for r in repos}
    followers = int(user["followers"]["totalCount"])
    created_year = int(user["createdAt"][:4])

    # Default 12-month rolling calendar
    cal_12m_raw = user["contributionsCollection"]["contributionCalendar"]
    days_12m: list[dict[str, Any]] = []
    for week in cal_12m_raw["weeks"]:
        for d in week["contributionDays"]:
            days_12m.append({"date": d["date"], "count": int(d["contributionCount"])})
    last_year_total = int(cal_12m_raw["totalContributions"])
    active_days_year = sum(1 for d in days_12m if d["count"] > 0)

    # Last 6 months slice (~26 weeks ending today)
    cutoff_6m = today - dt.timedelta(days=182)
    days_6m = [
        d for d in days_12m if dt.date.fromisoformat(d["date"]) >= cutoff_6m
    ]
    total_6m = sum(d["count"] for d in days_6m)

    # Per-year calendars for all-time total & collapsible yearly graphs
    years = sorted(
        set(user["contributionsCollection"]["contributionYears"] + [today.year]),
        reverse=True,
    )
    yearly: dict[str, dict[str, Any]] = {}
    all_days: list[dict[str, Any]] = []
    all_time_total = 0

    for yr in years:
        start_iso = f"{yr}-01-01T00:00:00Z"
        end_iso = (
            f"{today.isoformat()}T23:59:59Z"
            if yr == today.year
            else f"{yr}-12-31T23:59:59Z"
        )
        cal = _fetch_calendar_range(login, start_iso, end_iso, token)
        yearly[str(yr)] = cal
        all_time_total += cal["total"]
        all_days.extend(cal["days"])

    streaks = _compute_streaks(all_days + days_12m, today)

    state = {
        "fetched_at": today.isoformat(),
        "user": login,
        "created_year": created_year,
        "public_repos": public_repos,
        "stars_earned": stars_total,
        "followers": followers,
        "active_days_year": active_days_year,
        "last_year_contributions": last_year_total,
        "all_time_contributions": all_time_total,
        "current_streak": streaks["current_streak"],
        "current_streak_start": streaks["current_streak_start"],
        "longest_streak": streaks["longest_streak"],
        "repo_stars": repo_stars,
        "calendar_6m": {"total": total_6m, "days": days_6m},
        "calendar_12m": {"total": last_year_total, "days": days_12m},
        "yearly": yearly,
    }

    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    return state
