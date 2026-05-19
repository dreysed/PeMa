#!/bin/bash
# deploy-linux.sh — собирает PeMa и упаковывает в AppImage (работает на любом дистрибутиве)

set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BUILD_DIR="$SCRIPT_DIR/build-linux"
APPDIR="$BUILD_DIR/AppDir"

echo "═══════════════════════════════════════════"
echo "  PeMa — Linux AppImage Deploy"
echo "═══════════════════════════════════════════"

# ── Зависимости ───────────────────────────────────────────────────────────────
if ! command -v cmake &>/dev/null; then
    echo "❌ cmake не найден. Установите: sudo apt install cmake"
    exit 1
fi

# ── 1. Сборка ─────────────────────────────────────────────────────────────────
echo ""
echo "🔨 Сборка..."
mkdir -p "$BUILD_DIR"
cd "$BUILD_DIR"

cmake \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX="$APPDIR/usr" \
    "$SCRIPT_DIR"

cmake --build . --parallel "$(nproc)"
cmake --install .
echo "✅ Сборка готова"

# ── 2. AppDir структура ───────────────────────────────────────────────────────
echo ""
echo "📦 Подготовка AppDir..."

# Desktop файл (обязателен для AppImage)
cat > "$APPDIR/PeMa.desktop" << 'EOF'
[Desktop Entry]
Name=PeMa
Comment=Спортивный календарь тренировок
Exec=PeMa
Icon=AppIcon
Type=Application
Categories=Sports;Health;
EOF

# Иконка
if [ -f "$SCRIPT_DIR/resources/AppIcon_rounded.png" ]; then
    cp "$SCRIPT_DIR/resources/AppIcon_rounded.png" "$APPDIR/AppIcon.png"
fi

# AppRun — точка входа
cat > "$APPDIR/AppRun" << 'APPRUN'
#!/bin/bash
SELF=$(readlink -f "$0")
HERE="${SELF%/*}"
export QT_PLUGIN_PATH="$HERE/usr/lib/qt6/plugins:$QT_PLUGIN_PATH"
export QML2_IMPORT_PATH="$HERE/usr/lib/qt6/qml:$QML2_IMPORT_PATH"
exec "$HERE/usr/bin/PeMa" "$@"
APPRUN
chmod +x "$APPDIR/AppRun"

# ── 3. linuxdeploy + AppImage ─────────────────────────────────────────────────
echo ""
echo "🛠  Загрузка linuxdeploy..."

cd "$BUILD_DIR"

# Скачиваем linuxdeploy если нет
if [ ! -f "linuxdeploy-x86_64.AppImage" ]; then
    wget -q --show-progress \
        "https://github.com/linuxdeploy/linuxdeploy/releases/download/continuous/linuxdeploy-x86_64.AppImage"
    chmod +x linuxdeploy-x86_64.AppImage
fi

# Скачиваем Qt-плагин для linuxdeploy если нет
if [ ! -f "linuxdeploy-plugin-qt-x86_64.AppImage" ]; then
    wget -q --show-progress \
        "https://github.com/linuxdeploy/linuxdeploy-plugin-qt/releases/download/continuous/linuxdeploy-plugin-qt-x86_64.AppImage"
    chmod +x linuxdeploy-plugin-qt-x86_64.AppImage
fi

echo ""
echo "📦 Упаковка AppImage..."

OUTPUT="$SCRIPT_DIR/PeMa-linux.AppImage"

DEPLOY_LIBS=""
if command -v qmake6 &>/dev/null; then
    export QMAKE=$(command -v qmake6)
elif command -v qmake &>/dev/null; then
    export QMAKE=$(command -v qmake)
fi

./linuxdeploy-x86_64.AppImage \
    --appdir "$APPDIR" \
    --plugin qt \
    --output appimage

# linuxdeploy называет файл по имени из .desktop
GENERATED=$(ls "$BUILD_DIR"/PeMa*.AppImage 2>/dev/null | head -1)
if [ -n "$GENERATED" ] && [ "$GENERATED" != "$OUTPUT" ]; then
    mv "$GENERATED" "$OUTPUT"
fi

echo ""
echo "✅ Готово!"
echo "   📁 Файл: $OUTPUT"
echo "   📏 Размер: $(du -sh "$OUTPUT" | cut -f1)"
echo ""
echo "   Запуск: chmod +x PeMa-linux.AppImage && ./PeMa-linux.AppImage"
