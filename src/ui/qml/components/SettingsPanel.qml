import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item {
    id: panel
    visible: _open || drawerAnim.running || overlayAnim.running

    property bool _open: false

    // ── Theme ─────────────────────────────────────────────────────────────────
    property color bg:          "#f0f2f5"
    property color surface:     "#ffffff"
    property color surface2:    "#f6f8fa"
    property color borderCol:   "#dde3eb"
    property color textPrimary: "#0d1117"
    property color textMuted:   "#57606a"
    property color accent:      "#6366f1"
    property color runColor:    "#22c55e"
    property bool  dark:        false

    // ── Bindings ──────────────────────────────────────────────────────────────
    property string themeMode:         "light"
    property string serverUrl:         "http://localhost:8000"
    property bool   isLoggedIn:        false
    property bool   stravaConnected:   false
    property bool   stravaHasClientId: false

    // ── Signals ───────────────────────────────────────────────────────────────
    signal themeModeChangeRequested(string mode)
    signal serverUrlChangeRequested(string url)
    signal logoutRequested()
    signal stravaConnectRequested()
    signal stravaDisconnectRequested()
    signal stravaSyncRequested()
    signal stravaSettingsRequested()

    function open()  { _open = true }
    function close() { _open = false }
    function toggle(){ _open = !_open }

    // ── Dim overlay ───────────────────────────────────────────────────────────
    Rectangle {
        id: overlay
        anchors.fill: parent
        color: "#000000"
        opacity: panel._open ? 0.32 : 0.0
        Behavior on opacity { NumberAnimation { id: overlayAnim; duration: 220 } }
        MouseArea { anchors.fill: parent; onClicked: panel.close() }
    }

    // ── Drawer ────────────────────────────────────────────────────────────────
    Rectangle {
        id: drawer
        width: 340
        anchors.top: parent.top; anchors.bottom: parent.bottom; anchors.right: parent.right
        x: panel._open ? parent.width - width : parent.width
        Behavior on x { NumberAnimation { id: drawerAnim; duration: 240; easing.type: Easing.OutCubic } }
        color: panel.surface

        Rectangle {
            anchors.left: parent.left; anchors.top: parent.top; anchors.bottom: parent.bottom
            width: 1; color: panel.borderCol
        }

        ScrollView {
            id: settingsScroll
            anchors.fill: parent
            contentWidth: availableWidth
            clip: true
            ScrollBar.horizontal.policy: ScrollBar.AlwaysOff

            Column {
                width: settingsScroll.availableWidth
                spacing: 0

                // ── Header ────────────────────────────────────────────────────
                Rectangle {
                    width: parent.width; height: 60; color: "transparent"
                    RowLayout {
                        anchors.fill: parent; anchors.leftMargin: 24; anchors.rightMargin: 16
                        Label {
                            text: "Настройки"
                            font.pixelSize: 18; font.weight: Font.Black; color: panel.textPrimary
                            Layout.fillWidth: true
                        }
                        Rectangle {
                            width: 30; height: 30; radius: 8; color: "transparent"
                            Label { anchors.centerIn: parent; text: "✕"; font.pixelSize: 14; color: panel.textMuted }
                            MouseArea { anchors.fill: parent; cursorShape: Qt.PointingHandCursor
                                onClicked: panel.close() }
                        }
                    }
                }
                Rectangle { width: parent.width; height: 1; color: panel.borderCol }

                Item { width: parent.width; height: 20 }

                // ── Внешний вид ───────────────────────────────────────────────
                Column {
                    width: parent.width - 48; x: 24; spacing: 8

                    Label {
                        text: "ВНЕШНИЙ ВИД"
                        font.pixelSize: 9; font.weight: Font.Black
                        color: panel.textMuted; font.letterSpacing: 1.2
                    }

                    Rectangle {
                        width: parent.width; height: 50; radius: 10
                        color: panel.surface2; border.width: 1; border.color: panel.borderCol
                        RowLayout {
                            anchors.fill: parent; anchors.leftMargin: 14; anchors.rightMargin: 12
                            Label {
                                text: "Тема"; font.pixelSize: 13; color: panel.textPrimary
                                Layout.fillWidth: true
                            }
                            Row {
                                spacing: 4
                                Repeater {
                                    model: [
                                        { icon: "☀", v: "light",  label: "Светлая" },
                                        { icon: "☾", v: "dark",   label: "Тёмная" },
                                        { icon: "⊙", v: "system", label: "Авто" }
                                    ]
                                    Rectangle {
                                        width: 36; height: 28; radius: 7
                                        color: panel.themeMode === modelData.v ? panel.accent : "transparent"
                                        border.width: 1
                                        border.color: panel.themeMode === modelData.v ? panel.accent : panel.borderCol
                                        Label {
                                            anchors.centerIn: parent; text: modelData.icon; font.pixelSize: 14
                                            color: panel.themeMode === modelData.v ? "#fff" : panel.textMuted
                                        }
                                        MouseArea { anchors.fill: parent; cursorShape: Qt.PointingHandCursor
                                            onClicked: panel.themeModeChangeRequested(modelData.v) }
                                    }
                                }
                            }
                        }
                    }
                }

                Item { width: parent.width; height: 20 }

                // ── Strava ────────────────────────────────────────────────────
                Column {
                    width: parent.width - 48; x: 24; spacing: 8

                    Label {
                        text: "STRAVA"
                        font.pixelSize: 9; font.weight: Font.Black
                        color: panel.textMuted; font.letterSpacing: 1.2
                    }

                    Rectangle {
                        width: parent.width
                        height: stravaInner.implicitHeight + 24
                        radius: 10; color: panel.surface2
                        border.width: 1; border.color: panel.borderCol

                        Column {
                            id: stravaInner
                            anchors.left: parent.left; anchors.right: parent.right
                            anchors.top: parent.top; anchors.margins: 14
                            spacing: 10

                            RowLayout {
                                width: parent.width
                                // Status dot + text
                                Rectangle {
                                    width: 8; height: 8; radius: 4
                                    color: panel.stravaConnected ? panel.runColor : panel.borderCol
                                }
                                Label {
                                    text: panel.stravaConnected ? "Подключено" : "Не подключено"
                                    font.pixelSize: 13; font.weight: Font.DemiBold
                                    color: panel.stravaConnected ? panel.runColor : panel.textPrimary
                                    Layout.fillWidth: true
                                }
                            }

                            Label {
                                width: parent.width
                                text: panel.stravaConnected
                                    ? "Активности синхронизируются с вашим аккаунтом Strava"
                                    : "Подключите аккаунт Strava чтобы тренировки автоматически попадали в календарь"
                                font.pixelSize: 11; color: panel.textMuted; wrapMode: Text.Wrap
                            }

                            Flow {
                                width: parent.width
                                spacing: 8

                                // Connect / Disconnect button
                                Rectangle {
                                    height: 32; width: stravaConnLbl.implicitWidth + 20; radius: 8
                                    color: panel.stravaConnected ? panel.surface : "#FC4C02"
                                    border.width: panel.stravaConnected ? 1 : 0
                                    border.color: panel.borderCol
                                    Label {
                                        id: stravaConnLbl; anchors.centerIn: parent
                                        text: panel.stravaConnected ? "Отключить" : "Подключить Strava"
                                        font.pixelSize: 12; font.weight: Font.DemiBold
                                        color: panel.stravaConnected ? panel.textMuted : "#fff"
                                    }
                                    MouseArea { anchors.fill: parent; cursorShape: Qt.PointingHandCursor
                                        onClicked: {
                                            if (panel.stravaConnected) panel.stravaDisconnectRequested()
                                            else if (!panel.stravaHasClientId) panel.stravaSettingsRequested()
                                            else panel.stravaConnectRequested()
                                        }
                                    }
                                }

                                // Sync button (only when connected)
                                Rectangle {
                                    visible: panel.stravaConnected
                                    height: 32; width: stravaSyncLbl.implicitWidth + 20; radius: 8
                                    color: panel.surface2; border.width: 1; border.color: panel.borderCol
                                    Label {
                                        id: stravaSyncLbl; anchors.centerIn: parent
                                        text: "Синхронизировать"
                                        font.pixelSize: 12; color: panel.accent
                                    }
                                    MouseArea { anchors.fill: parent; cursorShape: Qt.PointingHandCursor
                                        onClicked: panel.stravaSyncRequested() }
                                }

                                // Settings button (only when has client id)
                                Rectangle {
                                    visible: panel.stravaHasClientId
                                    height: 32; width: stravaSetLbl.implicitWidth + 20; radius: 8
                                    color: "transparent"; border.width: 1; border.color: panel.borderCol
                                    Label {
                                        id: stravaSetLbl; anchors.centerIn: parent
                                        text: "API ключи"
                                        font.pixelSize: 12; color: panel.textMuted
                                    }
                                    MouseArea { anchors.fill: parent; cursorShape: Qt.PointingHandCursor
                                        onClicked: panel.stravaSettingsRequested() }
                                }
                            }
                        }
                    }
                }

                Item { width: parent.width; height: 20 }

                // ── Синхронизация с часами ────────────────────────────────────
                Column {
                    width: parent.width - 48; x: 24; spacing: 8

                    Label {
                        text: "СИНХРОНИЗАЦИЯ С ЧАСАМИ"
                        font.pixelSize: 9; font.weight: Font.Black
                        color: panel.textMuted; font.letterSpacing: 1.2
                    }

                    Rectangle {
                        width: parent.width
                        height: watchInner.implicitHeight + 24
                        radius: 10; color: panel.surface2
                        border.width: 1; border.color: panel.borderCol

                        Column {
                            id: watchInner
                            anchors.left: parent.left; anchors.right: parent.right
                            anchors.top: parent.top; anchors.margins: 14
                            spacing: 12

                            Label {
                                width: parent.width
                                text: "PeMa принимает файлы .gpx и .fit — экспортируй активность из приложения своих часов и загрузи через кнопку «Импорт» в тренировке."
                                font.pixelSize: 11; color: panel.textPrimary; wrapMode: Text.Wrap
                            }

                            Repeater {
                                model: [
                                    { name: "Garmin Connect",  icon: "⌚", hint: "Activities → тренировка → … → Export Original" },
                                    { name: "Apple Watch",     icon: "🍎", hint: "Здоровье → Поделиться → Экспорт данных (.zip с .gpx)" },
                                    { name: "Strava",          icon: "🏅", hint: "Активность → ⋯ → Экспорт GPX" },
                                ]
                                delegate: RowLayout {
                                    width: parent.width; spacing: 10
                                    Rectangle {
                                        width: 32; height: 32; radius: 8
                                        color: panel.surface
                                        border.width: 1; border.color: panel.borderCol
                                        Label { anchors.centerIn: parent; text: modelData.icon; font.pixelSize: 16 }
                                    }
                                    Column {
                                        Layout.fillWidth: true; spacing: 1
                                        Label { text: modelData.name; font.pixelSize: 12; font.weight: Font.DemiBold; color: panel.textPrimary }
                                        Label { width: parent.width; text: modelData.hint; font.pixelSize: 10; color: panel.textMuted; wrapMode: Text.Wrap }
                                    }
                                }
                            }
                        }
                    }
                }

                Item { width: parent.width; height: 20 }

                // ── О приложении ──────────────────────────────────────────────
                Column {
                    width: parent.width - 48; x: 24; spacing: 4
                    Label {
                        text: "О ПРИЛОЖЕНИИ"
                        font.pixelSize: 9; font.weight: Font.Black
                        color: panel.textMuted; font.letterSpacing: 1.2
                    }
                    Label { text: "PeMa v2.0"; font.pixelSize: 13; font.weight: Font.DemiBold; color: panel.textPrimary }
                    Label { text: "Qt 6 · FastAPI · SQLite · OpenStreetMap"; font.pixelSize: 11; color: panel.textMuted }
                }

                Item { width: parent.width; height: 28 }

                // ── Выход ─────────────────────────────────────────────────────
                Column {
                    width: parent.width - 48; x: 24; spacing: 10
                    visible: panel.isLoggedIn

                    Rectangle {
                        width: parent.width; height: 44; radius: 10
                        color: "#fef2f2"
                        border.width: 1; border.color: "#fecaca"

                        RowLayout {
                            anchors.fill: parent; anchors.leftMargin: 16; anchors.rightMargin: 14
                            spacing: 12

                            Label {
                                text: "⏏"
                                font.pixelSize: 18; color: "#ef4444"
                            }
                            Column {
                                spacing: 1; Layout.fillWidth: true
                                Label {
                                    text: "Выйти из аккаунта"
                                    font.pixelSize: 13; font.weight: Font.DemiBold; color: "#ef4444"
                                }
                                Label {
                                    text: "Вы вернётесь на экран входа"
                                    font.pixelSize: 10; color: "#f87171"
                                }
                            }
                            Label {
                                text: "›"
                                font.pixelSize: 18; color: "#ef4444"; opacity: 0.6
                            }
                        }

                        MouseArea {
                            anchors.fill: parent; cursorShape: Qt.PointingHandCursor
                            onClicked: panel.logoutRequested()
                        }
                    }
                }

                Item { width: parent.width; height: 24 }
            }
        }
    }
}
