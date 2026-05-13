[![RU](https://img.shields.io/badge/lang-RU-blue?style=flat-square)](README.ru.md)

# PeMa — Personal Training Manager

Desktop application for planning and tracking workouts. A coach creates training plans, athletes execute them and log results.

Built with **Qt 6 / QML** + **Python FastAPI**.

---

## Features

- **Calendar** — monthly workout grid, add/edit/delete workouts
- **Roles** — coach creates plans for athletes; athlete sees only own calendar
- **Analytics** — total distance, pace, streak, weekly/monthly charts, completion rate
- **Goals** — race or volume targets with automatic progress tracking
- **Routes** — generate circular routes by distance, draw freehand on OSM map with pen/eraser, edit saved routes, export as GPX
- **Watch import** — upload `.gpx` or `.fit` files → actual HR, distance, pace, elevation fill automatically, workout marked as done
- **Strava sync** — OAuth2 connect, imports full activity history
- **Templates** — save and reuse workout structures
- **Pain map** — clickable body silhouette for post-workout soreness feedback
- **AI coach** — Cerebras-powered assistant, role-aware (athlete gets advice only, coach gets full editing)
- **Dark / Light / System** theme

---

## Stack

🖥️ **UI** — Qt 6 / QML / QuickControls 2  
⚙️ **Backend** — Python 3.11+, FastAPI, SQLAlchemy, SQLite  
🔐 **Auth** — JWT (30-day tokens), bcrypt  
🗺️ **Maps** — OpenStreetMap tiles, OSRM routing  
🔄 **Sync** — Strava OAuth2, gpxpy, fitparse  
🤖 **AI** — Cerebras API (llama3.1-8b)

---

## Requirements

**Qt app**
- Qt 6.5 or newer (install via [Qt Maintenance Tool](https://www.qt.io/download))
- CMake 3.21+
- C++17 compiler (Xcode CLT on macOS, MSVC 2022 or MinGW on Windows)

**Backend**
- Python 3.10+
- Dependencies in `api/requirements.txt`

---

## Quick start — macOS

Double-click **`PeMa.command`** in Finder, or run from Terminal:

```bash
git clone https://github.com/dreysed/PeMa.git
cd PeMa
bash PeMa.command
```

The script:
1. Builds the Qt app (first run takes 1–2 min)
2. Creates a Python venv and installs dependencies
3. Starts the backend on `http://localhost:8000`
4. Opens the app; kills the backend when you close it

---

## Quick start — Windows

### 1. Install prerequisites

- [Qt 6.11](https://www.qt.io/download-qt-installer) — during install tick **MSVC 2022 64-bit** and **CMake**
- [Python 3.11+](https://www.python.org/downloads/windows/) — tick **Add Python to PATH**
- [Git](https://git-scm.com/download/win)
- Visual Studio 2022 Build Tools (or full VS) with **Desktop C++ workload**

### 2. Clone and build backend

Open **Developer Command Prompt for VS 2022** (search in Start menu):

```bat
git clone https://github.com/dreysed/PeMa.git
cd PeMa\api
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Build the Qt app

Still in Developer Command Prompt:

```bat
cd ..
mkdir build-win
cd build-win
cmake -DCMAKE_PREFIX_PATH="C:\Qt\6.11.0\msvc2022_64" -G "NMake Makefiles" ..
cmake --build . --parallel
```

> Adjust the Qt path to match your installation. Check `C:\Qt\` to find the exact folder name.

### 4. Deploy Qt DLLs

```bat
C:\Qt\6.11.0\msvc2022_64\bin\windeployqt.exe --qmldir ..\src\ui\qml PeMa.exe
```

### 5. Run

Open two command prompts:

**Terminal 1 — backend:**
```bat
cd PeMa\api
venv\Scripts\activate
uvicorn main:app --port 8000
```

**Terminal 2 — app:**
```bat
cd PeMa\build-win
PeMa.exe
```

---

## Manual build — macOS

```bash
# Backend
cd api
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --port 8000 &

# Qt app
cd ..
mkdir build && cd build
cmake -DCMAKE_PREFIX_PATH="$HOME/Qt/6.11.0/macos" -G "Unix Makefiles" ..
cmake --build . --parallel
open PeMa.app
```

---

## Strava setup

1. Go to [strava.com/settings/api](https://www.strava.com/settings/api) and create an app
   - Set **Authorization Callback Domain** to `localhost`
2. In PeMa open **Settings → Strava**, enter your Client ID and Client Secret
3. Click **Connect Strava** — browser opens for authorization
4. After redirect back, click **Sync** to import your full activity history

---

## Watch / GPS import

In the main app header click **📥 Импорт**, select a `.gpx` or `.fit` file exported from:

- **Garmin Connect** — Activities → activity → ··· → Export Original
- **Apple Watch** — Health → Share → Export (zip contains `.gpx` files)
- **Strava** — Activity → ··· → Export GPX
- **Polar / Suunto / Coros** — export from their respective apps or web portals

The workout is created automatically with `status = done` and all metrics filled in.

---

## License

MIT
