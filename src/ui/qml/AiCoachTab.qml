import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item {
    id: root

    // ── Theme ─────────────────────────────────────────────────────────────────
    property color bg:          "#f0f2f5"
    property color surface:     "#ffffff"
    property color surface2:    "#f6f8fa"
    property color borderCol:   "#dde3eb"
    property color textPrimary: "#0d1117"
    property color textMuted:   "#57606a"
    property color accent:      "#6366f1"
    property color runColor:    "#22c55e"
    property bool  dark: false

    // ── Store bindings ────────────────────────────────────────────────────────
    property var    store: null

    property var    chatHistory: store ? store.chatHistory  : []
    property bool   aiTyping:    store ? store.aiTyping     : false
    property bool   aiAvailable: store ? store.aiAvailable  : false
    property var    goals:       store ? store.goals         : []
    property var    analytics:   store ? store.analyticsSummary : ({})
    property string athleteName: store ? store.selectedAthleteName : ""

    // ── Layout ────────────────────────────────────────────────────────────────
    RowLayout {
        anchors.fill: parent
        spacing: 0

        // ══ Left sidebar ══════════════════════════════════════════════════════
        Rectangle {
            Layout.preferredWidth: 240
            Layout.fillHeight: true
            color: root.surface

            Rectangle {
                anchors.right: parent.right
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                width: 1
                color: root.borderCol
            }

            ScrollView {
                id: sideScroll
                anchors.fill: parent
                contentWidth: availableWidth
                clip: true
                ScrollBar.horizontal.policy: ScrollBar.AlwaysOff

                Column {
                    width: sideScroll.availableWidth
                    spacing: 0

                    // Header
                    Item {
                        width: parent.width
                        height: 64
                        Column {
                            anchors.left: parent.left
                            anchors.right: parent.right
                            anchors.verticalCenter: parent.verticalCenter
                            anchors.leftMargin: 20
                            anchors.rightMargin: 20
                            spacing: 2
                            Label {
                                text: "AI Тренер"
                                font.pixelSize: 17
                                font.weight: Font.Black
                                color: root.textPrimary
                            }
                            Label {
                                text: "На базе Gemini 2.0 · Google"
                                font.pixelSize: 11
                                color: root.textMuted
                            }
                        }
                    }

                    Rectangle { width: parent.width; height: 1; color: root.borderCol }

                    Item { width: parent.width; height: 16 }

                    // ── Athlete context ───────────────────────────────────────
                    Column {
                        width: parent.width - 32
                        x: 16
                        spacing: 8
                        visible: root.athleteName !== ""

                        Label {
                            text: "АТЛЕТ"
                            font.pixelSize: 9
                            font.weight: Font.Black
                            color: root.textMuted
                            font.letterSpacing: 1.2
                        }

                        Rectangle {
                            width: parent.width
                            height: athleteInner.implicitHeight + 20
                            radius: 10
                            color: root.surface2
                            border.width: 1
                            border.color: root.borderCol

                            Column {
                                id: athleteInner
                                anchors.left: parent.left
                                anchors.right: parent.right
                                anchors.top: parent.top
                                anchors.margins: 12
                                spacing: 8

                                Label {
                                    text: root.athleteName
                                    font.pixelSize: 13
                                    font.weight: Font.DemiBold
                                    color: root.textPrimary
                                    width: parent.width
                                    elide: Text.ElideRight
                                }

                                // Goals
                                Column {
                                    width: parent.width
                                    spacing: 4
                                    visible: root.goals.length > 0

                                    Label {
                                        text: "Цели (" + root.goals.length + ")"
                                        font.pixelSize: 10
                                        font.weight: Font.DemiBold
                                        color: root.textMuted
                                    }

                                    Repeater {
                                        model: Math.min(root.goals.length, 3)
                                        delegate: RowLayout {
                                            width: parent.width
                                            spacing: 6
                                            Label { text: "🎯"; font.pixelSize: 11 }
                                            Label {
                                                text: root.goals[index].title || ""
                                                font.pixelSize: 11
                                                color: root.textPrimary
                                                Layout.fillWidth: true
                                                elide: Text.ElideRight
                                            }
                                            Label {
                                                text: Math.round((root.goals[index].progress || 0) * 100) + "%"
                                                font.pixelSize: 10
                                                color: root.accent
                                            }
                                        }
                                    }
                                }

                                // 30d stats
                                RowLayout {
                                    width: parent.width
                                    spacing: 0
                                    Repeater {
                                        model: [
                                            { label: "Тренировок", value: (root.analytics.workoutsCount || 0) + "" },
                                            { label: "Км",         value: Math.round(root.analytics.distanceTotal || 0) + "" },
                                            { label: "Мин",        value: (root.analytics.durationTotal || 0) + "" }
                                        ]
                                        delegate: Column {
                                            Layout.fillWidth: true
                                            spacing: 2
                                            Label {
                                                anchors.horizontalCenter: parent.horizontalCenter
                                                text: modelData.value
                                                font.pixelSize: 16
                                                font.weight: Font.Black
                                                color: root.accent
                                            }
                                            Label {
                                                anchors.horizontalCenter: parent.horizontalCenter
                                                text: modelData.label
                                                font.pixelSize: 9
                                                color: root.textMuted
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }

                    Item { width: parent.width; height: 16 }

                    // ── Clear chat ────────────────────────────────────────────
                    Rectangle {
                        width: parent.width - 32
                        x: 16
                        height: 36
                        radius: 9
                        color: "transparent"
                        border.width: 1
                        border.color: root.borderCol
                        visible: root.chatHistory.length > 0

                        RowLayout {
                            anchors.fill: parent
                            anchors.leftMargin: 12
                            anchors.rightMargin: 12
                            spacing: 8
                            Label { text: "🗑"; font.pixelSize: 13 }
                            Label {
                                text: "Новая сессия"
                                font.pixelSize: 12
                                color: root.textMuted
                                Layout.fillWidth: true
                            }
                        }
                        MouseArea {
                            anchors.fill: parent
                            cursorShape: Qt.PointingHandCursor
                            onClicked: root.store && root.store.clearAiChat()
                        }
                    }

                    Item { width: parent.width; height: 20 }
                }
            }
        }

        // ══ Chat area ═════════════════════════════════════════════════════════
        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: root.bg

            ColumnLayout {
                anchors.fill: parent
                spacing: 0

                // ── Messages ──────────────────────────────────────────────────
                Item {
                    Layout.fillWidth: true
                    Layout.fillHeight: true

                    // Empty state
                    Column {
                        anchors.centerIn: parent
                        spacing: 12
                        visible: root.chatHistory.length === 0 && !root.aiTyping

                        Label {
                            anchors.horizontalCenter: parent.horizontalCenter
                            text: "🏋️"
                            font.pixelSize: 48
                        }
                        Label {
                            anchors.horizontalCenter: parent.horizontalCenter
                            text: "Спросите AI тренера"
                            font.pixelSize: 16
                            font.weight: Font.DemiBold
                            color: root.textPrimary
                        }
                        Label {
                            anchors.horizontalCenter: parent.horizontalCenter
                            text: "Составит план, подскажет по восстановлению\nи ответит на вопросы о тренировках"
                            font.pixelSize: 13
                            color: root.textMuted
                            horizontalAlignment: Text.AlignHCenter
                        }

                        Item { width: 1; height: 4 }

                        // Suggestion chips
                        Flow {
                            anchors.horizontalCenter: parent.horizontalCenter
                            width: 460
                            spacing: 8
                            Repeater {
                                model: [
                                    "Составь план на эту неделю",
                                    "Как восстановиться после забега?",
                                    "Темп для марафона",
                                    "Тренировка с больным коленом"
                                ]
                                delegate: Rectangle {
                                    height: 32
                                    width: chipLabel.implicitWidth + 24
                                    radius: 16
                                    color: root.surface
                                    border.width: 1
                                    border.color: root.borderCol
                                    Label {
                                        id: chipLabel
                                        anchors.centerIn: parent
                                        text: modelData
                                        font.pixelSize: 12
                                        color: root.accent
                                    }
                                    MouseArea {
                                        anchors.fill: parent
                                        cursorShape: Qt.PointingHandCursor
                                        onClicked: {
                                            msgField.text = modelData
                                            sendMessage()
                                        }
                                    }
                                }
                            }
                        }
                    }

                    // Messages
                    ScrollView {
                        id: chatScroll
                        anchors.fill: parent
                        contentWidth: availableWidth
                        clip: true
                        visible: root.chatHistory.length > 0 || root.aiTyping

                        Column {
                            id: chatCol
                            width: chatScroll.availableWidth
                            padding: 20
                            spacing: 12

                            Repeater {
                                model: root.chatHistory
                                delegate: Item {
                                    width: chatCol.width - 40
                                    height: bubble.implicitHeight + 8
                                    property bool isUser: modelData.role === "user"

                                    Rectangle {
                                        id: bubble
                                        anchors.right: isUser ? parent.right : undefined
                                        anchors.left:  isUser ? undefined    : parent.left
                                        width: Math.min(implicitWidth, parent.width * 0.78)
                                        implicitWidth: bubbleText.implicitWidth + 24
                                        implicitHeight: bubbleText.implicitHeight + 18
                                        radius: 12
                                        color: isUser ? root.accent : root.surface
                                        border.width: isUser ? 0 : 1
                                        border.color: root.borderCol

                                        Label {
                                            id: bubbleText
                                            anchors.left: parent.left
                                            anchors.right: parent.right
                                            anchors.top: parent.top
                                            anchors.margins: 12
                                            text: modelData.content || ""
                                            font.pixelSize: 13
                                            color: isUser ? "#ffffff" : root.textPrimary
                                            wrapMode: Text.Wrap
                                            lineHeight: 1.45
                                        }
                                    }

                                    Label {
                                        anchors.top: bubble.bottom
                                        anchors.topMargin: 3
                                        anchors.right: isUser ? parent.right : undefined
                                        anchors.left:  isUser ? undefined    : parent.left
                                        text: modelData.ts || ""
                                        font.pixelSize: 10
                                        color: root.textMuted
                                        opacity: 0.7
                                    }
                                }
                            }

                            // Typing indicator
                            Item {
                                width: chatCol.width - 40
                                height: 48
                                visible: root.aiTyping
                                Rectangle {
                                    width: 72; height: 36; radius: 12
                                    color: root.surface
                                    border.width: 1; border.color: root.borderCol
                                    Row {
                                        anchors.centerIn: parent
                                        spacing: 6
                                        Repeater {
                                            model: 3
                                            delegate: Rectangle {
                                                width: 7; height: 7; radius: 4
                                                color: root.textMuted
                                                opacity: 0.4
                                                SequentialAnimation on opacity {
                                                    running: root.aiTyping
                                                    loops: Animation.Infinite
                                                    PauseAnimation { duration: index * 200 }
                                                    NumberAnimation { to: 1.0; duration: 300 }
                                                    NumberAnimation { to: 0.4; duration: 300 }
                                                    PauseAnimation { duration: (2 - index) * 200 }
                                                }
                                            }
                                        }
                                    }
                                }
                            }

                            Item { width: 1; height: 4 }
                        }
                    }

                    Connections {
                        target: root
                        function onChatHistoryChanged() {
                            chatScroll.ScrollBar.vertical.position = 1.0
                        }
                        function onAiTypingChanged() {
                            if (root.aiTyping)
                                chatScroll.ScrollBar.vertical.position = 1.0
                        }
                    }
                }

                // ── Input bar ─────────────────────────────────────────────────
                Rectangle {
                    Layout.fillWidth: true
                    height: inputRow.implicitHeight + 24
                    color: root.surface

                    Rectangle {
                        anchors.left: parent.left
                        anchors.right: parent.right
                        anchors.top: parent.top
                        height: 1
                        color: root.borderCol
                    }

                    RowLayout {
                        id: inputRow
                        anchors.left: parent.left
                        anchors.right: parent.right
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.leftMargin: 16
                        anchors.rightMargin: 16
                        spacing: 10

                        ScrollView {
                            Layout.fillWidth: true
                            implicitHeight: Math.min(msgField.implicitHeight, 120)
                            clip: true
                            ScrollBar.horizontal.policy: ScrollBar.AlwaysOff

                            TextArea {
                                id: msgField
                                placeholderText: root.aiTyping
                                    ? "AI думает…"
                                    : "Спросите тренера о тренировках…"
                                enabled: !root.aiTyping
                                font.pixelSize: 13
                                color: root.textPrimary
                                wrapMode: TextArea.Wrap
                                background: Rectangle {
                                    radius: 10
                                    color: root.surface2
                                    border.width: 1
                                    border.color: msgField.activeFocus ? root.accent : root.borderCol
                                    Behavior on border.color { ColorAnimation { duration: 120 } }
                                }
                                leftPadding: 12; rightPadding: 12
                                topPadding: 10; bottomPadding: 10

                                Keys.onPressed: function(event) {
                                    if ((event.key === Qt.Key_Return || event.key === Qt.Key_Enter)
                                            && !(event.modifiers & Qt.ShiftModifier)) {
                                        sendMessage()
                                        event.accepted = true
                                    }
                                }
                            }
                        }

                        Rectangle {
                            width: 40; height: 40; radius: 10
                            color: (msgField.text.trim().length > 0 && !root.aiTyping)
                                   ? root.accent : root.borderCol
                            Behavior on color { ColorAnimation { duration: 150 } }

                            Label {
                                anchors.centerIn: parent
                                text: "↑"
                                font.pixelSize: 18
                                font.weight: Font.Bold
                                color: "#ffffff"
                            }
                            MouseArea {
                                anchors.fill: parent
                                cursorShape: Qt.PointingHandCursor
                                enabled: msgField.text.trim().length > 0 && !root.aiTyping
                                onClicked: sendMessage()
                            }
                        }
                    }
                }
            }
        }
    }

    function sendMessage() {
        const text = msgField.text.trim()
        if (!text || !root.store || root.aiTyping) return
        root.store.sendAiMessage(text)
        msgField.text = ""
    }
}
