
Tech Digest
An automated daily archive of the top 15 stories on Hacker News.

A GitHub Actions workflow runs every morning, pulls the top stories from the Hacker News API, and saves them as a Markdown table in digest/YYYY/MM/YYYY-MM-DD.md. Over time this builds a searchable history of what the tech world was talking about each day.

How it works
scripts/fetch_digest.py: fetches stories and writes the day's file (standard library only)
.github/workflows/daily-commit.yml: runs the script daily at 04:30 UTC and commits the result
Run locally
python scripts/fetch_digest.py

