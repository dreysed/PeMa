import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: root
    color: bg

    property color bg: "#f0f2f5"
    property color surface: "#ffffff"
    property color surface2: "#f6f8fa"
    property color borderCol: "#dde3eb"
    property color textPrimary: "#0d1117"
    property color textMuted: "#57606a"
    property color accent: "#6366f1"
    property color runColor: "#22c55e"
    property color hardColor: "#ef4444"
    property bool dark: false
    property bool isBusy: false
    property bool canApply: false
    property string athleteName: ""
    property var report: ({})
    property var chatMessages: []
    property string chatDraft: ""

    signal refreshRequested(int horizonDays)
    signal applyRequested(int horizonDays)
    signal chatMessageRequested(string message, int horizonDays)

    function addChatReply(message) {
        var next = chatMessages.slice()
        next.push({ role: "ai", text: message })
        chatMessages = next
    }

    function addUserMessage(message) {
        var next = chatMessages.slice()
        next.push({ role: "coach", text: message })
        chatMessages = next
    }

    function riskText(v) {
        if (v === "high") return "Высокий"
        if (v === "medium") return "Средний"
        return "Низкий"
    }
    function riskColor(v) {
        if (v === "high") return hardColor
        if (v === "medium") return "#f59e0b"
        return runColor
    }
    function focusText(v) {
        if (v === "recover") return "Восстановление"
        if (v === "stabilize") return "Стабилизация"
        if (v === "rebuild") return "Возврат объема"
        return "Развитие"
    }
    function intensityText(v) {
        if (v === "easy") return "Легко"
        if (v === "hard") return "Тяжело"
        return "Умеренно"
    }

    ScrollView {
        anchors.fill: parent
        contentWidth: availableWidth
        ScrollBar.horizontal.policy: ScrollBar.AlwaysOff

        ColumnLayout {
            width: parent.width
            spacing: 14
            anchors { leftMargin: 20; rightMargin: 20; topMargin: 20; bottomMargin: 20 }

            Rectangle {
                Layout.fillWidth: true
                height: 112
                radius: 8
                color: surface
                border.width: 1
                border.color: borderCol

                RowLayout {
                    anchors.fill: parent
                    anchors.margins: 18
                    spacing: 16

                    Rectangle {
                        width: 46; height: 46; radius: 8
                        color: dark ? "#1f2937" : "#eef2ff"
                        Label {
                            anchors.centerIn: parent
                            text: "AI"
                            color: accent
                            font.pixelSize: 15
                            font.weight: Font.Black
                        }
                    }

                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 4
                        Label {
                            text: "AI Coach"
                            color: textPrimary
                            font.pixelSize: 20
                            font.weight: Font.Black
                        }
                        Label {
                            Layout.fillWidth: true
                            text: athleteName ? ("Атлет: " + athleteName) : "Выберите атлета для анализа"
                            color: textMuted
                            font.pixelSize: 13
                            elide: Text.ElideRight
                        }
                        Row {
                            spacing: 8
                            Rectangle {
                                height: 24; width: riskLbl.implicitWidth + 18; radius: 12
                                color: riskColor(report.riskLevel) + "22"
                                Label {
                                    id: riskLbl
                                    anchors.centerIn: parent
                                    text: "Риск: " + riskText(report.riskLevel)
                                    color: riskColor(report.riskLevel)
                                    font.pixelSize: 11
                                    font.weight: Font.DemiBold
                                }
                            }
                            Rectangle {
                                height: 24; width: focusLbl.implicitWidth + 18; radius: 12
                                color: dark ? "#22272e" : "#f1f5f9"
                                Label {
                                    id: focusLbl
                                    anchors.centerIn: parent
                                    text: focusText(report.focus)
                                    color: textPrimary
                                    font.pixelSize: 11
                                    font.weight: Font.DemiBold
                                }
                            }
                        }
                    }

                    SpinBox {
                        id: horizon
                        from: 7
                        to: 42
                        value: report.horizonDays || 14
                        stepSize: 7
                        editable: true
                    }
                    Button {
                        text: isBusy ? "Анализ..." : "Обновить"
                        enabled: !isBusy
                        onClicked: root.refreshRequested(horizon.value)
                    }
                    Button {
                        text: isBusy ? "Применение..." : "Применить план"
                        enabled: !isBusy && canApply && !!report.actions && report.actions.length > 0
                        highlighted: true
                        onClicked: root.applyRequested(horizon.value)
                    }
                }
            }

            GridLayout {
                Layout.fillWidth: true
                columns: 4
                columnSpacing: 10
                rowSpacing: 10

                Repeater {
                    model: [
                        { label: "Выполнено", value: (report.summary || {}).completedWorkouts || 0 },
                        { label: "Выполнение", value: Math.round(((report.summary || {}).completionRate || 0) * 100) + "%" },
                        { label: "Объем", value: ((report.summary || {}).distanceKm || 0) + " км" },
                        { label: "RPE", value: ((report.summary || {}).avgRpe || "нет") }
                    ]
                    delegate: Rectangle {
                        Layout.fillWidth: true
                        height: 76
                        radius: 8
                        color: surface
                        border.width: 1
                        border.color: borderCol
                        Column {
                            anchors { fill: parent; margins: 12 }
                            spacing: 5
                            Label { text: modelData.label; color: textMuted; font.pixelSize: 11 }
                            Label { text: modelData.value; color: textPrimary; font.pixelSize: 21; font.weight: Font.Black }
                        }
                    }
                }
            }

            RowLayout {
                Layout.fillWidth: true
                spacing: 14

                Rectangle {
                    Layout.fillWidth: true
                    Layout.preferredWidth: 1
                    Layout.fillHeight: true
                    radius: 8
                    color: surface
                    border.width: 1
                    border.color: borderCol
                    implicitHeight: 360

                    ColumnLayout {
                        anchors { fill: parent; margins: 14 }
                        spacing: 10
                        Label { text: "Рекомендации"; color: textPrimary; font.pixelSize: 15; font.weight: Font.Black }
                        Repeater {
                            model: report.recommendations || []
                            delegate: Rectangle {
                                Layout.fillWidth: true
                                height: Math.max(74, recCol.implicitHeight + 20)
                                radius: 8
                                color: surface2
                                border.width: 1
                                border.color: borderCol
                                ColumnLayout {
                                    id: recCol
                                    anchors { fill: parent; margins: 10 }
                                    spacing: 4
                                    Label { text: modelData.title; color: textPrimary; font.pixelSize: 13; font.weight: Font.DemiBold; Layout.fillWidth: true; wrapMode: Text.Wrap }
                                    Label { text: modelData.detail; color: textMuted; font.pixelSize: 12; Layout.fillWidth: true; wrapMode: Text.Wrap }
                                }
                            }
                        }
                        Label {
                            visible: !(report.recommendations && report.recommendations.length)
                            text: "Данных пока мало: добавьте выполненные тренировки, самочувствие и импорт с часов."
                            color: textMuted
                            wrapMode: Text.Wrap
                            Layout.fillWidth: true
                        }
                    }
                }

                Rectangle {
                    Layout.fillWidth: true
                    Layout.preferredWidth: 1
                    Layout.fillHeight: true
                    radius: 8
                    color: surface
                    border.width: 1
                    border.color: borderCol
                    implicitHeight: 360

                    ColumnLayout {
                        anchors { fill: parent; margins: 14 }
                        spacing: 10
                        Label { text: "Будущий план"; color: textPrimary; font.pixelSize: 15; font.weight: Font.Black }
                        
                        // Goals context section
                        Loader {
                            Layout.fillWidth: true
                            active: report.summary && report.summary.activeGoals && report.summary.activeGoals.length > 0
                            sourceComponent: ColumnLayout {
                                spacing: 6
                                Label { 
                                    text: "Цели атлета:"; 
                                    color: accent; 
                                    font.pixelSize: 12; 
                                    font.weight: Font.DemiBold 
                                }
                                Repeater {
                                    model: report.summary.activeGoals || []
                                    delegate: RowLayout {
                                        spacing: 6
                                        Rectangle {
                                            width: 4; height: 16; radius: 2
                                            color: modelData.daysLeft && modelData.daysLeft < 30 ? "#f59e0b" : runColor
                                        }
                                        Label { 
                                            text: modelData.title + (modelData.daysLeft ? " · " + modelData.daysLeft + " дн." : ""); 
                                            color: textMuted; 
                                            font.pixelSize: 11;
                                            elide: Text.ElideRight
                                            Layout.fillWidth: true
                                        }
                                    }
                                }
                            }
                        }
                        
                        // Success/failure patterns
                        Loader {
                            Layout.fillWidth: true
                            active: report.summary && (report.summary.successPatterns || []).length > 0
                            sourceComponent: ColumnLayout {
                                spacing: 4
                                Label { 
                                    text: "Успешные паттерны:"; 
                                    color: runColor; 
                                    font.pixelSize: 11; 
                                    font.weight: Font.DemiBold 
                                }
                                Repeater {
                                    model: report.summary.successPatterns || []
                                    delegate: Label { 
                                        text: "• " + modelData; 
                                        color: textMuted; 
                                        font.pixelSize: 10;
                                        wrapMode: Text.Wrap
                                        Layout.fillWidth: true
                                    }
                                }
                            }
                        }
                        
                        // Scrollable actions list with fixed height
                        Rectangle {
                            Layout.fillWidth: true
                            height: 180
                            color: "transparent"
                            clip: true
                            
                            ScrollView {
                                anchors.fill: parent
                                contentWidth: availableWidth
                                ScrollBar.horizontal.policy: ScrollBar.AlwaysOff
                                ScrollBar.vertical.policy: ScrollBar.AsNeeded
                                
                                ColumnLayout {
                                    width: parent.width
                                    spacing: 6
                                    
                                    Repeater {
                                        model: report.actions || []
                                        delegate: Rectangle {
                                            Layout.fillWidth: true
                                            height: 64
                                            radius: 8
                                            color: surface2
                                            border.width: 1
                                            border.color: borderCol
                                            RowLayout {
                                                anchors { fill: parent; margins: 10 }
                                                spacing: 10
                                                Label { text: modelData.date; color: textMuted; font.pixelSize: 11; Layout.preferredWidth: 78 }
                                                ColumnLayout {
                                                    Layout.fillWidth: true
                                                    spacing: 2
                                                    Label { text: modelData.title; color: textPrimary; font.pixelSize: 13; font.weight: Font.DemiBold; elide: Text.ElideRight; Layout.fillWidth: true }
                                                    Label { text: modelData.distanceKm + " км · " + modelData.durationMin + " мин · " + intensityText(modelData.intensity); color: textMuted; font.pixelSize: 11 }
                                                }
                                            }
                                        }
                                    }
                                    
                                    // Empty state inside ScrollView
                                    Label {
                                        visible: !(report.actions && report.actions.length)
                                        text: "Нет запланированных действий. Нажмите «Обновить» для анализа."
                                        color: textMuted
                                        wrapMode: Text.Wrap
                                        Layout.fillWidth: true
                                        Layout.margins: 10
                                    }
                                }
                            }
                        }
                    }
                }
            }

            Rectangle {
                Layout.fillWidth: true
                height: 340
                radius: 8
                color: surface
                border.width: 1
                border.color: borderCol

                ColumnLayout {
                    anchors { fill: parent; margins: 14 }
                    spacing: 10

                    RowLayout {
                        Layout.fillWidth: true
                        Label {
                            text: "Чат с AI Coach"
                            color: textPrimary
                            font.pixelSize: 15
                            font.weight: Font.Black
                            Layout.fillWidth: true
                        }
                        Label {
                            text: report.modelMode || ""
                            color: textMuted
                            font.pixelSize: 11
                        }
                    }

                    Label {
                        visible: report.cloudError && report.cloudError.length > 0
                        Layout.fillWidth: true
                        text: "Cloud: " + report.cloudError
                        color: hardColor
                        font.pixelSize: 11
                        wrapMode: Text.Wrap
                    }

                    ListView {
                        id: chatList
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        clip: true
                        spacing: 8
                        model: root.chatMessages
                        delegate: Rectangle {
                            width: chatList.width
                            height: bubble.implicitHeight + 14
                            color: "transparent"
                            Rectangle {
                                id: bubble
                                width: Math.min(parent.width * 0.78, body.implicitWidth + 26)
                                anchors.right: modelData.role === "coach" ? parent.right : undefined
                                anchors.left: modelData.role === "coach" ? undefined : parent.left
                                radius: 8
                                color: modelData.role === "coach" ? accent : surface2
                                border.width: modelData.role === "coach" ? 0 : 1
                                border.color: borderCol
                                implicitHeight: body.implicitHeight + 16
                                Label {
                                    id: body
                                    anchors { left: parent.left; right: parent.right; top: parent.top; margins: 8 }
                                    text: modelData.text
                                    color: modelData.role === "coach" ? "#ffffff" : textPrimary
                                    font.pixelSize: 12
                                    wrapMode: Text.Wrap
                                }
                            }
                        }
                        onCountChanged: Qt.callLater(positionViewAtEnd)
                    }

                    RowLayout {
                        Layout.fillWidth: true
                        spacing: 8
                        TextArea {
                            id: chatInput
                            Layout.fillWidth: true
                            Layout.preferredHeight: 58
                            placeholderText: "Например: снизь нагрузку на неделю, объясни состояние спортсмена, предложи корректировки"
                            text: root.chatDraft
                            wrapMode: TextArea.Wrap
                            onTextChanged: root.chatDraft = text
                        }
                        Button {
                            text: isBusy ? "Жду..." : "Отправить"
                            enabled: !isBusy && root.chatDraft.trim().length > 0
                            highlighted: true
                            onClicked: {
                                var msg = root.chatDraft.trim()
                                root.chatDraft = ""
                                chatInput.text = ""
                                root.addUserMessage(msg)
                                root.chatMessageRequested(msg, horizon.value)
                            }
                        }
                    }
                }
            }
        }
    }
}
