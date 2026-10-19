#!/usr/bin/env python3
"""Fetch GitHub's public contribution calendar for prithvikings."""
from __future__ import annotations
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path
import requests
from bs4 import BeautifulSoup

USERNAME = os.environ.get("GH_PROFILE_USER", "prithvikings")
URL = f"https://github.com/users/{USERNAME}/contributions"
OUT = Path(__file__).resolve().parent.parent / "data" / "contributions.json"

def fetch_days():
    response = requests.get(URL, headers={"User-Agent": "prithvikings-profile-art/1.0"}, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    cells = soup.select("td.ContributionCalendar-day")
    if not cells:
        raise RuntimeError("No contribution cells found; GitHub may have changed its HTML.")
    days = []
    for cell in cells:
        date = cell.get("data-date")
        if not date:
            continue
        tip_id = cell.get("id")
        tip = soup.find("tool-tip", attrs={"for": tip_id}) if tip_id else None
        label = tip.get_text(" ", strip=True) if tip else ""
        match = re.search(r"(\d[\d,]*)\s+contribution", label, re.I)
        count = int(match.group(1).replace(",", "")) if match else 0
        days.append({"date": date, "count": count, "level": int(cell.get("data-level") or 0)})
    days.sort(key=lambda d: d["date"])
    if not days:
        raise RuntimeError("Contribution calendar contained no dated days.")
    return days

def streaks(days):
    longest = run = 0
    prev = None
    for day in days:
        date = dt.date.fromisoformat(day["date"])
        if day["count"] and (prev is None or (date-prev).days == 1):
            run = run + 1 if prev is not None and (date-prev).days == 1 else 1
        else:
            run = 0
        longest = max(longest, run)
        prev = date
    index = len(days)-1
    if days[index]["date"] == dt.date.today().isoformat() and days[index]["count"] == 0:
        index -= 1
    current = 0
    while index >= 0 and days[index]["count"]:
        current += 1
        index -= 1
    return current, longest

def main():
    days = fetch_days()
    monthly = {}
    for d in days:
        monthly[d["date"][:7]] = monthly.get(d["date"][:7], 0) + d["count"]
    total = sum(d["count"] for d in days)
    active = sum(d["count"] > 0 for d in days)
    best = max(days, key=lambda d: d["count"])
    current, longest = streaks(days)
    payload = {
        "username": USERNAME,
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "range": {"start": days[0]["date"], "end": days[-1]["date"]},
        "total_contributions": total,
        "active_days": active,
        "avg_per_active_day": round(total/active, 1) if active else 0,
        "current_streak": current,
        "longest_streak": longest,
        "best_day": {"date": best["date"], "count": best["count"]},
        "monthly": [{"month": k, "total": v} for k,v in sorted(monthly.items())],
        "days": days,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2)+"\n", encoding="utf-8")
    print(f"Wrote {OUT}: {total} calendar contributions; current streak {current}; longest {longest}.")
if __name__ == "__main__":
    try: main()
    except Exception as exc:
        print(f"Contribution fetch failed: {exc}", file=sys.stderr)
        raise
