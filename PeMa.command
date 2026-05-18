#!/bin/bash
# PeMa launcher — сборка + приложение (бэкенд на Amvera)

APP_DIR="$(cd "$(dirname "$0")" && pwd)"
BUILD_DIR="$APP_DIR/build-local"
QT_APP="$BUILD_DIR/PeMa.app"
CMAKE="$HOME/Qt/Tools/CMake/CMake.app/Contents/bin/cmake"
QT_DIR="$HOME/Qt/6.11.0/macos"

# ── 1. Собрать Qt-приложение если нужно ──────────────────────────────────────
echo "🔨 Проверяю сборку..."

if [ ! -f "$BUILD_DIR/Makefile" ] && [ ! -f "$BUILD_DIR/build.ninja" ]; then
    echo "   Первая сборка, конфигурирую..."
    mkdir -p "$BUILD_DIR"
    cd "$BUILD_DIR"
    "$CMAKE" -DCMAKE_PREFIX_PATH="$QT_DIR" -G "Unix Makefiles" "$APP_DIR" || {
        echo "❌ Ошибка конфигурации CMake"; read -p "Нажмите Enter..."; exit 1
    }
fi

cd "$BUILD_DIR"
"$CMAKE" --build . --parallel $(sysctl -n hw.logicalcpu) 2>&1 | tail -5
if [ $? -ne 0 ]; then
    echo "❌ Ошибка сборки."
    read -p "Нажмите Enter для выхода..."
    exit 1
fi
echo "✅ Сборка готова"

# ── 2. Запустить приложение ───────────────────────────────────────────────────
echo "🖥  Открываю приложение..."
open "$QT_APP"
