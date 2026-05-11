# PeMa - Personal Training Manager

Desktop app for planning and tracking workouts. Coach creates plans, athlete executes and logs results.

Built with Qt 6 + FastAPI.

## Features

- Calendar with monthly workout grid
- Coach and athlete roles
- Analytics: distance, pace, streak, weekly and monthly charts
- Routes: generate circular routes by distance, draw on OSM map, Strava sync
- Watch import: upload .gpx or .fit files for actual HR, distance, elevation
- Templates: save and reuse workout templates
- Pain map: clickable body silhouette for post-workout feedback
- Goals: race or volume targets with progress tracking
- Dark / light / system theme

## Stack

- UI: Qt 6 / QML / QuickControls 2
- Backend: Python, FastAPI, SQLAlchemy, SQLite
- Maps: OpenStreetMap tiles, OSRM routing
- Auth: JWT, bcrypt
- Sync: Strava OAuth2, GPX/FIT parsing

## Requirements

Qt app: Qt 6.5+, CMake 3.21+, C++17

Backend: Python 3.10+, see `api/requirements.txt`

## Quick start (macOS)

```bash
git clone https://github.com/dreysed/PeMa.git
cd PeMa
bash PeMa.command
```

The script builds the Qt app, installs Python deps, starts the backend on port 8000 and opens the app.

## Manual build

```bash
# Backend
cd api
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --port 8000

# Qt app
mkdir build && cd build
cmake -DCMAKE_PREFIX_PATH="~/Qt/6.11.0/macos" ..
cmake --build . --parallel
open PeMa.app
```

## Strava setup

1. Create an app at strava.com/settings/api
2. In PeMa go to Settings, enter Client ID and Secret
3. Click Connect Strava and authorize in the browser
4. Click Sync to import recent activities

## License

MIT
