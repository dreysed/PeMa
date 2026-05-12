import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "components"

Item {
    id: routeTab

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

    // ── Data ─────────────────────────────────────────────────────────────────
    property var    routesModel:    []
    property bool   isBusy:         false
    property bool   stravaConnected: false
    property bool   stravaHasClientId: false
    property var    selectedRoute:  null

    // ── Generation-batch tracking ─────────────────────────────────────────────
    property int  _batchSize:       0
    property bool _wasGenerating:   false

    onIsBusyChanged: {
        if (routeTab.isBusy) {
            routeTab._wasGenerating = true
        } else if (routeTab._wasGenerating) {
            routeTab._wasGenerating = false
            routeTab._batchSize = routeTab.genCount
            if (routeTab.routesModel.length > 0)
                routeTab.selectedRoute = routeTab.routesModel[0]
        }
    }
    onRoutesModelChanged: {
        if (routeTab._batchSize > 0 && routeTab.routesModel.length > 0)
            routeTab.selectedRoute = routeTab.routesModel[0]
    }

    // ── Signals ───────────────────────────────────────────────────────────────
    signal generateRequested(real lat, real lon, real distKm, string prefs, int count)
    signal deleteRouteRequested(string id)
    signal buildFromWaypointsRequested(var waypoints, string name)
    signal connectStravaRequested()
    signal disconnectStravaRequested()
    signal syncStravaRequested()
    signal openStravaSettingsRequested()

    // ── Location ──────────────────────────────────────────────────────────────
    property real defaultLat: 55.7558
    property real defaultLon: 37.6173

    Component.onCompleted: {
        var xhr = new XMLHttpRequest()
        xhr.open("GET", "https://ipapi.co/json/")
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4 && xhr.status === 200) {
                try {
                    var d = JSON.parse(xhr.responseText)
                    if (d.latitude && d.longitude) {
                        routeTab.defaultLat = d.latitude
                        routeTab.defaultLon = d.longitude
                    }
                } catch(e) {}
            }
        }
        xhr.send()
    }

    // ── Generate form state ───────────────────────────────────────────────────
    property real   genLat:   defaultLat
    property real   genLon:   defaultLon
    property real   genDist:  5.0
    property string genPrefs: ""
    property int    genCount: 3

    onDefaultLatChanged: genLat = defaultLat
    onDefaultLonChanged: genLon = defaultLon

    // ── GPX clipboard export ──────────────────────────────────────────────────
    TextEdit { id: clipHelper; visible: false; focus: false }
    Timer    { id: gpxToast;   interval: 2000 }

    function copyRouteAsGpx() {
        if (!routeTab.selectedRoute || !routeTab.selectedRoute.geojson) return
        try {
            var geo    = JSON.parse(routeTab.selectedRoute.geojson)
            var coords = geo.coordinates || []
            var name   = (routeTab.selectedRoute.name || "Маршрут")
                             .replace(/&/g, "&amp;").replace(/</g, "&lt;")
            var lines  = ['<?xml version="1.0" encoding="UTF-8"?>',
                          '<gpx version="1.1" creator="SportCal" xmlns="http://www.topografix.com/GPX/1/1">',
                          '  <trk>', '    <name>' + name + '</name>', '    <trkseg>']
            for (var i = 0; i < coords.length; i++)
                lines.push('      <trkpt lat="' + coords[i][1].toFixed(6)
                            + '" lon="' + coords[i][0].toFixed(6) + '"><ele>0</ele></trkpt>')
            lines.push('    </trkseg>', '  </trk>', '</gpx>')
            clipHelper.text = lines.join('\n')
            clipHelper.selectAll()
            clipHelper.copy()
            gpxToast.restart()
        } catch(e) {}
    }

    // ── City geocoding ────────────────────────────────────────────────────────
    function searchCity(query) {
        if (!query || query.trim() === "") return
        var q = query.trim()
        var xhr = new XMLHttpRequest()
        xhr.open("GET", "https://nominatim.openstreetmap.org/search?q="
                 + encodeURIComponent(q) + "&format=json&limit=1")
        xhr.setRequestHeader("User-Agent", "SportCalApp/1.0")
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    try {
                        var results = JSON.parse(xhr.responseText)
                        if (results.length > 0) {
                            var r = results[0]
                            var lat = parseFloat(r.lat)
                            var lon = parseFloat(r.lon)
                            routeTab.genLat = lat
                            routeTab.genLon = lon
                            // Pan handler breaks the declarative binding, so we
                            // explicitly push the new centre into the map too.
                            theMap.centerLat = lat
                            theMap.centerLon = lon
                            theMap.zoom = 13
                            cityStatusLabel.text = r.display_name.split(",").slice(0, 2).join(",")
                        } else {
                            cityStatusLabel.text = "Город не найден"
                        }
                    } catch(e) { cityStatusLabel.text = "Ошибка разбора ответа" }
                } else {
                    cityStatusLabel.text = "Ошибка поиска (" + xhr.status + ")"
                }
            }
        }
        xhr.send()
    }

    // ── Route coords from selected route GeoJSON ──────────────────────────────
    property var routeCoords: []
    onSelectedRouteChanged: {
        if (!selectedRoute || !selectedRoute.geojson) { routeCoords = []; return }
        try {
            var geo = JSON.parse(selectedRoute.geojson)
            routeCoords = geo.coordinates || []
        } catch(e) { routeCoords = [] }
    }

    // ── Layout ────────────────────────────────────────────────────────────────
    RowLayout {
        anchors.fill: parent
        spacing: 0

        // ── Left sidebar ──────────────────────────────────────────────────────
        Rectangle {
            id: sidebar
            Layout.preferredWidth: 300
            Layout.fillHeight: true
            color: surface

            // Right border
            Rectangle {
                anchors.top: parent.top
                anchors.right: parent.right
                anchors.bottom: parent.bottom
                width: 1; color: borderCol
            }

            ScrollView {
                id: sidebarScroll
                anchors.fill: parent
                contentWidth: availableWidth
                clip: true
                ScrollBar.horizontal.policy: ScrollBar.AlwaysOff

                // Single Column — width always equals the scroll viewport
                Column {
                    width: sidebarScroll.availableWidth
                    spacing: 0

                    // ── Header ────────────────────────────────────────────────
                    Rectangle {
                        width: parent.width; height: 56; color: "transparent"
                        RowLayout {
                            anchors.fill: parent
                            anchors.leftMargin: 20; anchors.rightMargin: 16
                            Label {
                                text: "Маршруты"
                                font.pixelSize: 17; font.weight: Font.Black
                                color: textPrimary; font.letterSpacing: -0.3
                                Layout.fillWidth: true
                            }
                        }
                    }
                    Rectangle { width: parent.width; height: 1; color: borderCol }

                    // ── Strava section ─────────────────────────────────────────
                    Item { width: parent.width; height: 16 }

                    Rectangle {
                        width: parent.width - 40
                        x: 20
                        height: stravaBlock.implicitHeight + 16
                        radius: 10; color: surface2
                        border.width: 1; border.color: borderCol

                        Column {
                            id: stravaBlock
                            anchors.left: parent.left; anchors.right: parent.right
                            anchors.top: parent.top
                            anchors.margins: 12
                            spacing: 8

                            Label {
                                text: "STRAVA"
                                font.pixelSize: 9; font.weight: Font.Black
                                color: textMuted; font.letterSpacing: 1.2
                            }

                            RowLayout {
                                width: parent.width
                                Label {
                                    text: routeTab.stravaConnected ? "Подключено" : "Не подключено"
                                    font.pixelSize: 12; font.weight: Font.DemiBold
                                    color: routeTab.stravaConnected ? runColor : textMuted
                                    Layout.fillWidth: true
                                }
                                Rectangle {
                                    width: 8; height: 8; radius: 4
                                    color: routeTab.stravaConnected ? runColor : borderCol
                                }
                            }

                            Label {
                                width: parent.width
                                text: routeTab.stravaConnected
                                    ? "Активности синхронизируются автоматически"
                                    : "Подключите аккаунт чтобы тренировки загружались сами"
                                font.pixelSize: 10; color: textMuted; wrapMode: Text.Wrap
                            }

                            Row {
                                spacing: 6
                                Rectangle {
                                    height: 28; width: stravaBtn.implicitWidth + 18; radius: 7
                                    color: routeTab.stravaConnected ? surface : "#FC4C02"
                                    border.width: routeTab.stravaConnected ? 1 : 0
                                    border.color: borderCol
                                    Label {
                                        id: stravaBtn; anchors.centerIn: parent
                                        text: routeTab.stravaConnected ? "Отключить" : "Подключить Strava"
                                        font.pixelSize: 11; font.weight: Font.DemiBold
                                        color: routeTab.stravaConnected ? textMuted : "#fff"
                                    }
                                    MouseArea { anchors.fill: parent; cursorShape: Qt.PointingHandCursor
                                        onClicked: {
                                            if (routeTab.stravaConnected)
                                                routeTab.disconnectStravaRequested()
                                            else if (!routeTab.stravaHasClientId)
                                                routeTab.openStravaSettingsRequested()
                                            else
                                                routeTab.connectStravaRequested()
                                        }
                                    }
                                }
                                Rectangle {
                                    visible: routeTab.stravaConnected
                                    height: 28; width: syncLbl.implicitWidth + 18; radius: 7
                                    color: surface2; border.width: 1; border.color: borderCol
                                    Label {
                                        id: syncLbl; anchors.centerIn: parent
                                        text: "Синхронизировать"; font.pixelSize: 11; color: accent
                                    }
                                    MouseArea { anchors.fill: parent; cursorShape: Qt.PointingHandCursor
                                        onClicked: routeTab.syncStravaRequested() }
                                }
                            }
                        }
                    }

                    // ── Generate form ──────────────────────────────────────────
                    Item { width: parent.width; height: 16 }

                    Column {
                        width: parent.width - 40
                        x: 20
                        spacing: 8

                        Label {
                            text: "СГЕНЕРИРОВАТЬ"
                            font.pixelSize: 9; font.weight: Font.Black
                            color: textMuted; font.letterSpacing: 1.2
                        }

                        Rectangle {
                            width: parent.width
                            height: genInner.implicitHeight + 24
                            radius: 10; color: surface2
                            border.width: 1; border.color: borderCol

                            Column {
                                id: genInner
                                anchors.left: parent.left; anchors.right: parent.right
                                anchors.top: parent.top
                                anchors.margins: 14
                                spacing: 12

                                // City / district / park search
                                Column {
                                    width: parent.width; spacing: 4

                                    Label {
                                        text: "Место (район, парк, улица, город)"
                                        font.pixelSize: 10; color: textMuted
                                    }

                                    RowLayout {
                                        width: parent.width; spacing: 6
                                        TextField {
                                            id: cityField
                                            Layout.fillWidth: true; implicitHeight: 34
                                            font.pixelSize: 12
                                            placeholderText: "Сокольники Москва · Парк Горького · Казань..."
                                            onAccepted: {
                                                cityStatusLabel.text = "Ищу…"
                                                routeTab.searchCity(cityField.text)
                                            }
                                        }
                                        Rectangle {
                                            width: 34; height: 34; radius: 8; color: accent
                                            Label { anchors.centerIn: parent; text: "→"; font.pixelSize: 15; color: "#fff"; font.weight: Font.DemiBold }
                                            MouseArea { anchors.fill: parent; cursorShape: Qt.PointingHandCursor
                                                onClicked: {
                                                    cityStatusLabel.text = "Ищу…"
                                                    routeTab.searchCity(cityField.text)
                                                }
                                            }
                                        }
                                    }

                                    Label {
                                        id: cityStatusLabel
                                        width: parent.width
                                        text: ""; visible: text !== ""
                                        font.pixelSize: 10; color: textMuted; wrapMode: Text.Wrap
                                        elide: Text.ElideRight; maximumLineCount: 1
                                    }
                                }

                                // Distance
                                Column {
                                    width: parent.width; spacing: 2

                                    RowLayout {
                                        width: parent.width
                                        Label { text: "Длина"; font.pixelSize: 10; color: textMuted }
                                        Item { Layout.fillWidth: true }
                                        Label {
                                            text: routeTab.genDist.toFixed(1) + " км"
                                            font.pixelSize: 12; font.weight: Font.DemiBold; color: accent
                                        }
                                    }
                                    Slider {
                                        width: parent.width; from: 1; to: 42; stepSize: 0.5
                                        value: routeTab.genDist
                                        onValueChanged: routeTab.genDist = value
                                    }
                                }

                                // Preferences
                                TextField {
                                    width: parent.width; implicitHeight: 34; font.pixelSize: 12
                                    placeholderText: "парки, набережная, тихие улицы..."
                                    onTextChanged: routeTab.genPrefs = text
                                }

                                // Count selector
                                Column {
                                    width: parent.width; spacing: 6

                                    Label {
                                        text: "ВАРИАНТОВ МАРШРУТА"
                                        font.pixelSize: 9; font.weight: Font.Black
                                        color: textMuted; font.letterSpacing: 1.2
                                    }

                                    Row {
                                        width: parent.width
                                        spacing: (width - 5 * 40) / 4
                                        Repeater {
                                            model: [1, 2, 3, 4, 5]
                                            Rectangle {
                                                width: 40; height: 32; radius: 8
                                                color: routeTab.genCount === modelData ? accent : surface
                                                border.width: 1
                                                border.color: routeTab.genCount === modelData ? accent : borderCol
                                                Label {
                                                    anchors.centerIn: parent; text: modelData
                                                    font.pixelSize: 13; font.weight: Font.DemiBold
                                                    color: routeTab.genCount === modelData ? "#fff" : textMuted
                                                }
                                                MouseArea { anchors.fill: parent; cursorShape: Qt.PointingHandCursor
                                                    onClicked: routeTab.genCount = modelData }
                                            }
                                        }
                                    }
                                }

                                // Generate button
                                Rectangle {
                                    width: parent.width; height: 36; radius: 8
                                    color: routeTab.isBusy ? borderCol : accent
                                    opacity: routeTab.isBusy ? 0.7 : 1.0
                                    Label {
                                        anchors.centerIn: parent
                                        text: routeTab.isBusy ? "Строю маршруты…" : "Сгенерировать"
                                        font.pixelSize: 13; font.weight: Font.DemiBold; color: "#fff"
                                    }
                                    MouseArea {
                                        anchors.fill: parent
                                        enabled: !routeTab.isBusy
                                        cursorShape: Qt.PointingHandCursor
                                        onClicked: routeTab.generateRequested(
                                            routeTab.genLat, routeTab.genLon,
                                            routeTab.genDist, routeTab.genPrefs, routeTab.genCount)
                                    }
                                }
                            }
                        }
                    }

                    // ── Route list ─────────────────────────────────────────────
                    Item { width: parent.width; height: 16 }

                    // "НОВЫЕ ВАРИАНТЫ" header
                    Item {
                        width: parent.width
                        height: newVariantsHeader.visible ? newVariantsHeader.height : 0
                        visible: routeTab._batchSize > 0 && routeTab.routesModel.length > 0

                        RowLayout {
                            id: newVariantsHeader
                            anchors.left: parent.left; anchors.right: parent.right
                            anchors.leftMargin: 20; anchors.rightMargin: 20
                            Label {
                                text: "НОВЫЕ ВАРИАНТЫ"
                                font.pixelSize: 9; font.weight: Font.Black
                                color: accent; font.letterSpacing: 1.2
                            }
                            Item { Layout.fillWidth: true }
                            Label {
                                text: "скрыть"; font.pixelSize: 9; color: textMuted
                                MouseArea { anchors.fill: parent; cursorShape: Qt.PointingHandCursor
                                    onClicked: routeTab._batchSize = 0 }
                            }
                        }
                    }
                    Item {
                        width: parent.width; height: 4
                        visible: routeTab._batchSize > 0 && routeTab.routesModel.length > 0
                    }

                    // Route list header when no batch
                    Item {
                        width: parent.width; height: savedHeader.implicitHeight
                        visible: routeTab._batchSize === 0 && routeTab.routesModel.length > 0
                        Label {
                            id: savedHeader
                            anchors.left: parent.left; anchors.leftMargin: 20
                            text: "СОХРАНЁННЫЕ"
                            font.pixelSize: 9; font.weight: Font.Black
                            color: textMuted; font.letterSpacing: 1.2
                        }
                    }
                    Item {
                        width: parent.width; height: 4
                        visible: routeTab._batchSize === 0 && routeTab.routesModel.length > 0
                    }

                    // Route delegates via Repeater inside Column
                    Repeater {
                        model: routeTab.routesModel
                        delegate: Item {
                            id: routeDelegate
                            property bool isNew: index < routeTab._batchSize
                            property bool isSelected: routeTab.selectedRoute !== null
                                                      && routeTab.selectedRoute.id === modelData.id

                            width: sidebarScroll.availableWidth
                            height: 64

                            Rectangle {
                                anchors.fill: parent
                                color: isSelected
                                       ? (dark ? "#16123a" : "#f5f3ff")
                                       : isNew ? (dark ? "#1a1a2e" : "#fafafe") : "transparent"

                                // Left accent bar
                                Rectangle {
                                    anchors.left: parent.left
                                    anchors.top: parent.top
                                    anchors.bottom: parent.bottom
                                    width: isNew ? 4 : 3
                                    color: isNew ? accent : (isSelected ? accent : borderCol)
                                    opacity: isNew ? 1 : (isSelected ? 0.8 : 0)
                                }

                                // Bottom separator
                                Rectangle {
                                    anchors.left: parent.left; anchors.right: parent.right
                                    anchors.bottom: parent.bottom
                                    anchors.leftMargin: 20; anchors.rightMargin: 20
                                    height: 1; color: borderCol; opacity: 0.5
                                }

                                RowLayout {
                                    anchors.fill: parent
                                    anchors.leftMargin: 20; anchors.rightMargin: 14
                                    spacing: 10

                                    ColumnLayout {
                                        Layout.fillWidth: true; spacing: 3

                                        RowLayout {
                                            spacing: 6; Layout.fillWidth: true
                                            Label {
                                                text: modelData.name || "Маршрут"
                                                font.pixelSize: 13; font.weight: Font.DemiBold
                                                color: textPrimary; elide: Text.ElideRight
                                                Layout.fillWidth: true
                                            }
                                            Rectangle {
                                                visible: isNew
                                                height: 16; width: newBadgeLbl.implicitWidth + 8; radius: 4
                                                color: accent
                                                Label {
                                                    id: newBadgeLbl; anchors.centerIn: parent
                                                    text: "NEW"; font.pixelSize: 8
                                                    font.weight: Font.Black; color: "#fff"
                                                    font.letterSpacing: 0.5
                                                }
                                            }
                                        }

                                        Label {
                                            text: (modelData.distanceKm || 0).toFixed(1) + " км"
                                                  + (modelData.description && !isNew
                                                     ? "  ·  " + modelData.description : "")
                                            font.pixelSize: 11; color: textMuted
                                            elide: Text.ElideRight; Layout.fillWidth: true
                                        }
                                    }

                                    // Delete button
                                    Rectangle {
                                        width: 26; height: 26; radius: 6
                                        color: surface2; border.width: 1; border.color: borderCol
                                        Label { anchors.centerIn: parent; text: "×"; font.pixelSize: 14; color: textMuted }
                                        MouseArea { anchors.fill: parent; cursorShape: Qt.PointingHandCursor
                                            onClicked: {
                                                if (routeTab._batchSize > 0)
                                                    routeTab._batchSize = Math.max(0, routeTab._batchSize - 1)
                                                routeTab.deleteRouteRequested(modelData.id)
                                            }
                                        }
                                    }
                                }

                                MouseArea {
                                    anchors.fill: parent; z: -1
                                    cursorShape: Qt.PointingHandCursor
                                    onClicked: routeTab.selectedRoute = modelData
                                }
                            }
                        }
                    }

                    // Separator between variants and older routes
                    Rectangle {
                        visible: routeTab._batchSize > 0 && routeTab.routesModel.length > routeTab._batchSize
                        width: parent.width - 40; x: 20
                        height: 1; color: borderCol
                    }
                    Item {
                        visible: routeTab._batchSize > 0 && routeTab.routesModel.length > routeTab._batchSize
                        width: parent.width; height: 6
                        Label {
                            anchors.left: parent.left; anchors.leftMargin: 20
                            anchors.verticalCenter: parent.verticalCenter
                            text: "РАНЕЕ СОХРАНЁННЫЕ"
                            font.pixelSize: 9; font.weight: Font.Black
                            color: textMuted; font.letterSpacing: 1.2
                        }
                    }

                    // Empty state
                    Item {
                        width: parent.width; height: 60
                        visible: routeTab.routesModel.length === 0
                        Label {
                            anchors.centerIn: parent
                            text: "Маршрутов пока нет"
                            font.pixelSize: 12; color: textMuted
                        }
                    }

                    Item { width: parent.width; height: 20 }
                }
            }
        }

        // ── Right: map + toolbar ──────────────────────────────────────────────
        Item {
            Layout.fillWidth: true; Layout.fillHeight: true

            TileMap {
                id: theMap
                anchors.fill: parent
                dark:        routeTab.dark
                lineColor:   routeTab.accent
                routeCoords: routeTab.routeCoords
                centerLat:   routeTab.selectedRoute
                             ? (routeTab.selectedRoute.startLat || routeTab.genLat)
                             : routeTab.genLat
                centerLon:   routeTab.selectedRoute
                             ? (routeTab.selectedRoute.startLon || routeTab.genLon)
                             : routeTab.genLon
            }

            // ── Route info overlay ────────────────────────────────────────────
            Rectangle {
                visible: !!routeTab.selectedRoute
                anchors.top: parent.top
                anchors.left: parent.left; anchors.right: parent.right
                anchors.margins: 12
                height: routeInfoRow.implicitHeight + 20
                radius: 10; color: surface + "ee"
                border.width: 1; border.color: borderCol

                RowLayout {
                    id: routeInfoRow
                    anchors.fill: parent; anchors.margins: 12
                    spacing: 12

                    ColumnLayout {
                        Layout.fillWidth: true; spacing: 2
                        Label {
                            text: routeTab.selectedRoute ? (routeTab.selectedRoute.name || "Маршрут") : ""
                            font.pixelSize: 15; font.weight: Font.Black; color: textPrimary
                        }
                        Label {
                            text: routeTab.selectedRoute
                                  ? ((routeTab.selectedRoute.distanceKm || 0).toFixed(1)
                                     + " км  ·  " + (routeTab.selectedRoute.description || ""))
                                  : ""
                            font.pixelSize: 11; color: textMuted; elide: Text.ElideRight
                            Layout.fillWidth: true
                        }
                    }

                    Rectangle {
                        height: 30; width: gpxLbl.implicitWidth + 16; radius: 7
                        color: gpxToast.running ? routeTab.runColor : routeTab.surface2
                        border.width: 1; border.color: gpxToast.running ? routeTab.runColor : routeTab.borderCol
                        Label {
                            id: gpxLbl; anchors.centerIn: parent
                            text: gpxToast.running ? "Скопировано!" : "Скопировать GPX"
                            font.pixelSize: 11
                            color: gpxToast.running ? "#fff" : routeTab.accent
                        }
                        MouseArea { anchors.fill: parent; cursorShape: Qt.PointingHandCursor
                            onClicked: routeTab.copyRouteAsGpx() }
                    }

                    Rectangle {
                        height: 30; width: editRtLbl.implicitWidth + 16; radius: 7
                        color: surface2; border.width: 1; border.color: borderCol
                        Label { id: editRtLbl; anchors.centerIn: parent; text: "Редактировать"; font.pixelSize: 11; color: accent }
                        MouseArea { anchors.fill: parent; cursorShape: Qt.PointingHandCursor
                            onClicked: {
                                if (!routeTab.selectedRoute || !routeTab.selectedRoute.geojson) return
                                try {
                                    var geo = JSON.parse(routeTab.selectedRoute.geojson)
                                    var coords = geo.coordinates || []
                                    if (coords.length < 2) return
                                    var wps = []
                                    var n = Math.min(10, coords.length)
                                    for (var i = 0; i < n; i++) {
                                        var idx = Math.round(i * (coords.length - 1) / (n - 1))
                                        wps.push({ lon: coords[idx][0], lat: coords[idx][1] })
                                    }
                                    theMap.editWaypoints = wps
                                    theMap.editMode = true
                                } catch(ex) {}
                            }
                        }
                    }

                    Rectangle {
                        width: 30; height: 30; radius: 7
                        color: surface2; border.width: 1; border.color: borderCol
                        Label { anchors.centerIn: parent; text: "✕"; font.pixelSize: 13; color: textMuted }
                        MouseArea { anchors.fill: parent; cursorShape: Qt.PointingHandCursor
                            onClicked: { routeTab.selectedRoute = null; routeTab.routeCoords = [] } }
                    }
                }
            }

            // ── Edit toolbar (bottom of map) ──────────────────────────────────
            Rectangle {
                anchors.bottom: parent.bottom
                anchors.left: parent.left; anchors.right: parent.right
                anchors.margins: 12
                height: toolbarRow.implicitHeight + 16
                radius: 10; color: surface + "f0"
                border.width: 1; border.color: borderCol

                RowLayout {
                    id: toolbarRow
                    anchors.fill: parent; anchors.margins: 10
                    spacing: 8

                    Rectangle {
                        height: 34; width: drawLbl.implicitWidth + 18; radius: 8
                        color: theMap.editMode ? accent : surface2
                        border.width: 1; border.color: theMap.editMode ? accent : borderCol
                        Label {
                            id: drawLbl; anchors.centerIn: parent
                            text: theMap.editMode ? "Рисую…" : "Нарисовать маршрут"
                            font.pixelSize: 12; font.weight: Font.DemiBold
                            color: theMap.editMode ? "#fff" : textPrimary
                        }
                        MouseArea { anchors.fill: parent; cursorShape: Qt.PointingHandCursor
                            onClicked: theMap.editMode = !theMap.editMode }
                    }

                    Rectangle {
                        visible: theMap.editMode && theMap.editWaypoints.length > 0
                        height: 34; width: undoLbl.implicitWidth + 18; radius: 8
                        color: surface2; border.width: 1; border.color: borderCol
                        Label { id: undoLbl; anchors.centerIn: parent; text: "← Отмена"; font.pixelSize: 12; color: textPrimary }
                        MouseArea { anchors.fill: parent; cursorShape: Qt.PointingHandCursor
                            onClicked: theMap.removeLastWaypoint() }
                    }

                    Rectangle {
                        visible: theMap.editMode && theMap.editWaypoints.length > 0
                        height: 34; width: clearLbl.implicitWidth + 18; radius: 8
                        color: surface2; border.width: 1; border.color: borderCol
                        Label { id: clearLbl; anchors.centerIn: parent; text: "Очистить"; font.pixelSize: 12; color: textMuted }
                        MouseArea { anchors.fill: parent; cursorShape: Qt.PointingHandCursor
                            onClicked: theMap.clearEditWaypoints() }
                    }

                    Item { Layout.fillWidth: true }

                    Rectangle {
                        visible: theMap.editWaypoints.length >= 2
                        height: 34; width: buildLbl.implicitWidth + 18; radius: 8
                        color: routeTab.isBusy ? borderCol : runColor
                        opacity: routeTab.isBusy ? 0.7 : 1.0
                        Label {
                            id: buildLbl; anchors.centerIn: parent
                            text: routeTab.isBusy ? "Строю…" : "Построить маршрут"
                            font.pixelSize: 12; font.weight: Font.DemiBold; color: "#fff"
                        }
                        MouseArea { anchors.fill: parent; enabled: !routeTab.isBusy; cursorShape: Qt.PointingHandCursor
                            onClicked: {
                                var wps = []
                                for (var i = 0; i < theMap.editWaypoints.length; i++) {
                                    var wp = theMap.editWaypoints[i]
                                    wps.push([wp.lon, wp.lat])
                                }
                                routeTab.buildFromWaypointsRequested(wps, "Мой маршрут")
                                theMap.clearEditWaypoints()
                                theMap.editMode = false
                            }
                        }
                    }

                    Label {
                        visible: !theMap.editMode
                        text: "Прокрутка для зума · Перетаскивание для перемещения"
                        font.pixelSize: 10; color: textMuted
                    }
                }
            }
        }
    }
}
