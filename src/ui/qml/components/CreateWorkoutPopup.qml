import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Popup {
    id: root
    modal: true
    focus: true
    anchors.centerIn: Overlay.overlay
    width: 500
    height: 560
    closePolicy: Popup.NoAutoClose

    property string dialogTitle: "Новая тренировка"
    property string draftDateIso: ""
    property string workoutTitle: ""
    property string workoutCategory: "run"
    property real workoutDistance: 5
    property int workoutDuration: 45
    property string workoutIntensity: "moderate"
    property string workoutNotes: ""
    property bool workoutHidden: false
    property string workoutIntervals: "[]"
    property string errorText: ""
    property bool saveEnabled: true
    property string saveDisabledHint: ""
    property bool busy: false
    property var categories: []
    property var intensities: []
    property int uiControlHeight: 34
    property int uiSpacing: 8
    property int uiMargin: 14

    signal cancelRequested()
    signal saveRequested(
        string title,
        string category,
        real distanceKm,
        int durationMin,
        string intensity,
        string notes,
        bool hiddenFromAthlete,
        string intervalsJson
    )

    onClosed: cancelRequested()

    background: Rectangle {
        color: "#ffffff"
        radius: 10
        border.width: 1
        border.color: "#cfd8dc"
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: uiMargin
        spacing: uiSpacing

        Label {
            text: root.dialogTitle
            font.bold: true
            font.pixelSize: 16
        }
        Label {
            text: "Дата: " + root.draftDateIso
            color: "#455a64"
        }

        Label { text: "Категория" }
        ComboBox {
            Layout.fillWidth: true
            implicitHeight: uiControlHeight
            model: root.categories
            currentIndex: Math.max(0, model.indexOf(root.workoutCategory))
            enabled: !root.busy
            onActivated: root.workoutCategory = currentText
        }

        Label { text: "Название" }
        TextField {
            Layout.fillWidth: true
            implicitHeight: uiControlHeight
            text: root.workoutTitle
            placeholderText: "Например: Бег - интервалы"
            enabled: !root.busy
            onTextChanged: root.workoutTitle = text
        }

        RowLayout {
            Layout.fillWidth: true
            Label { text: "Дистанция (км)" }
            SpinBox {
                implicitHeight: uiControlHeight
                from: 0
                to: 300
                value: Math.round(root.workoutDistance)
                enabled: !root.busy
                onValueModified: root.workoutDistance = value
            }
            Label { text: "Длительность (мин)" }
            SpinBox {
                implicitHeight: uiControlHeight
                from: 0
                to: 500
                value: root.workoutDuration
                enabled: !root.busy
                onValueModified: root.workoutDuration = value
            }
        }

        Label { text: "Интенсивность" }
        ComboBox {
            Layout.fillWidth: true
            implicitHeight: uiControlHeight
            model: root.intensities
            currentIndex: Math.max(0, model.indexOf(root.workoutIntensity))
            enabled: !root.busy
            onActivated: root.workoutIntensity = currentText
        }

        CheckBox {
            text: "Скрыть от атлета"
            checked: root.workoutHidden
            enabled: !root.busy
            onToggled: root.workoutHidden = checked
        }

        Label { text: "Интервалы (JSON-массив)" }
        TextArea {
            Layout.fillWidth: true
            Layout.preferredHeight: 80
            text: root.workoutIntervals
            enabled: !root.busy
            onTextChanged: root.workoutIntervals = text
        }

        Label { text: "Заметки" }
        TextArea {
            Layout.fillWidth: true
            Layout.fillHeight: true
            text: root.workoutNotes
            placeholderText: "Пульс, темп, ощущения..."
            enabled: !root.busy
            onTextChanged: root.workoutNotes = text
        }

        Label {
            text: root.errorText
            color: "#c62828"
            visible: errorText.length > 0
        }

        RowLayout {
            Layout.fillWidth: true
            Item { Layout.fillWidth: true }
            Button {
                text: "Отмена"
                implicitHeight: uiControlHeight
                enabled: !root.busy
                onClicked: root.cancelRequested()
            }
            Button {
                text: "Сохранить"
                implicitHeight: uiControlHeight
                highlighted: true
                enabled: root.saveEnabled && !root.busy
                onClicked: {
                    root.saveRequested(
                        root.workoutTitle,
                        root.workoutCategory,
                        root.workoutDistance,
                        root.workoutDuration,
                        root.workoutIntensity,
                        root.workoutNotes,
                        root.workoutHidden,
                        root.workoutIntervals
                    )
                }
            }
        }

        Label {
            Layout.fillWidth: true
            visible: !root.saveEnabled && root.saveDisabledHint.length > 0
            text: root.saveDisabledHint
            color: "#6b7280"
            wrapMode: Text.Wrap
        }
    }
}
