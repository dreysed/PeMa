#!/bin/bash
# PeMa.sh — запуск с автообновлением (Linux)
# chmod +x PeMa.sh && ./PeMa.sh

REPO="dreysed/PeMa"
DATA_DIR="$HOME/.local/share/PeMa"
VERSION_FILE="$DATA_DIR/.version"
APPIMAGE="$DATA_DIR/PeMa.AppImage"

mkdir -p "$DATA_DIR"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  PeMa Launcher"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "⏳ Проверка обновлений..."

LATEST=$(curl -sf "https://api.github.com/repos/$REPO/releases/latest" \
    | python3 -c "import sys,json; print(json.load(sys.stdin)['tag_name'])" 2>/dev/null || echo "")

if [ -z "$LATEST" ]; then
    echo "⚠️  Нет интернета — запускаем текущую версию"
else
    CURRENT=$(cat "$VERSION_FILE" 2>/dev/null || echo "none")

    if [ "$LATEST" != "$CURRENT" ] || [ ! -f "$APPIMAGE" ]; then
        echo "📦 Скачиваем PeMa $LATEST..."
        curl -L --progress-bar \
            "https://github.com/$REPO/releases/download/$LATEST/PeMa-linux.AppImage" \
            -o "$APPIMAGE"
        chmod +x "$APPIMAGE"
        echo "$LATEST" > "$VERSION_FILE"
        echo "✅ Обновлено до $LATEST"
    else
        echo "✅ Актуальная версия ($CURRENT)"
    fi
fi

echo ""
echo "🚀 Запуск PeMa..."
exec "$APPIMAGE"
