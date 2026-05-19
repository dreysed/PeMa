#!/bin/bash
# deploy-mac.command — собирает PeMa.app и упаковывает в DMG-установщик

set -e
APP_DIR="$(cd "$(dirname "$0")" && pwd)"
BUILD_DIR="$APP_DIR/build-release"
QT_DIR="$HOME/Qt/6.11.0/macos"
CMAKE="$HOME/Qt/Tools/CMake/CMake.app/Contents/bin/cmake"
APP="$BUILD_DIR/PeMa.app"
OUT_DMG="$APP_DIR/PeMa-mac.dmg"

echo "═══════════════════════════════════════════"
echo "  PeMa — macOS Deploy"
echo "═══════════════════════════════════════════"

# ── 1. Сборка ─────────────────────────────────
echo ""
echo "🔨 Сборка..."
mkdir -p "$BUILD_DIR"
cd "$BUILD_DIR"

if [ ! -f "Makefile" ] && [ ! -f "build.ninja" ]; then
    "$CMAKE" -DCMAKE_PREFIX_PATH="$QT_DIR" \
             -DCMAKE_BUILD_TYPE=Release \
             -G "Unix Makefiles" \
             "$APP_DIR"
fi

"$CMAKE" --build . --config Release --parallel "$(sysctl -n hw.logicalcpu)"
echo "✅ Сборка готова"

# ── 2. macdeployqt — копирует Qt-фреймворки в .app ───────────────────────────
echo ""
echo "📦 Упаковка Qt-фреймворков..."
"$QT_DIR/bin/macdeployqt" "$APP" \
    --qmldir="$APP_DIR/src/ui/qml" \
    -always-overwrite
echo "✅ Фреймворки добавлены"

# ── 3. Создание DMG ───────────────────────────
echo ""
echo "💿 Создание DMG..."

# Временный образ
TMP_DMG="$BUILD_DIR/tmp.dmg"
VOLUME_NAME="PeMa"
STAGING="$BUILD_DIR/dmg-stage"

rm -rf "$STAGING"
mkdir -p "$STAGING"
cp -R "$APP" "$STAGING/"
# Симлинк на /Applications для drag-and-drop установки
ln -sf /Applications "$STAGING/Applications"

hdiutil create \
    -volname "$VOLUME_NAME" \
    -srcfolder "$STAGING" \
    -ov \
    -format UDRW \
    "$TMP_DMG" > /dev/null

# Конвертируем в read-only сжатый DMG
rm -f "$OUT_DMG"
hdiutil convert "$TMP_DMG" \
    -format UDZO \
    -o "$OUT_DMG" > /dev/null

rm -f "$TMP_DMG"

echo "✅ Готово!"
echo ""
echo "   📁 Файл: $OUT_DMG"
echo "   📏 Размер: $(du -sh "$OUT_DMG" | cut -f1)"
echo ""
echo "   Откройте DMG, перетащите PeMa в Applications — и готово."
echo ""
open "$APP_DIR"
