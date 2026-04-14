import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "components"

ApplicationWindow {
    id: root
    visible: true
    width: 1500
    height: 900
    title: "SportApp Qt (Calendar)"
    property string themeMode: "light" // light, dark, system
    property bool useDarkTheme: themeMode === "dark" || (themeMode === "system" && Qt.styleHints.colorScheme === Qt.Dark)
    property real uiScale: Math.max(0.85, Math.min(1.15, (width / 1500) * (Qt.platform.os === "osx" ? 0.95 : 1.0)))
    property int uiControlHeight: Math.round(34 * uiScale)
    property int uiSmallControlHeight: Math.round(30 * uiScale)
    property int uiSectionSpacing: Math.round(10 * uiScale)
    property int uiItemSpacing: Math.round(6 * uiScale)
    property int uiPanelMargin: Math.round(10 * uiScale)
    property int uiCaptionSize: Math.round(11 * uiScale)
    property color appBgColor: useDarkTheme ? "#111827" : "#edf1f5"
    property color cardColor: useDarkTheme ? "#1f2937" : "#ffffff"
    property color borderColor: useDarkTheme ? "#374151" : "#dbe2ea"
    property color panelColor: useDarkTheme ? "#111827" : "#151f31"
    property color panelTextColor: useDarkTheme ? "#e5e7eb" : "#ecf2ff"
    property color primaryTextColor: useDarkTheme ? "#e5e7eb" : "#1f2937"
    property color mutedTextColor: useDarkTheme ? "#9ca3af" : "#607d8b"
    color: appBgColor
    font.family: Qt.platform.os === "osx" ? ".AppleSystemUIFont" : "Segoe UI"
    font.pixelSize: Math.round(13 * uiScale)
    palette {
        window: appBgColor
        base: cardColor
        alternateBase: useDarkTheme ? "#111827" : "#f8fafc"
        windowText: primaryTextColor
        text: useDarkTheme ? "#e5e7eb" : "#1f2937"
        button: useDarkTheme ? "#374151" : "#f3f4f6"
        buttonText: useDarkTheme ? "#f9fafb" : "#111827"
        highlight: useDarkTheme ? "#2563eb" : "#2f6fde"
        highlightedText: "#ffffff"
        brightText: "#ffffff"
        placeholderText: useDarkTheme ? "#9ca3af" : "#6b7280"
    }
    property var store: workoutStore

    property string draftTitle: ""
    property string draftCategory: "run"
    property real draftDistance: 5
    property int draftDuration: 45
    property string draftIntensity: "moderate"
    property string draftNotes: ""
    property bool draftHidden: false
    property string draftIntervals: "[]"
    property string editingWorkoutId: ""

    property string commentText: ""
    property string commentAuthor: "coach"
    property string tplTitle: ""
    property string tplCategory: "run"
    property real tplDistance: 10
    property int tplDuration: 50
    property string tplIntensity: "moderate"
    property string tplIntervals: "[{\"step\":\"10min warmup\"},{\"step\":\"main set\"}]"
    property string tplTags: ""
    property string tplNotes: ""
    property string selectedTemplateId: ""
    property string planDateIso: workoutStore.selectedDateIso
    property string feedbackDraft: ""
    property string statusDraft: "planned"
    property string moodDraft: ""
    property int perceivedExertionDraft: 0
    property string deleteWorkoutId: ""
    property string deleteTemplateId: ""
    property var selectedWorkoutObj: store ? store.selectedWorkout : ({})
    property var analyticsObj: store ? store.analyticsSummary : ({})
    property bool hasSelectedWorkout: !!(selectedWorkoutObj && selectedWorkoutObj.id)
    property bool isAuthenticated: false
    property string loginRole: "coach"
    property string loginUserId: ""

    function resetWorkoutDraft() {
        editingWorkoutId = ""
        draftTitle = ""
        draftCategory = "run"
        draftDistance = 5
        draftDuration = 45
        draftIntensity = "moderate"
        draftNotes = ""
        draftHidden = false
        draftIntervals = "[]"
    }

    function fillDraftFromSelected() {
        const selected = workoutStore.selectedWorkout
        if (!selected || !selected.id)
            return
        editingWorkoutId = selected.id
        draftTitle = selected.title || ""
        draftCategory = selected.category || "run"
        const distRaw = (selected.distance || "0").replace(" км", "")
        const durRaw = (selected.duration || "0").replace(" мин", "")
        draftDistance = Number(distRaw) || 0
        draftDuration = Number(durRaw) || 0
        draftIntensity = selected.intensity || "moderate"
        draftNotes = selected.notes || ""
        draftHidden = !!selected.hidden
        draftIntervals = selected.intervalsJson || "[]"
    }

    function statusIndex(value) {
        if (value === "done")
            return 1
        if (value === "skipped")
            return 2
        return 0
    }

    function moodLabel(value) {
        if (value === "excellent")
            return "Отлично"
        if (value === "good")
            return "Хорошо"
        if (value === "normal")
            return "Нормально"
        if (value === "weak")
            return "Слабость"
        if (value === "awful")
            return "Ужасно"
        return ""
    }

    function nextThemeMode() {
        if (themeMode === "light")
            themeMode = "dark"
        else if (themeMode === "dark")
            themeMode = "system"
        else
            themeMode = "light"
    }

    function themeLabel() {
        if (themeMode === "dark")
            return "Тема: тёмная"
        if (themeMode === "system")
            return "Тема: системная"
        return "Тема: светлая"
    }

    function roleUsers(role) {
        if (!store || !store.users)
            return []
        const list = []
        for (let i = 0; i < store.users.length; ++i) {
            const u = store.users[i]
            if (u.role === role)
                list.push(u)
        }
        return list
    }

    function syncLoginUser() {
        const users = roleUsers(loginRole)
        loginUserId = users.length > 0 ? users[0].id : ""
    }

    Connections {
        target: workoutStore
        function onWorkoutCreated() {
            resetWorkoutDraft()
        }
        function onSelectedDateChanged() {
            planDateIso = workoutStore.selectedDateIso
        }
        function onSelectedWorkoutChanged() {
            root.selectedWorkoutObj = workoutStore.selectedWorkout
            const selected = root.selectedWorkoutObj
            feedbackDraft = selected && selected.athleteFeedback ? selected.athleteFeedback : ""
            statusDraft = selected && selected.status ? selected.status : "planned"
            moodDraft = selected && selected.athleteMood ? selected.athleteMood : ""
            perceivedExertionDraft = selected && selected.perceivedExertion ? selected.perceivedExertion : 0
        }
        function onAnalyticsChanged() {
            root.analyticsObj = workoutStore.analyticsSummary
        }
        function onCurrentUserChanged() {
            commentAuthor = workoutStore.currentUserRole === "athlete" ? "athlete" : "coach"
        }
        function onUsersChanged() {
            syncLoginUser()
        }
    }

    Component.onCompleted: {
        root.selectedWorkoutObj = workoutStore.selectedWorkout
        root.analyticsObj = workoutStore.analyticsSummary
        loginRole = workoutStore.currentUserRole === "athlete" ? "athlete" : "coach"
        syncLoginUser()
    }

    ErrorBanner {
        id: errorBanner
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.margins: 8
        z: 10
        message: workoutStore.errorMessage
        onDismissed: workoutStore.clearError()
    }

    RowLayout {
        anchors.fill: parent
        anchors.topMargin: errorBanner.visible ? 54 : 10
        anchors.margins: 10
        spacing: uiSectionSpacing

        Rectangle {
            Layout.preferredWidth: 96
            Layout.fillHeight: true
            color: panelColor
            radius: 12

            Column {
                anchors.fill: parent
                anchors.margins: 10
                spacing: uiItemSpacing

                Label {
                    text: "Модули"
                    color: panelTextColor
                    font.bold: true
                }

                Repeater {
                    model: ["Календарь", "Builder", "Аналитика", "Тренер"]
                    delegate: Rectangle {
                        width: parent.width
                        height: uiControlHeight
                        radius: 6
                        color: moduleTabs.currentIndex === index ? (useDarkTheme ? "#374151" : "#253550") : "transparent"
                        MouseArea {
                            anchors.fill: parent
                            onClicked: moduleTabs.currentIndex = index
                        }
                        Label {
                            anchors.centerIn: parent
                            text: modelData
                            color: panelTextColor
                            font.pixelSize: 12
                        }
                    }
                }
            }
        }

        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: useDarkTheme ? "#0f172a" : "#f8fafc"
            radius: 12

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: uiPanelMargin
                spacing: uiSectionSpacing

                Frame {
                    Layout.fillWidth: true
                    padding: 8
                    background: Rectangle {
                        color: cardColor
                        radius: 8
                        border.width: 1
                        border.color: borderColor
                    }

                    ColumnLayout {
                        anchors.fill: parent
                        spacing: uiItemSpacing

                        RowLayout {
                            Layout.fillWidth: true
                            spacing: uiItemSpacing

                            Label {
                                text: "Профиль"
                                color: mutedTextColor
                                font.pixelSize: uiCaptionSize
                            }
                            ComboBox {
                                Layout.preferredWidth: Math.max(140, root.width * 0.12)
                                implicitHeight: uiControlHeight
                                model: workoutStore.users
                                textRole: "name"
                                valueRole: "id"
                                onActivated: function(index) {
                                    const selected = model[index]
                                    if (selected && selected.id)
                                        workoutStore.currentUserId = selected.id
                                }
                                Component.onCompleted: {
                                    for (let i = 0; i < model.length; ++i) {
                                        if (model[i].id === workoutStore.currentUserId) {
                                            currentIndex = i
                                            break
                                        }
                                    }
                                }
                            }

                            Label {
                                text: "Атлет"
                                color: mutedTextColor
                                font.pixelSize: uiCaptionSize
                            }
                            ComboBox {
                                Layout.preferredWidth: Math.max(140, root.width * 0.14)
                                implicitHeight: uiControlHeight
                                model: workoutStore.athletes
                                textRole: "name"
                                valueRole: "id"
                                onActivated: function(index) {
                                    const selected = model[index]
                                    if (selected && selected.id)
                                        workoutStore.selectedAthleteId = selected.id
                                }
                                Component.onCompleted: {
                                    for (let i = 0; i < model.length; ++i) {
                                        if (model[i].id === workoutStore.selectedAthleteId) {
                                            currentIndex = i
                                            break
                                        }
                                    }
                                }
                            }
                            Item { Layout.fillWidth: true }
                            Button {
                                text: themeLabel()
                                implicitHeight: uiControlHeight
                                onClicked: nextThemeMode()
                            }
                            Button {
                                text: "Сменить вход"
                                implicitHeight: uiControlHeight
                                onClicked: {
                                    loginRole = workoutStore.currentUserRole === "athlete" ? "athlete" : "coach"
                                    syncLoginUser()
                                    isAuthenticated = false
                                }
                            }
                        }

                        RowLayout {
                            Layout.fillWidth: true
                            spacing: uiItemSpacing
                            Button {
                                text: "Сегодня"
                                implicitHeight: uiControlHeight
                                onClicked: workoutStore.goToToday()
                            }
                            Button {
                                text: "◀"
                                implicitHeight: uiControlHeight
                                onClicked: workoutStore.prevMonth()
                            }
                            Label {
                                text: workoutStore.monthLabel
                                font.bold: true
                                Layout.fillWidth: true
                                horizontalAlignment: Text.AlignHCenter
                            }
                            Button {
                                text: "▶"
                                implicitHeight: uiControlHeight
                                onClicked: workoutStore.nextMonth()
                            }
                            ToolButton {
                                text: "Месяц"
                                checkable: true
                                checked: true
                                enabled: false
                            }
                        }
                    }
                }

                TabBar {
                    id: moduleTabs
                    Layout.fillWidth: true
                    TabButton { text: "Календарь" }
                    TabButton { text: "Workout Builder" }
                    TabButton { text: "Аналитика" }
                    TabButton { text: "Тренерский workspace" }
                }

                StackLayout {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    currentIndex: moduleTabs.currentIndex

                    Rectangle {
                        radius: 8
                        color: cardColor
                        border.width: 1
                        border.color: borderColor
                        Layout.fillWidth: true
                        Layout.fillHeight: true

                        ColumnLayout {
                            anchors.fill: parent
                            anchors.margins: 8
                            spacing: uiItemSpacing

                            RowLayout {
                                Layout.fillWidth: true
                                Repeater {
                                    model: ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
                                    delegate: Label {
                                        Layout.fillWidth: true
                                        horizontalAlignment: Text.AlignHCenter
                                        text: modelData
                                        color: "#546e7a"
                                        font.bold: true
                                    }
                                }
                            }

                            GridLayout {
                                Layout.fillWidth: true
                                Layout.fillHeight: true
                                columns: 7
                                rowSpacing: 5
                                columnSpacing: uiItemSpacing

                                Repeater {
                                    model: workoutStore.dayCells
                                    delegate: Rectangle {
                                        Layout.fillWidth: true
                                        Layout.fillHeight: true
                                        radius: 6
                                        color: modelData.background
                                        border.width: modelData.isSelected ? 2 : 1
                                        border.color: modelData.isToday ? "#2f6fde" : "#dde4ed"

                                        property var dayData: modelData

                                        MouseArea {
                                            id: hoverArea
                                            anchors.fill: parent
                                            hoverEnabled: true
                                            onClicked: workoutStore.selectDate(dayData.dateIso)
                                        }

                                        Button {
                                            anchors.top: parent.top
                                            anchors.right: parent.right
                                            anchors.margins: 4
                                            width: 22
                                            height: 22
                                            text: "+"
                                            visible: hoverArea.containsMouse && workoutStore.canEditWorkouts
                                            onClicked: {
                                                resetWorkoutDraft()
                                                workoutStore.openCreateDialogForDate(dayData.dateIso)
                                            }
                                        }

                                        Column {
                                            anchors.fill: parent
                                            anchors.margins: 5
                                            spacing: 3

                                            Label {
                                                text: dayData.dayNumber
                                                color: dayData.inCurrentMonth ? "#263238" : "#9aa6b2"
                                                font.bold: true
                                            }

                                            Repeater {
                                                model: dayData.workouts
                                                delegate: Rectangle {
                                                    width: parent.width
                                                    height: 42
                                                    radius: 4
                                                    color: cardColor
                                                    border.width: 1
                                                    border.color: modelData.intensityColor

                                                    MouseArea {
                                                        anchors.fill: parent
                                                        onClicked: {
                                                            root.store.selectDate(dayData.dateIso)
                                                            root.store.selectWorkout(modelData.id)
                                                        }
                                                    }

                                                    Column {
                                                        anchors.fill: parent
                                                        anchors.margins: 3
                                                        spacing: 0
                                                        Label { text: modelData.typeIcon + " " + modelData.title; elide: Text.ElideRight; width: parent.width; font.pixelSize: 10 }
                                                        Label { text: modelData.distance + " • " + modelData.duration + " • " + modelData.status; color: mutedTextColor; font.pixelSize: 10 }
                                                        Label { text: modelData.intensityLabel + (modelData.hidden ? " • скрыто" : ""); color: modelData.intensityColor; font.pixelSize: 10 }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }

                    Rectangle {
                        radius: 8
                        color: cardColor
                        border.width: 1
                        border.color: borderColor
                        Layout.fillWidth: true
                        Layout.fillHeight: true

                        RowLayout {
                            anchors.fill: parent
                            anchors.margins: uiPanelMargin
                            spacing: uiSectionSpacing

                            ColumnLayout {
                                Layout.fillWidth: true
                                Layout.fillHeight: true
                                Label { text: selectedTemplateId ? "Редактирование шаблона" : "Новый шаблон"; font.bold: true }
                                TextField { Layout.fillWidth: true; implicitHeight: uiControlHeight; text: tplTitle; placeholderText: "Название шаблона"; onTextChanged: tplTitle = text }
                                ComboBox { Layout.fillWidth: true; implicitHeight: uiControlHeight; model: workoutStore.categories; currentIndex: Math.max(0, model.indexOf(tplCategory)); onActivated: tplCategory = currentText }
                                RowLayout {
                                    Layout.fillWidth: true
                                    Label { text: "Км" }
                                    SpinBox { implicitHeight: uiControlHeight; from: 0; to: 300; value: Math.round(tplDistance); onValueModified: tplDistance = value }
                                    Label { text: "Мин" }
                                    SpinBox { implicitHeight: uiControlHeight; from: 0; to: 400; value: tplDuration; onValueModified: tplDuration = value }
                                }
                                ComboBox { Layout.fillWidth: true; implicitHeight: uiControlHeight; model: workoutStore.intensities; currentIndex: Math.max(0, model.indexOf(tplIntensity)); onActivated: tplIntensity = currentText }
                                TextArea { Layout.fillWidth: true; Layout.preferredHeight: 90; text: tplIntervals; placeholderText: "JSON интервалов"; onTextChanged: tplIntervals = text }
                                TextField { Layout.fillWidth: true; implicitHeight: uiControlHeight; text: tplTags; placeholderText: "Теги"; onTextChanged: tplTags = text }
                                TextArea { Layout.fillWidth: true; Layout.fillHeight: true; text: tplNotes; placeholderText: "Заметки"; onTextChanged: tplNotes = text }
                                RowLayout {
                                    Layout.fillWidth: true
                                    Button {
                                        text: selectedTemplateId ? "Обновить шаблон" : "Сохранить шаблон"
                                        implicitHeight: uiControlHeight
                                        enabled: workoutStore.canEditWorkouts
                                        onClicked: {
                                            if (selectedTemplateId) {
                                                workoutStore.updateTemplate(selectedTemplateId, tplTitle, tplCategory, tplDistance, tplDuration, tplIntensity, tplIntervals, tplNotes, tplTags)
                                            } else {
                                                workoutStore.saveTemplate(tplTitle, tplCategory, tplDistance, tplDuration, tplIntensity, tplIntervals, tplNotes, tplTags)
                                            }
                                        }
                                    }
                                    Button {
                                        text: "Сброс"
                                        implicitHeight: uiControlHeight
                                        onClicked: {
                                            selectedTemplateId = ""
                                            tplTitle = ""
                                            tplCategory = "run"
                                            tplDistance = 10
                                            tplDuration = 50
                                            tplIntensity = "moderate"
                                            tplIntervals = "[{\"step\":\"10min warmup\"},{\"step\":\"main set\"}]"
                                            tplTags = ""
                                            tplNotes = ""
                                        }
                                    }
                                }
                            }

                            Rectangle { Layout.preferredWidth: 1; Layout.fillHeight: true; color: "#e0e6ed" }

                            ColumnLayout {
                                Layout.fillWidth: true
                                Layout.fillHeight: true
                                Label { text: "Библиотека шаблонов"; font.bold: true }
                                RowLayout {
                                    Layout.fillWidth: true
                                    Label { text: "Дата плана" }
                                    TextField { Layout.fillWidth: true; implicitHeight: uiControlHeight; text: planDateIso; placeholderText: "YYYY-MM-DD"; onTextChanged: planDateIso = text }
                                }
                                Label {
                                    text: /^\\d{4}-\\d{2}-\\d{2}$/.test(planDateIso) ? "" : "Формат даты: YYYY-MM-DD"
                                    color: "#c62828"
                                }
                                ListView {
                                    Layout.fillWidth: true
                                    Layout.fillHeight: true
                                    model: workoutStore.templateLibrary
                                    spacing: 5
                                    clip: true
                                    delegate: Rectangle {
                                        width: ListView.view.width
                                        height: 96
                                        radius: 6
                                        color: selectedTemplateId === modelData.id ? "#e9f2ff" : "#f8fafc"
                                        border.width: 1
                                        border.color: "#d9e2ec"
                                        Column {
                                            anchors.fill: parent
                                            anchors.margins: 6
                                            Label { text: modelData.title + " [" + modelData.category + "]"; font.bold: true }
                                            Label { text: modelData.distanceKm + " км • " + modelData.durationMin + " мин • " + modelData.intensity; color: mutedTextColor }
                                            Row {
                                                spacing: 6
                                                Button {
                                                    text: "Поставить в план"
                                                    implicitHeight: uiSmallControlHeight
                                                    enabled: workoutStore.canEditWorkouts && /^\\d{4}-\\d{2}-\\d{2}$/.test(planDateIso)
                                                    onClicked: workoutStore.planFromTemplate(modelData.id, planDateIso)
                                                }
                                                Button {
                                                    text: "Ред."
                                                    implicitHeight: uiSmallControlHeight
                                                    enabled: workoutStore.canEditWorkouts
                                                    onClicked: {
                                                        selectedTemplateId = modelData.id
                                                        tplTitle = modelData.title
                                                        tplCategory = modelData.category
                                                        tplDistance = modelData.distanceKm
                                                        tplDuration = modelData.durationMin
                                                        tplIntensity = modelData.intensity
                                                        tplIntervals = modelData.intervals
                                                        tplNotes = modelData.notes
                                                        tplTags = modelData.tags
                                                    }
                                                }
                                                Button {
                                                    text: "Удалить"
                                                    implicitHeight: uiSmallControlHeight
                                                    enabled: workoutStore.canEditWorkouts
                                                    onClicked: {
                                                        deleteTemplateId = modelData.id
                                                        confirmDeleteTemplate.open()
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                                Label {
                                    visible: workoutStore.templateLibrary.length === 0
                                    text: "Шаблонов пока нет. Создайте первый шаблон слева."
                                    color: mutedTextColor
                                }
                            }
                        }
                    }

                    Rectangle {
                        radius: 8
                        color: cardColor
                        border.width: 1
                        border.color: borderColor
                        Layout.fillWidth: true
                        Layout.fillHeight: true

                        Column {
                            anchors.fill: parent
                            anchors.margins: 12
                            spacing: 8
                            Label { text: "Аналитика спортсмена: " + workoutStore.selectedAthleteName; font.bold: true; font.pixelSize: 16; color: primaryTextColor }
                            Label { text: "Всего тренировок: " + (root.analyticsObj.workoutsCount || 0); color: primaryTextColor }
                            Label { text: "Общая длительность: " + (root.analyticsObj.durationTotal || 0) + " мин"; color: primaryTextColor }
                            Label { text: "Общая дистанция: " + Number(root.analyticsObj.distanceTotal || 0).toFixed(1) + " км"; color: primaryTextColor }
                            Label { text: "Легко: " + ((root.analyticsObj.byIntensity && root.analyticsObj.byIntensity.easy) ? root.analyticsObj.byIntensity.easy : 0); color: primaryTextColor }
                            Label { text: "Умеренно: " + ((root.analyticsObj.byIntensity && root.analyticsObj.byIntensity.moderate) ? root.analyticsObj.byIntensity.moderate : 0); color: primaryTextColor }
                            Label { text: "Тяжело: " + ((root.analyticsObj.byIntensity && root.analyticsObj.byIntensity.hard) ? root.analyticsObj.byIntensity.hard : 0); color: primaryTextColor }
                        }
                    }

                    Rectangle {
                        radius: 8
                        color: cardColor
                        border.width: 1
                        border.color: borderColor
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        ColumnLayout {
                            anchors.fill: parent
                            anchors.margins: uiPanelMargin
                            spacing: uiItemSpacing
                            Label { text: "Тренер ↔ атлет"; font.bold: true; font.pixelSize: 16; color: primaryTextColor }
                            Label { text: "Текущая роль: " + workoutStore.currentUserRole; color: primaryTextColor }
                            Label { text: "Текущий атлет: " + workoutStore.selectedAthleteName; color: primaryTextColor }
                            Label { text: workoutStore.canEditWorkouts ? "Тренер может создавать/редактировать тренировки и шаблоны." : "Атлет видит только свои данные, без изменения планов."; color: primaryTextColor }
                            Label { text: "Комментарии и статусы выполнения доступны в правой панели."; color: primaryTextColor }
                        }
                    }
                }
            }
        }

        Rectangle {
            Layout.preferredWidth: 360
            Layout.fillHeight: true
            color: cardColor
            radius: 12
            border.width: 1
            border.color: borderColor

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: uiPanelMargin
                spacing: uiItemSpacing

                Label {
                    text: "Контекст"
                    font.bold: true
                    font.pixelSize: 16
                    color: primaryTextColor
                }
                Label { text: "Выбранная дата: " + workoutStore.selectedDayLabel; color: mutedTextColor }
                Label { text: "Тренировки дня"; font.bold: true; color: primaryTextColor }

                ListView {
                    Layout.fillWidth: true
                    Layout.preferredHeight: Math.max(96, Math.min(180, workoutStore.selectedDayWorkouts.length * 64))
                    clip: true
                    model: workoutStore.selectedDayWorkouts
                    spacing: 4
                    delegate: Rectangle {
                        width: ListView.view.width
                        height: 60
                        radius: 5
                        color: "#f8fafc"
                        border.width: 1
                        border.color: "#dde4ed"
                        MouseArea {
                            anchors.fill: parent
                            onClicked: workoutStore.selectWorkout(modelData.id)
                        }
                        Column {
                            anchors.fill: parent
                            anchors.margins: 6
                            Label { text: modelData.typeIcon + " " + modelData.title; elide: Text.ElideRight; width: parent.width; color: primaryTextColor }
                            Label { text: modelData.distance + " • " + modelData.duration; color: mutedTextColor; font.pixelSize: 11 }
                            Label { text: modelData.intensityLabel + " • " + modelData.status; color: modelData.intensityColor; font.pixelSize: 11 }
                        }
                    }
                }
                Label {
                    visible: workoutStore.selectedDayWorkouts.length === 0
                    text: "На выбранную дату тренировок нет."
                    color: mutedTextColor
                }

                Rectangle {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 260
                    Layout.minimumHeight: 220
                    radius: 6
                    color: "#f8fafc"
                    border.width: 1
                    border.color: "#dde4ed"
                    clip: true

                    ScrollView {
                        anchors.fill: parent
                        anchors.margins: 8
                        clip: true
                        ScrollBar.horizontal.policy: ScrollBar.AlwaysOff

                        ColumnLayout {
                            width: parent.width
                            spacing: 6

                            Label { text: "Детали"; font.bold: true; color: primaryTextColor }
                            Label { Layout.fillWidth: true; text: root.selectedWorkoutObj.title ? root.selectedWorkoutObj.typeIcon + " " + root.selectedWorkoutObj.title : "Нет выбранной тренировки"; wrapMode: Text.Wrap; color: primaryTextColor }
                            Label { text: root.selectedWorkoutObj.dateIso ? "Дата: " + root.selectedWorkoutObj.dateIso : ""; color: primaryTextColor }
                            Label { text: root.selectedWorkoutObj.distance ? "Дистанция: " + root.selectedWorkoutObj.distance : ""; color: primaryTextColor }
                            Label { text: root.selectedWorkoutObj.duration ? "Длительность: " + root.selectedWorkoutObj.duration : ""; color: primaryTextColor }
                            Label { text: root.selectedWorkoutObj.intensityLabel ? "Интенсивность: " + root.selectedWorkoutObj.intensityLabel : ""; color: primaryTextColor }
                            Label { text: root.selectedWorkoutObj.status ? "Статус: " + root.selectedWorkoutObj.status : ""; color: primaryTextColor }
                            Label { text: root.selectedWorkoutObj.athleteMood ? "Самочувствие: " + moodLabel(root.selectedWorkoutObj.athleteMood) : ""; color: primaryTextColor }
                            Label { text: root.selectedWorkoutObj.perceivedExertion ? "Воспринимаемое усилие: " + root.selectedWorkoutObj.perceivedExertion + "/6" : ""; color: primaryTextColor }
                            Label { Layout.fillWidth: true; text: root.selectedWorkoutObj.intervalsJson ? "Интервалы: " + root.selectedWorkoutObj.intervalsJson : ""; wrapMode: Text.Wrap; color: primaryTextColor }

                            RowLayout {
                                Layout.fillWidth: true
                                spacing: 6
                                ComboBox {
                                    Layout.fillWidth: true
                                    model: [
                                        { label: "Запланировано", value: "planned" },
                                        { label: "Выполнено", value: "done" },
                                        { label: "Пропущено", value: "skipped" }
                                    ]
                                    textRole: "label"
                                    currentIndex: statusIndex(statusDraft)
                                    enabled: root.selectedWorkoutObj.id && (workoutStore.canEditWorkouts || workoutStore.currentUserRole === "athlete")
                                    onActivated: function(index) {
                                        statusDraft = model[index].value
                                    if (statusDraft === "done" && perceivedExertionDraft === 0)
                                        perceivedExertionDraft = 1
                                    }
                                }
                                Button {
                                    text: "Применить статус"
                                    implicitHeight: uiControlHeight
                                    enabled: root.selectedWorkoutObj.id && statusDraft.length > 0
                                    onClicked: {
                                        if (root.selectedWorkoutObj.id)
                                        workoutStore.markWorkoutStatusDetailed(
                                            root.selectedWorkoutObj.id,
                                            statusDraft,
                                            feedbackDraft,
                                            moodDraft,
                                            perceivedExertionDraft
                                        )
                                    }
                                }
                            }

                            TextField {
                                Layout.fillWidth: true
                                implicitHeight: uiControlHeight
                                text: feedbackDraft
                                placeholderText: "Фидбек атлета"
                                onTextChanged: feedbackDraft = text
                            }

                            Label {
                                visible: statusDraft === "done"
                                text: "Как я себя чувствовал"
                                font.bold: true
                                color: primaryTextColor
                            }
                            ComboBox {
                                visible: statusDraft === "done"
                                Layout.fillWidth: true
                                model: [
                                    { label: "Отлично", value: "excellent" },
                                    { label: "Хорошо", value: "good" },
                                    { label: "Нормально", value: "normal" },
                                    { label: "Слабость", value: "weak" },
                                    { label: "Ужасно", value: "awful" }
                                ]
                                textRole: "label"
                                currentIndex: {
                                    if (moodDraft === "excellent") return 0
                                    if (moodDraft === "good") return 1
                                    if (moodDraft === "normal") return 2
                                    if (moodDraft === "weak") return 3
                                    if (moodDraft === "awful") return 4
                                    return 0
                                }
                                onActivated: function(index) {
                                    moodDraft = model[index].value
                                }
                            }

                            Label {
                                visible: statusDraft === "done"
                                text: "Воспринимаемое усилие (1-6)"
                                font.bold: true
                                color: primaryTextColor
                            }
                            ComboBox {
                                visible: statusDraft === "done"
                                Layout.fillWidth: true
                                model: [
                                    { label: "1 - Очень легко", value: 1 },
                                    { label: "2 - Легко", value: 2 },
                                    { label: "3 - Средне", value: 3 },
                                    { label: "4 - Чуть сложнее среднего", value: 4 },
                                    { label: "5 - Сложно", value: 5 },
                                    { label: "6 - Очень сложно", value: 6 }
                                ]
                                textRole: "label"
                                currentIndex: Math.max(0, perceivedExertionDraft - 1)
                                onActivated: function(index) {
                                    perceivedExertionDraft = model[index].value
                                }
                            }

                            RowLayout {
                                Layout.fillWidth: true
                                spacing: 6
                                visible: root.selectedWorkoutObj.id && workoutStore.canEditWorkouts
                                Button {
                                    text: "Редактировать"
                                    implicitHeight: uiSmallControlHeight
                                    onClicked: {
                                        fillDraftFromSelected()
                                        workoutStore.openCreateDialogForDate(root.selectedWorkoutObj.dateIso)
                                    }
                                }
                                Button {
                                    text: "Удалить"
                                    implicitHeight: uiSmallControlHeight
                                    onClicked: {
                                        deleteWorkoutId = root.selectedWorkoutObj.id
                                        confirmDeleteWorkout.open()
                                    }
                                }
                            }
                        }
                    }
                }

                Rectangle {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 1
                    color: "#e2e8f0"
                }

                Label { text: "Комментарии"; font.bold: true; color: primaryTextColor }
                ListView {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    clip: true
                    model: workoutStore.selectedWorkoutComments
                    spacing: 4
                    delegate: Rectangle {
                        width: ListView.view.width
                        height: 62
                        radius: 6
                        color: "#f5f9ff"
                        border.width: 1
                        border.color: "#d4e3f6"
                        Column {
                            anchors.fill: parent
                            anchors.margins: 6
                            Label { text: modelData.author + " • " + modelData.createdAt; font.pixelSize: 10; color: "#546e7a" }
                            Label { text: modelData.text; wrapMode: Text.Wrap }
                        }
                    }
                }
                Label {
                    visible: hasSelectedWorkout && workoutStore.selectedWorkoutComments.length === 0
                    text: "Комментариев пока нет."
                    color: mutedTextColor
                }
                TextField {
                    Layout.fillWidth: true
                    implicitHeight: uiControlHeight
                    placeholderText: "Комментарий"
                    text: commentText
                    enabled: hasSelectedWorkout
                    onTextChanged: commentText = text
                }
                RowLayout {
                    Layout.fillWidth: true
                    TextField {
                        Layout.fillWidth: true
                        implicitHeight: uiControlHeight
                        placeholderText: "Автор"
                        text: commentAuthor
                        enabled: hasSelectedWorkout
                        onTextChanged: commentAuthor = text
                    }
                    Button {
                        text: "Отправить"
                        implicitHeight: uiControlHeight
                        enabled: hasSelectedWorkout && commentText.trim().length > 0
                        onClicked: {
                            if (workoutStore.addComment(commentAuthor, commentText))
                                commentText = ""
                        }
                    }
                }
            }
        }
    }

    Rectangle {
        anchors.fill: parent
        visible: !root.isAuthenticated
        z: 30
        color: "#B3000000"

        Frame {
            anchors.centerIn: parent
            width: 420
            padding: 16

            background: Rectangle {
                color: cardColor
                radius: 10
                border.width: 1
                border.color: borderColor
            }

            ColumnLayout {
                anchors.fill: parent
                spacing: 10

                Label {
                    text: "Вход в приложение"
                    font.bold: true
                    font.pixelSize: 18
                }
                Label {
                    text: "Выберите роль и профиль"
                    color: mutedTextColor
                }

                ComboBox {
                    Layout.fillWidth: true
                    implicitHeight: root.uiControlHeight
                    model: [
                        { label: "Тренер", value: "coach" },
                        { label: "Атлет", value: "athlete" }
                    ]
                    textRole: "label"
                    currentIndex: loginRole === "athlete" ? 1 : 0
                    onActivated: function(index) {
                        loginRole = model[index].value
                        syncLoginUser()
                    }
                }

                ComboBox {
                    id: loginUserCombo
                    Layout.fillWidth: true
                    implicitHeight: root.uiControlHeight
                    model: roleUsers(loginRole)
                    textRole: "name"
                    valueRole: "id"
                    onActivated: function(index) {
                        const user = model[index]
                        loginUserId = user && user.id ? user.id : ""
                    }
                    Component.onCompleted: {
                        syncLoginUser()
                    }
                }

                Label {
                    visible: loginUserCombo.model.length === 0
                    text: "Для выбранной роли не найдено пользователей."
                    color: "#c62828"
                }

                RowLayout {
                    Layout.fillWidth: true
                    Item { Layout.fillWidth: true }
                    Button {
                        text: "Войти"
                        implicitHeight: root.uiControlHeight
                        enabled: loginUserId.length > 0
                        highlighted: true
                        onClicked: {
                            workoutStore.currentUserId = loginUserId
                            commentAuthor = workoutStore.currentUserRole === "athlete" ? "athlete" : "coach"
                            root.isAuthenticated = true
                        }
                    }
                }
            }
        }
    }

    CreateWorkoutPopup {
        id: createWorkoutPopup
        visible: workoutStore.createDialogOpen
        dialogTitle: editingWorkoutId.length > 0 ? "Редактирование тренировки" : "Новая тренировка"
        draftDateIso: workoutStore.draftDateIso
        workoutTitle: draftTitle
        workoutCategory: draftCategory
        workoutDistance: draftDistance
        workoutDuration: draftDuration
        workoutIntensity: draftIntensity
        workoutNotes: draftNotes
        workoutHidden: draftHidden
        workoutIntervals: draftIntervals
        categories: workoutStore.categories
        intensities: workoutStore.intensities
        errorText: workoutStore.errorMessage
        busy: workoutStore.busy
        saveEnabled: workoutStore.selectedAthleteId.length > 0 && workoutStore.canEditWorkouts
        saveDisabledHint: !workoutStore.canEditWorkouts ? "Редактирование тренировок доступно только тренеру." : "Выберите атлета для сохранения тренировки."
        onCancelRequested: {
            workoutStore.cancelCreateDialog()
            resetWorkoutDraft()
        }
        onSaveRequested: function(title, category, distanceKm, durationMin, intensity, notes, hiddenFromAthlete, intervalsJson) {
            if (editingWorkoutId.length > 0) {
                workoutStore.updateWorkout(editingWorkoutId, title, category, distanceKm, durationMin, intensity, notes, hiddenFromAthlete, intervalsJson)
            } else {
                workoutStore.createWorkout(title, category, distanceKm, durationMin, intensity, notes, hiddenFromAthlete, intervalsJson)
            }
        }
    }

    Dialog {
        id: confirmDeleteWorkout
        title: "Удалить тренировку?"
        modal: true
        standardButtons: Dialog.Yes | Dialog.No
        onAccepted: {
            if (deleteWorkoutId.length > 0)
                workoutStore.deleteWorkout(deleteWorkoutId)
            deleteWorkoutId = ""
        }
        onRejected: deleteWorkoutId = ""
    }

    Dialog {
        id: confirmDeleteTemplate
        title: "Удалить шаблон?"
        modal: true
        standardButtons: Dialog.Yes | Dialog.No
        onAccepted: {
            if (deleteTemplateId.length > 0)
                workoutStore.deleteTemplate(deleteTemplateId)
            deleteTemplateId = ""
        }
        onRejected: deleteTemplateId = ""
    }
}
