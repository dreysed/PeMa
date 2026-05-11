import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Popup {
    id: goalDialog
    modal: true; focus: true
    anchors.centerIn: Overlay.overlay
    width: 400; padding: 0
    closePolicy: Popup.NoAutoClose

    // Theme
    property color surface:     "#ffffff"
    property color surface2:    "#f6f8fa"
    property color borderCol:   "#dde3eb"
    property color textPrimary: "#0d1117"
    property color textMuted:   "#57606a"
    property color accent:      "#6366f1"

    signal goalCreated(string title, string targetDate, string type,
                       real targetValue, string targetUnit)

    // Pre-fill date from calendar click
    property string prefillDate: ""

    onOpened: {
        goalTitleField.text        = ""
        goalDateField.text         = goalDialog.prefillDate !== ""
                                     ? goalDialog.prefillDate
                                     : Qt.formatDate(new Date(), "yyyy-MM-dd")
        goalValueSpin.value        = 42
        goalUnitCombo.currentIndex = 0   // 0 = авто
        volumeToggle.checked       = false
    }

    background: Rectangle {
        radius: 14; color: goalDialog.surface
        border.width: 1; border.color: goalDialog.borderCol
    }

    ColumnLayout {
        width: goalDialog.width; spacing: 0

        // ── Header ────────────────────────────────────────────────────────────
        Rectangle {
            Layout.fillWidth: true; height: 56; radius: 14
            color: goalDialog.surface2
            Rectangle { anchors.left: parent.left; anchors.right: parent.right; anchors.bottom: parent.bottom; height: 14; color: parent.color }
            RowLayout {
                anchors.fill: parent; anchors.leftMargin: 20; anchors.rightMargin: 14
                Column {
                    spacing: 2
                    Label {
                        text: "Новая цель"
                        font.pixelSize: 15; font.weight: Font.DemiBold; color: goalDialog.textPrimary
                    }
                    Label {
                        text: "Цель сохраняется и отображается в аналитике"
                        font.pixelSize: 11; color: goalDialog.textMuted
                    }
                }
                Item { Layout.fillWidth: true }
                Rectangle {
                    width: 30; height: 30; radius: 8; color: "transparent"
                    Label { anchors.centerIn: parent; text: "✕"; font.pixelSize: 14; color: goalDialog.textMuted }
                    MouseArea { anchors.fill: parent; cursorShape: Qt.PointingHandCursor
                        onClicked: goalDialog.close() }
                }
            }
        }
        Rectangle { Layout.fillWidth: true; height: 1; color: goalDialog.borderCol }

        // ── Form ──────────────────────────────────────────────────────────────
        ColumnLayout {
            Layout.fillWidth: true; Layout.margins: 20; spacing: 16

            ColumnLayout { Layout.fillWidth: true; spacing: 6
                Label { text: "НАЗВАНИЕ"; font.pixelSize: 9; font.weight: Font.Black; color: goalDialog.textMuted; font.letterSpacing: 1.2 }
                TextField {
                    id: goalTitleField
                    Layout.fillWidth: true; implicitHeight: 38
                    placeholderText: "Например: Марафон Москва"
                    background: Rectangle { radius: 8; color: goalDialog.surface2; border.width: 1; border.color: goalDialog.borderCol }
                }
            }

            ColumnLayout { Layout.fillWidth: true; spacing: 6
                Label { text: "ДАТА ЦЕЛИ"; font.pixelSize: 9; font.weight: Font.Black; color: goalDialog.textMuted; font.letterSpacing: 1.2 }
                TextField {
                    id: goalDateField
                    Layout.fillWidth: true; implicitHeight: 38
                    placeholderText: "ГГГГ-ММ-ДД"
                    background: Rectangle { radius: 8; color: goalDialog.surface2; border.width: 1; border.color: goalDialog.borderCol }
                }
            }

            ColumnLayout { Layout.fillWidth: true; spacing: 8
                // Toggle row
                RowLayout {
                    Layout.fillWidth: true
                    Label { text: "ЦЕЛЕВОЙ ОБЪЁМ"; font.pixelSize: 9; font.weight: Font.Black; color: goalDialog.textMuted; font.letterSpacing: 1.2; Layout.fillWidth: true }
                    CheckBox {
                        id: volumeToggle
                        checked: false
                        text: "Указать"
                        font.pixelSize: 11
                    }
                }
                // Hint when auto
                Label {
                    visible: !volumeToggle.checked
                    Layout.fillWidth: true
                    text: "Прогресс будет считаться автоматически: 50% по времени + 50% по выполнению тренировок"
                    font.pixelSize: 10; color: goalDialog.textMuted; wrapMode: Text.Wrap
                }
                // Volume fields (shown only when toggle is on)
                RowLayout {
                    visible: volumeToggle.checked
                    spacing: 10; Layout.fillWidth: true
                    SpinBox {
                        id: goalValueSpin
                        from: 1; to: 99999; value: 42
                        implicitHeight: 38; Layout.fillWidth: true
                    }
                    ComboBox {
                        id: goalUnitCombo
                        implicitHeight: 38; implicitWidth: 120
                        model: ["км", "мин", "пробежек"]
                    }
                }
            }
        }

        Rectangle { Layout.fillWidth: true; height: 1; color: goalDialog.borderCol }

        // ── Footer ────────────────────────────────────────────────────────────
        Rectangle {
            Layout.fillWidth: true; height: 60; radius: 14
            color: goalDialog.surface2
            Rectangle { anchors.left: parent.left; anchors.right: parent.right; anchors.top: parent.top; height: 14; color: parent.color }
            RowLayout {
                anchors.fill: parent; anchors.leftMargin: 20; anchors.rightMargin: 20; spacing: 10
                Item { Layout.fillWidth: true }
                Rectangle {
                    height: 34; width: goalCnclLbl.implicitWidth + 24; radius: 8
                    color: "transparent"; border.width: 1; border.color: goalDialog.borderCol
                    Label { id: goalCnclLbl; anchors.centerIn: parent; text: "Отмена"; font.pixelSize: 13; color: goalDialog.textMuted }
                    MouseArea { anchors.fill: parent; cursorShape: Qt.PointingHandCursor
                        onClicked: goalDialog.close() }
                }
                Rectangle {
                    height: 34; width: goalSaveLbl.implicitWidth + 24; radius: 8
                    color: goalDialog.accent
                    opacity: goalTitleField.text.trim().length > 0 ? 1.0 : 0.4
                    Label { id: goalSaveLbl; anchors.centerIn: parent; text: "Создать цель"; font.pixelSize: 13; font.weight: Font.DemiBold; color: "#fff" }
                    MouseArea {
                        anchors.fill: parent
                        enabled: goalTitleField.text.trim().length > 0
                        cursorShape: Qt.PointingHandCursor
                        onClicked: {
                            var unitMap = ["km", "min", "runs"]
                            var unit = volumeToggle.checked ? unitMap[goalUnitCombo.currentIndex] : ""
                            var val  = volumeToggle.checked ? goalValueSpin.value : 0
                            goalDialog.goalCreated(
                                goalTitleField.text.trim(),
                                goalDateField.text,
                                "volume",
                                val,
                                unit
                            )
                            goalDialog.close()
                        }
                    }
                }
            }
        }
    }
}
