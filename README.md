# Shelfie — Personal Media Dashboard

An interactive dashboard for my personal media log (2020–2026), tracking everything I've finished across TV shows, movies, games, books, comics, and more.

**Live:** https://shelfie-one-topaz.vercel.app/

## Stats
- **752** items finished across 7 years (2020–2026)
- 📺 392 TV Shows · 🎬 168 Movies · 🎮 107 Games · 📖 61 Books · 📱 22 Comics · 🎧 2 Audiobooks

## Features
- **Overview** — Summary stats, type & year breakdowns, activity heatmap
- **Timeline** — Monthly bar chart per year, filterable by media type
- **Browse & Search** — Full-text search + filter by type, year, and star rating
- **Year Wrap-ups** — Per-year summary cards with highlights and 5-star picks

## Stack
- Pure HTML + vanilla JS (no framework)
- Tailwind CSS (via gstatic CDN)
- All data embedded inline — no server required

## Data
- `shelfie_data.json` — 752 structured entries parsed from calendar log
- `parse_log.py` — Parser script to regenerate JSON from the source `.txt` log

## Updating
Re-run `parse_log.py` against an updated log file, then re-inject the JSON into `index.html` with:
```bash
python parse_log.py
```
