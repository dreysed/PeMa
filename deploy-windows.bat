@echo off
chcp 65001 > nul
echo ═══════════════════════════════════════════
echo   PeMa — Windows Deploy
echo ═══════════════════════════════════════════

:: ── Пути (меняй если Qt установлен в другую папку) ─────────────────────────
set QT_VER=6.11.0
set QT_ARCH=msvc2022_64
set QT_DIR=C:\Qt\%QT_VER%\%QT_ARCH%
set CMAKE_DIR=C:\Qt\Tools\CMake_64\bin

set SCRIPT_DIR=%~dp0
set BUILD_DIR=%SCRIPT_DIR%build-windows
set STAGE_DIR=%SCRIPT_DIR%installer\windows-stage
set EXE=%BUILD_DIR%\Release\PeMa.exe

:: ── 1. Сборка ─────────────────────────────────────────────────────────────
echo.
echo [1/3] Сборка...

if not exist "%BUILD_DIR%" mkdir "%BUILD_DIR%"
cd /d "%BUILD_DIR%"

if not exist "CMakeCache.txt" (
    "%CMAKE_DIR%\cmake.exe" ^
        -DCMAKE_PREFIX_PATH="%QT_DIR%" ^
        -DCMAKE_BUILD_TYPE=Release ^
        -G "Visual Studio 17 2022" -A x64 ^
        "%SCRIPT_DIR%"
    if errorlevel 1 ( echo [ОШИБКА] cmake configure & pause & exit /b 1 )
)

"%CMAKE_DIR%\cmake.exe" --build . --config Release --parallel
if errorlevel 1 ( echo [ОШИБКА] cmake build & pause & exit /b 1 )
echo [OK] Сборка готова

:: ── 2. windeployqt — копирует DLL-ки ──────────────────────────────────────
echo.
echo [2/3] Упаковка DLL...

if not exist "%STAGE_DIR%" mkdir "%STAGE_DIR%"
copy /Y "%EXE%" "%STAGE_DIR%\" > nul

"%QT_DIR%\bin\windeployqt.exe" ^
    --release ^
    --no-translations ^
    --qmldir "%SCRIPT_DIR%src\ui\qml" ^
    "%STAGE_DIR%\PeMa.exe"

if errorlevel 1 ( echo [ОШИБКА] windeployqt & pause & exit /b 1 )
echo [OK] DLL скопированы в %STAGE_DIR%

:: ── 3. Inno Setup — создаёт installer .exe ────────────────────────────────
echo.
echo [3/3] Создание установщика...

:: Ищем Inno Setup
set INNO=""
if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" set INNO=C:\Program Files (x86)\Inno Setup 6\ISCC.exe
if exist "C:\Program Files\Inno Setup 6\ISCC.exe"       set INNO=C:\Program Files\Inno Setup 6\ISCC.exe

if %INNO%=="" (
    echo.
    echo [!] Inno Setup не найден.
    echo     Скачайте с https://jrsoftware.org/isdl.php и установите.
    echo.
    echo     Папка с файлами приложения: %STAGE_DIR%
    echo     После установки Inno Setup запустите этот скрипт снова.
    pause
    exit /b 0
)

"%INNO%" "%SCRIPT_DIR%installer\PeMa.iss"
if errorlevel 1 ( echo [ОШИБКА] Inno Setup & pause & exit /b 1 )

echo.
echo ✅ Готово!
echo    Файл: %SCRIPT_DIR%installer\PeMa-Setup.exe
echo.
pause
