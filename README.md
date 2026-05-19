[![RU](https://img.shields.io/badge/lang-RU-blue?style=flat-square)](README.ru.md)

# PeMa — Personal Training Manager

Creative work of students from group RIS-25-1b — Parkhomenko Roman and Mekhonoshin Anton.  
Subject: Development of an automated workplace for a sports trainer.

Desktop application for planning and tracking workouts. A coach creates training plans, athletes execute them and log results.

Built with **Qt 6 / QML** + **Python FastAPI** (backend hosted on Amvera).

---

## Features

- **Calendar** — monthly workout grid, add / edit / delete workouts
- **Roles** — coach creates plans for athletes; athlete sees only their own calendar
- **Analytics** — total distance, pace, streak, weekly / monthly charts, completion rate
- **Goals** — race or volume targets with automatic progress tracking
- **Routes** — generate circular routes by distance, draw freehand on OSM map, edit and export as GPX
- **Watch import** — upload `.gpx` or `.fit` files → HR, distance, pace, elevation fill automatically
- **Strava sync** — OAuth2 connect, imports full activity history
- **Templates** — save and reuse workout structures
- **Pain map** — clickable body silhouette for post-workout soreness feedback
- **AI coach** — Cerebras-powered assistant, role-aware
- **Dark / Light / System** theme

---

## Quick start

No Qt, no Python, no compilers needed. Just download a launcher for your OS and run it.  
On every launch it checks GitHub for updates and installs them automatically.

### macOS

1. Download **[PeMa.command](https://raw.githubusercontent.com/dreysed/PeMa/final/PeMa.command)**
2. Open Terminal, run once to allow execution:
   ```bash
   chmod +x ~/Downloads/PeMa.command
   ```
3. Double-click `PeMa.command` in Finder — done.

On first launch the app is downloaded (~100 MB). Subsequent launches start instantly unless there's an update.

### Linux

1. Download **[PeMa.sh](https://raw.githubusercontent.com/dreysed/PeMa/final/PeMa.sh)**
2. Make it executable and run:
   ```bash
   chmod +x PeMa.sh
   ./PeMa.sh
   ```

### Windows

1. Download **[PeMa.bat](https://raw.githubusercontent.com/dreysed/PeMa/final/PeMa.bat)**
2. Double-click it — the app downloads, installs silently, and opens.

---

## Stack

🖥️ **UI** — Qt 6 / QML / QuickControls 2  
⚙️ **Backend** — Python 3.11+, FastAPI, SQLAlchemy, SQLite  
🔐 **Auth** — JWT (30-day tokens), bcrypt  
🗺️ **Maps** — OpenStreetMap tiles, OSRM routing  
🔄 **Sync** — Strava OAuth2, gpxpy, fitparse  
🤖 **AI** — Cerebras API (llama3.1-8b)  
☁️ **Hosting** — Amvera

---

## Strava setup

1. Go to [strava.com/settings/api](https://www.strava.com/settings/api) → create an app  
   Set **Authorization Callback Domain** to `localhost`
2. In PeMa open **Settings → Strava**, enter Client ID and Client Secret
3. Click **Connect Strava** — browser opens for authorization
4. After redirect, click **Sync** to import your full activity history

---

## Watch / GPS import

In the app header click **📥 Import**, select a `.gpx` or `.fit` file exported from:

- **Garmin Connect** — Activities → activity → ··· → Export Original
- **Apple Watch** — Health → Share → Export (zip contains `.gpx` files)
- **Strava** — Activity → ··· → Export GPX
- **Polar / Suunto / Coros** — export from their apps or web portals

The workout is created automatically with `status = done` and all metrics filled in.

---

## License

MIT
