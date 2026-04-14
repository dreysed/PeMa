import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: root
    property string message: ""
    signal dismissed()

    visible: message.length > 0
    color: "#ffebee"
    border.color: "#ef9a9a"
    border.width: 1
    radius: 8
    implicitHeight: 40

    RowLayout {
        anchors.fill: parent
        anchors.margins: 8
        spacing: 8

        Label {
            Layout.fillWidth: true
            text: root.message
            color: "#b71c1c"
            elide: Text.ElideRight
            font.pixelSize: 12
        }

        ToolButton {
            text: "×"
            onClicked: root.dismissed()
        }
    }
}
