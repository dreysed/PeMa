[![EN](https://img.shields.io/badge/lang-EN-blue?style=flat-square)](README.md)

# PeMa — Персональный менеджер тренировок

Творческая работа студента группы РИС-25-1Б Пархоменко Романа и Мехоношина Антона на тему: 
Разработка автоматизированного рабочего места спортивного тренера.

Десктопное приложение для планирования и отслеживания тренировок. Тренер создаёт планы, спортсмены выполняют их и фиксируют результаты.

Стек: **Qt 6 / QML** + **Python FastAPI**.

---

## Возможности

- **Календарь** — месячная сетка тренировок, добавление / редактирование / удаление
- **Роли** — тренер создаёт планы для спортсменов; спортсмен видит только свой календарь
- **Аналитика** — суммарная дистанция, темп, серия дней, графики по неделям/месяцам, процент выполнения
- **Цели** — соревновательные или объёмные цели с автоматическим отслеживанием прогресса
- **Маршруты** — генерация круговых маршрутов по дистанции, рисование от руки на OSM-карте (карандаш / ластик), редактирование и экспорт GPX
- **Импорт с часов** — загрузка `.gpx` или `.fit` файлов → ЧСС, дистанция, темп, набор высоты заполняются автоматически, тренировка помечается как выполненная
- **Синхронизация со Strava** — подключение по OAuth2, импорт всей истории активностей
- **Шаблоны** — сохранение и повторное использование структур тренировок
- **Карта боли** — кликабельный силуэт тела для отметки болевых ощущений после тренировки
- **ИИ-тренер** — ассистент на базе Cerebras, с учётом роли (спортсмен получает советы, тренер — полное редактирование)
- **Темы** — тёмная / светлая / системная

---

## Стек

🖥️ **UI** — Qt 6 / QML / QuickControls 2  
⚙️ **Backend** — Python 3.11+, FastAPI, SQLAlchemy, SQLite  
🔐 **Авторизация** — JWT (токены на 30 дней), bcrypt  
🗺️ **Карты** — OpenStreetMap tiles, OSRM routing  
🔄 **Синхронизация** — Strava OAuth2, gpxpy, fitparse  
🤖 **ИИ** — Cerebras API (llama3.1-8b)

---

## Требования

**Qt-приложение**
- Qt 6.5 или новее ([Qt Maintenance Tool](https://www.qt.io/download))
- CMake 3.21+
- Компилятор C++17 (Xcode CLT на macOS; MSVC 2022 или MinGW на Windows)

**Backend**
- Python 3.10+
- Зависимости в `api/requirements.txt`

---

## Быстрый старт — macOS

Дважды нажмите **`PeMa.command`** в Finder или выполните в терминале:

```bash
git clone https://github.com/dreysed/PeMa.git
cd PeMa
bash PeMa.command
```

Скрипт:
1. Собирает Qt-приложение (первый раз — 1–2 мин)
2. Создаёт Python venv и устанавливает зависимости
3. Запускает бэкенд на `http://localhost:8000`
4. Открывает приложение; при закрытии завершает бэкенд

---

## Быстрый старт — Windows

### 1. Установите зависимости

- [Qt 6.11](https://www.qt.io/download-qt-installer) — при установке отметьте **MSVC 2022 64-bit** и **CMake**
- [Python 3.11+](https://www.python.org/downloads/windows/) — отметьте **Add Python to PATH**
- [Git](https://git-scm.com/download/win)
- Visual Studio 2022 Build Tools (или полная VS) с компонентом **Desktop development with C++**

### 2. Клонируйте репозиторий и настройте бэкенд

Откройте **Developer Command Prompt for VS 2022** (найдите через поиск в меню «Пуск»):

```bat
git clone https://github.com/dreysed/PeMa.git
cd PeMa\api
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Соберите Qt-приложение

В том же терминале Developer Command Prompt:

```bat
cd ..
mkdir build-win
cd build-win
cmake -DCMAKE_PREFIX_PATH="C:\Qt\6.11.0\msvc2022_64" -G "NMake Makefiles" ..
cmake --build . --parallel
```

> Путь к Qt уточните в папке `C:\Qt\` — название подпапки зависит от версии.

### 4. Разверните Qt DLL

```bat
C:\Qt\6.11.0\msvc2022_64\bin\windeployqt.exe --qmldir ..\src\ui\qml PeMa.exe
```

### 5. Запуск

Откройте два командных окна:

**Окно 1 — бэкенд:**
```bat
cd PeMa\api
venv\Scripts\activate
uvicorn main:app --port 8000
```

**Окно 2 — приложение:**
```bat
cd PeMa\build-win
PeMa.exe
```

---

## Ручная сборка — macOS

```bash
# Бэкенд
cd api
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --port 8000 &

# Qt-приложение
cd ..
mkdir build && cd build
cmake -DCMAKE_PREFIX_PATH="$HOME/Qt/6.11.0/macos" -G "Unix Makefiles" ..
cmake --build . --parallel
open PeMa.app
```

---

## Настройка Strava

1. Зайдите на [strava.com/settings/api](https://www.strava.com/settings/api) и создайте приложение
   - В поле **Authorization Callback Domain** укажите `localhost`
2. В PeMa откройте **Настройки → Strava**, введите Client ID и Client Secret
3. Нажмите **Подключить Strava** — откроется браузер для авторизации
4. После редиректа нажмите **Синхронизировать** — вся история активностей импортируется

---

## Импорт с часов / GPS

В шапке приложения нажмите **📥 Импорт**, выберите файл `.gpx` или `.fit`, экспортированный из:

- **Garmin Connect** — Активности → активность → ··· → Экспортировать оригинал
- **Apple Watch** — Здоровье → Поделиться → Экспортировать (zip содержит `.gpx`)
- **Strava** — Активность → ··· → Экспортировать GPX
- **Polar / Suunto / Coros** — экспорт из их приложений или веб-портала

Тренировка создаётся автоматически со статусом `выполнено`, все метрики заполняются.

---

## Лицензия

MIT
