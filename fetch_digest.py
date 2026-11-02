"""Fetch today's top Hacker News stories and save them as a Markdown digest."""
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

API = "https://hacker-news.firebaseio.com/v0"
TOP_N = 15


def get(url):
    with urllib.request.urlopen(url, timeout=20) as resp:
        return json.load(resp)


def main():
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    ids = get(f"{API}/topstories.json")[:TOP_N]
    stories = [get(f"{API}/item/{i}.json") for i in ids]

    lines = [f"# Tech digest: {today}", "", "| # | Story | Points | Comments |", "|---|---|---|---|"]
    for n, s in enumerate(stories, 1):
        if not s:
            continue
        url = s.get("url") or f"https://news.ycombinator.com/item?id={s['id']}"
        title = s.get("title", "").replace("|", "\\|")
        discuss = f"[{s.get('descendants', 0)}](https://news.ycombinator.com/item?id={s['id']})"
        lines.append(f"| {n} | [{title}]({url}) | {s.get('score', 0)} | {discuss} |")

    year, month, _ = today.split("-")
    out = Path("digest") / year / month / f"{today}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n")

    # Keep the README pointing at the latest digest.
    readme = Path("README.md")
    marker = "<!-- latest -->"
    text = readme.read_text()
    head = text.split(marker)[0]
    readme.write_text(f"{head}{marker}\n**Latest:** [{today}]({out.as_posix()})\n")


if __name__ == "__main__":
    main()
