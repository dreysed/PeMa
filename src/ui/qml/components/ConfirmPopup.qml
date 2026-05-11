import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

/**
 * Reusable confirmation popup — matches the app's visual language.
 * Usage:
 *   ConfirmPopup { id: myConfirm; title: "..."; message: "..."; onAccepted: ... }
 *   myConfirm.open()
 */
Popup {
    id: confirmPopup
    modal: true; focus: true
    anchors.centerIn: Overlay.overlay
    width: 360; padding: 0
    closePolicy: Popup.NoAutoClose

    property string title:       "Подтвердите"
    property string message:     ""
    property string confirmText: "Удалить"
    property string cancelText:  "Отмена"
    property bool   destructive: true     // red confirm button

    // Theme (injected from root)
    property color surface:     "#ffffff"
    property color surface2:    "#f6f8fa"
    property color borderCol:   "#dde3eb"
    property color textPrimary: "#0d1117"
    property color textMuted:   "#57606a"
    property color accent:      "#6366f1"

    signal accepted()
    signal rejected()

    background: Rectangle {
        radius: 14; color: confirmPopup.surface
        border.width: 1; border.color: confirmPopup.borderCol
    }

    ColumnLayout {
        width: confirmPopup.width; spacing: 0

        // ── Header ────────────────────────────────────────────────────────────
        Rectangle {
            Layout.fillWidth: true; height: 56; radius: 14
            color: confirmPopup.surface2
            Rectangle { anchors.left: parent.left; anchors.right: parent.right; anchors.bottom: parent.bottom; height: 14; color: parent.color }
            RowLayout {
                anchors.fill: parent; anchors.leftMargin: 20; anchors.rightMargin: 14
                Label {
                    text: confirmPopup.title
                    font.pixelSize: 15; font.weight: Font.DemiBold; color: confirmPopup.textPrimary
                    Layout.fillWidth: true
                }
                Rectangle {
                    width: 30; height: 30; radius: 8; color: "transparent"
                    Label { anchors.centerIn: parent; text: "✕"; font.pixelSize: 14; color: confirmPopup.textMuted }
                    MouseArea { anchors.fill: parent; cursorShape: Qt.PointingHandCursor
                        onClicked: { confirmPopup.rejected(); confirmPopup.close() } }
                }
            }
        }
        Rectangle { Layout.fillWidth: true; height: 1; color: confirmPopup.borderCol }

        // ── Message ───────────────────────────────────────────────────────────
        Label {
            Layout.fillWidth: true; Layout.margins: 20
            text: confirmPopup.message
            font.pixelSize: 13; color: confirmPopup.textPrimary; wrapMode: Text.Wrap
        }

        Rectangle { Layout.fillWidth: true; height: 1; color: confirmPopup.borderCol }

        // ── Footer ────────────────────────────────────────────────────────────
        Rectangle {
            Layout.fillWidth: true; height: 60; radius: 14
            color: confirmPopup.surface2
            Rectangle { anchors.left: parent.left; anchors.right: parent.right; anchors.top: parent.top; height: 14; color: parent.color }
            RowLayout {
                anchors.fill: parent; anchors.leftMargin: 20; anchors.rightMargin: 20; spacing: 10
                Item { Layout.fillWidth: true }
                Rectangle {
                    height: 34; width: cnclLbl.implicitWidth + 24; radius: 8
                    color: "transparent"; border.width: 1; border.color: confirmPopup.borderCol
                    Label { id: cnclLbl; anchors.centerIn: parent; text: confirmPopup.cancelText
                            font.pixelSize: 13; color: confirmPopup.textMuted }
                    MouseArea { anchors.fill: parent; cursorShape: Qt.PointingHandCursor
                        onClicked: { confirmPopup.rejected(); confirmPopup.close() } }
                }
                Rectangle {
                    height: 34; width: cfrmLbl.implicitWidth + 24; radius: 8
                    color: confirmPopup.destructive ? "#ef4444" : confirmPopup.accent
                    Label { id: cfrmLbl; anchors.centerIn: parent; text: confirmPopup.confirmText
                            font.pixelSize: 13; font.weight: Font.DemiBold; color: "#fff" }
                    MouseArea { anchors.fill: parent; cursorShape: Qt.PointingHandCursor
                        onClicked: { confirmPopup.accepted(); confirmPopup.close() } }
                }
            }
        }
    }
}
