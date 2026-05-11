import QtQuick
import QtQuick.Controls

/**
 * TileMap — OpenStreetMap tiles + route overlay. Pan/zoom.
 *
 * Performance trick: during drag we only translate the tile container (GPU move,
 * zero tile rebuilds). Tiles are rebuilt once when the finger lifts.
 */
Item {
    id: tileMap
    clip: true

    // ── Public API ────────────────────────────────────────────────────────────
    property double centerLat:  55.7558
    property double centerLon:  37.6173
    property int    zoom:       14
    property var    routeCoords: []       // [[lon, lat], …]
    property color  lineColor:  "#6366f1"
    property bool   dark:       false
    property string tileServer: "http://localhost:8000/api/tiles"

    // ── Edit mode ─────────────────────────────────────────────────────────────
    property bool editMode: false
    property var  editWaypoints: []
    signal waypointAdded()

    function addWaypoint(lat, lon) {
        var wps = editWaypoints.slice()
        wps.push({ lat: lat, lon: lon })
        editWaypoints = wps
        waypointAdded()
        routeCanvas.requestPaint()
    }
    function removeLastWaypoint() {
        if (editWaypoints.length === 0) return
        editWaypoints = editWaypoints.slice(0, editWaypoints.length - 1)
        routeCanvas.requestPaint()
    }
    function clearEditWaypoints() {
        editWaypoints = []
        routeCanvas.requestPaint()
    }

    // Repaint when waypoints are changed externally (e.g. loading a route for editing)
    onEditWaypointsChanged: routeCanvas.requestPaint()

    // ── Mercator helpers ──────────────────────────────────────────────────────
    function _scale()          { return Math.pow(2, zoom) * 256 }
    function _lonToWorld(lon)  { return (lon + 180) / 360 * _scale() }
    function _latToWorld(lat)  {
        var s = Math.sin(lat * Math.PI / 180)
        return (0.5 - Math.log((1 + s) / (1 - s)) / (4 * Math.PI)) * _scale()
    }
    function _worldYToLat(wy) {
        var n = Math.PI - 2 * Math.PI * wy / _scale()
        return 180 / Math.PI * Math.atan(Math.sinh(n))
    }
    function latLonToScreen(lat, lon) {
        var cx = _lonToWorld(centerLon);  var cy = _latToWorld(centerLat)
        var wx = _lonToWorld(lon);        var wy = _latToWorld(lat)
        return Qt.point(wx - cx + width / 2, wy - cy + height / 2)
    }
    function screenToLatLon(sx, sy) {
        var cx = _lonToWorld(centerLon);  var cy = _latToWorld(centerLat)
        var wx = sx - width / 2 + cx;    var wy = sy - height / 2 + cy
        return { lat: _worldYToLat(wy), lon: wx * 360 / _scale() - 180 }
    }

    // ── Tile grid ─────────────────────────────────────────────────────────────
    property var tileData: []

    function _updateTiles() {
        if (width <= 0 || height <= 0) return
        var maxTile = Math.pow(2, zoom)
        var cx = _lonToWorld(centerLon);  var cy = _latToWorld(centerLat)
        // Extra tile margin so pan doesn't expose empty edges
        var tilesX = Math.ceil(width  / 256) + 5
        var tilesY = Math.ceil(height / 256) + 5
        var ctx_ = Math.floor(cx / 256)
        var cty_ = Math.floor(cy / 256)
        var startX = ctx_ - Math.floor(tilesX / 2) - 1
        var startY = cty_ - Math.floor(tilesY / 2) - 1
        var tiles = []
        for (var ty = startY; ty <= startY + tilesY + 1; ty++) {
            for (var tx = startX; tx <= startX + tilesX + 1; tx++) {
                var vtx = ((tx % maxTile) + maxTile) % maxTile
                var vty = Math.max(0, Math.min(maxTile - 1, ty))
                tiles.push({
                    x:   tx * 256 - cx + width / 2,
                    y:   ty * 256 - cy + height / 2,
                    url: tileMap.tileServer + "/" + zoom + "/" + vtx + "/" + vty
                })
            }
        }
        tileData = tiles
    }

    // ── Auto-fit to route bounding box ────────────────────────────────────────
    function fitRoute() {
        if (!routeCoords || routeCoords.length < 2) { _updateTiles(); return }
        var minLat = routeCoords[0][1], maxLat = routeCoords[0][1]
        var minLon = routeCoords[0][0], maxLon = routeCoords[0][0]
        for (var i = 1; i < routeCoords.length; i++) {
            if (routeCoords[i][1] < minLat) minLat = routeCoords[i][1]
            if (routeCoords[i][1] > maxLat) maxLat = routeCoords[i][1]
            if (routeCoords[i][0] < minLon) minLon = routeCoords[i][0]
            if (routeCoords[i][0] > maxLon) maxLon = routeCoords[i][0]
        }
        centerLat = (minLat + maxLat) / 2
        centerLon = (minLon + maxLon) / 2
        for (var z = 16; z >= 8; z--) {
            zoom = z
            var tl = latLonToScreen(maxLat, minLon)
            var br = latLonToScreen(minLat, maxLon)
            var pad = 48
            if (tl.x >= pad && br.x <= width - pad && tl.y >= pad && br.y <= height - pad) break
        }
        _updateTiles()
        routeCanvas.requestPaint()
    }

    // ── Zoom visual preview ───────────────────────────────────────────────────
    // _tilesZoom = zoom at which tileData was last built.
    // _zoomScale = live scale applied to tileGroup so old tiles approximate
    //              the new zoom level while fresh tiles load.
    property int  _tilesZoom: zoom
    property real _zoomScale: 1.0

    // Debounce tile updates (avoids double-rebuild when both lat+lon change at once)
    Timer {
        id: tileTimer; interval: 60; repeat: false
        onTriggered: {
            tileMap._updateTiles()
            tileMap._tilesZoom = tileMap.zoom
            tileMap._zoomScale = 1.0      // snap back — new tiles are ready
            routeCanvas.requestPaint()
        }
    }

    onWidthChanged:       Qt.callLater(_updateTiles)
    onHeightChanged:      Qt.callLater(_updateTiles)
    onZoomChanged: {
        if (!panMa.pressed) {
            // Show scaled preview of old tiles immediately
            tileMap._zoomScale = Math.pow(2, tileMap.zoom - tileMap._tilesZoom)
            tileTimer.restart()
        }
    }
    onRouteCoordsChanged: Qt.callLater(fitRoute)
    Component.onCompleted: Qt.callLater(fitRoute)

    // When center changes from code (not from drag), rebuild tiles
    onCenterLatChanged: { if (!panMa.pressed) tileTimer.restart() }
    onCenterLonChanged: { if (!panMa.pressed) tileTimer.restart() }

    // ── Wheel / trackpad throttle ─────────────────────────────────────────────
    property real _wheelAccum: 0
    // After each zoom-level change, lock for 180 ms so trackpad can't fly to max
    Timer { id: zoomCooldown; interval: 180; repeat: false }

    // ── Pan drag state ────────────────────────────────────────────────────────
    property real   _dragX:   0; property real   _dragY:   0
    property double _dragLat: 0; property double _dragLon: 0
    // Live pixel offset applied to tileGroup during drag
    property real   _panOffX: 0; property real   _panOffY: 0

    // ── Tile + Canvas layer (translated during drag, scaled during zoom) ────────
    Item {
        id: tileGroup
        // Extend beyond clip boundary so tiles don't vanish mid-pan
        x: tileMap._panOffX - 512;  y: tileMap._panOffY - 512
        width:  tileMap.width  + 1024
        height: tileMap.height + 1024

        // Zoom preview: scale old tiles from map centre while new tiles load
        transform: Scale {
            xScale: tileMap._zoomScale; yScale: tileMap._zoomScale
            // Origin = screen centre in tileGroup's coordinate system
            origin.x: tileMap.width  / 2 + 512
            origin.y: tileMap.height / 2 + 512
        }

        // Background fill
        Rectangle {
            anchors.fill: parent
            color: tileMap.dark ? "#2d3748" : "#e8ecef"
        }

        Repeater {
            model: tileMap.tileData
            Image {
                // offset +512 because tileGroup origin is shifted by -512
                x: modelData.x + 512; y: modelData.y + 512
                width: 256; height: 256
                source: modelData.url
                cache: true; smooth: true; asynchronous: true
                opacity: 0
                onStatusChanged: if (status === Image.Ready) fadeIn.start()
                NumberAnimation on opacity { id: fadeIn; to: 1; duration: 150 }
            }
        }

        // ── Route Canvas ──────────────────────────────────────────────────────
        Canvas {
            id: routeCanvas
            // Canvas covers the visible area (compensate for tileGroup shift)
            x: 512 - tileMap._panOffX; y: 512 - tileMap._panOffY
            width: tileMap.width; height: tileMap.height
            z: 10

            onPaint: {
                var ctx = getContext("2d")
                ctx.clearRect(0, 0, width, height)

                // ── Saved route ───────────────────────────────────────────────
                if (tileMap.routeCoords && tileMap.routeCoords.length >= 2) {
                    var p0 = tileMap.latLonToScreen(tileMap.routeCoords[0][1], tileMap.routeCoords[0][0])
                    // White halo
                    ctx.strokeStyle = "white"; ctx.lineWidth = 6
                    ctx.lineCap = "round"; ctx.lineJoin = "round"; ctx.globalAlpha = 0.7
                    ctx.beginPath(); ctx.moveTo(p0.x, p0.y)
                    for (var i = 1; i < tileMap.routeCoords.length; i++) {
                        var p = tileMap.latLonToScreen(tileMap.routeCoords[i][1], tileMap.routeCoords[i][0])
                        ctx.lineTo(p.x, p.y)
                    }
                    ctx.stroke()
                    // Colored line
                    ctx.strokeStyle = tileMap.lineColor; ctx.lineWidth = 3.5; ctx.globalAlpha = 1.0
                    ctx.beginPath(); ctx.moveTo(p0.x, p0.y)
                    for (var j = 1; j < tileMap.routeCoords.length; j++) {
                        var q = tileMap.latLonToScreen(tileMap.routeCoords[j][1], tileMap.routeCoords[j][0])
                        ctx.lineTo(q.x, q.y)
                    }
                    ctx.stroke()
                    // Start dot
                    ctx.strokeStyle = "white"; ctx.lineWidth = 2.5; ctx.fillStyle = "#22c55e"
                    ctx.beginPath(); ctx.arc(p0.x, p0.y, 7, 0, Math.PI * 2); ctx.fill(); ctx.stroke()
                    // End dot
                    var pn = tileMap.latLonToScreen(
                        tileMap.routeCoords[tileMap.routeCoords.length - 1][1],
                        tileMap.routeCoords[tileMap.routeCoords.length - 1][0])
                    ctx.fillStyle = tileMap.lineColor
                    ctx.beginPath(); ctx.arc(pn.x, pn.y, 5, 0, Math.PI * 2); ctx.fill(); ctx.stroke()
                }

                // ── Edit waypoints preview ────────────────────────────────────
                var wps = tileMap.editWaypoints
                if (wps && wps.length >= 1) {
                    ctx.setLineDash([6, 4])
                    ctx.strokeStyle = tileMap.lineColor; ctx.lineWidth = 2.5
                    ctx.globalAlpha = 0.85; ctx.lineCap = "round"; ctx.lineJoin = "round"
                    ctx.beginPath()
                    var ep0 = tileMap.latLonToScreen(wps[0].lat, wps[0].lon)
                    ctx.moveTo(ep0.x, ep0.y)
                    for (var wi = 1; wi < wps.length; wi++) {
                        var ep = tileMap.latLonToScreen(wps[wi].lat, wps[wi].lon)
                        ctx.lineTo(ep.x, ep.y)
                    }
                    ctx.stroke(); ctx.setLineDash([])
                    for (var di = 0; di < wps.length; di++) {
                        var dp = tileMap.latLonToScreen(wps[di].lat, wps[di].lon)
                        ctx.globalAlpha = 1.0
                        ctx.fillStyle = "white"; ctx.strokeStyle = tileMap.lineColor; ctx.lineWidth = 2
                        ctx.beginPath(); ctx.arc(dp.x, dp.y, 8, 0, Math.PI * 2); ctx.fill(); ctx.stroke()
                        ctx.fillStyle = tileMap.lineColor; ctx.font = "bold 9px sans-serif"
                        ctx.textAlign = "center"; ctx.textBaseline = "middle"
                        ctx.fillText(String(di + 1), dp.x, dp.y)
                    }
                }
            }
        }
    }

    // ── OSM attribution ───────────────────────────────────────────────────────
    Rectangle {
        anchors { right: parent.right; bottom: parent.bottom }
        width: attribLbl.implicitWidth + 10; height: 16
        color: "#ffffffcc"; z: 30
        Label { id: attribLbl; anchors.centerIn: parent
                text: "© OpenStreetMap contributors"; font.pixelSize: 8; color: "#333" }
        MouseArea { anchors.fill: parent; cursorShape: Qt.PointingHandCursor
            onClicked: Qt.openUrlExternally("https://www.openstreetmap.org/copyright") }
    }

    // ── Zoom buttons ──────────────────────────────────────────────────────────
    Column {
        anchors { left: parent.left; top: parent.top; margins: 10 }
        spacing: 2; z: 30
        Rectangle {
            width: 30; height: 30; radius: 6
            color: ziMa.containsMouse ? "#f0f0f0" : "white"; border.width: 1; border.color: "#ccc"
            Label { anchors.centerIn: parent; text: "+"; font.pixelSize: 18; font.weight: Font.Bold; color: "#333" }
            MouseArea { id: ziMa; anchors.fill: parent; hoverEnabled: true; cursorShape: Qt.PointingHandCursor
                        onClicked: tileMap.zoom = Math.min(18, tileMap.zoom + 1) }
        }
        Rectangle {
            width: 30; height: 30; radius: 6
            color: zoMa.containsMouse ? "#f0f0f0" : "white"; border.width: 1; border.color: "#ccc"
            Label { anchors.centerIn: parent; text: "−"; font.pixelSize: 18; font.weight: Font.Bold; color: "#333" }
            MouseArea { id: zoMa; anchors.fill: parent; hoverEnabled: true; cursorShape: Qt.PointingHandCursor
                        onClicked: tileMap.zoom = Math.max(8, tileMap.zoom - 1) }
        }
    }

    // ── Edit mode badge (top-right) ───────────────────────────────────────────
    Rectangle {
        visible: tileMap.editMode
        anchors { top: parent.top; right: parent.right; margins: 8 }
        height: 24; width: editLbl.implicitWidth + 16; radius: 6
        color: tileMap.lineColor; z: 30
        Label { id: editLbl; anchors.centerIn: parent
                text: "✏ " + tileMap.editWaypoints.length + " точек  ·  клик — добавить  ·  клик по точке — удалить"
                font.pixelSize: 10; font.weight: Font.DemiBold; color: "#fff" }
    }

    // ── Mouse: pan + zoom + edit clicks ──────────────────────────────────────
    MouseArea {
        id: panMa
        anchors.fill: parent; z: 20
        cursorShape: tileMap.editMode ? Qt.CrossCursor : Qt.OpenHandCursor

        property bool _didDrag: false

        onPressed: function(e) {
            _didDrag = false
            tileMap._dragX   = e.x;  tileMap._dragY   = e.y
            tileMap._dragLat = tileMap.centerLat
            tileMap._dragLon = tileMap.centerLon
            cursorShape = tileMap.editMode ? Qt.CrossCursor : Qt.ClosedHandCursor
        }

        onPositionChanged: function(e) {
            if (!pressed) return
            var dx = e.x - tileMap._dragX
            var dy = e.y - tileMap._dragY
            // 5 px threshold — gives click actions room to breathe (especially on trackpad)
            if (Math.abs(dx) > 5 || Math.abs(dy) > 5) _didDrag = true
            tileMap._panOffX = dx
            tileMap._panOffY = dy
        }

        onReleased: function(e) {
            cursorShape = tileMap.editMode ? Qt.CrossCursor : Qt.OpenHandCursor
            if (!_didDrag) return
            // Commit pan — works in both view and edit mode so the user can
            // navigate the map while drawing waypoints
            var dx = e.x - tileMap._dragX
            var dy = e.y - tileMap._dragY
            var sc = tileMap._scale()
            tileMap.centerLon = tileMap._dragLon - dx * 360 / sc
            tileMap.centerLat = tileMap._worldYToLat(tileMap._latToWorld(tileMap._dragLat) - dy)
            tileMap._panOffX = 0
            tileMap._panOffY = 0
        }

        onClicked: function(e) {
            if (!tileMap.editMode || _didDrag) return
            var wps = tileMap.editWaypoints
            // Click within 16 px of an existing waypoint → delete that waypoint
            for (var i = 0; i < wps.length; i++) {
                var sp = tileMap.latLonToScreen(wps[i].lat, wps[i].lon)
                var ddx = e.x - sp.x; var ddy = e.y - sp.y
                if (ddx * ddx + ddy * ddy <= 16 * 16) {
                    var nw = wps.slice(); nw.splice(i, 1)
                    tileMap.editWaypoints = nw
                    return
                }
            }
            // Otherwise add a new waypoint at the clicked position
            var ll = tileMap.screenToLatLon(e.x, e.y)
            tileMap.addWaypoint(ll.lat, ll.lon)
        }

        onWheel: function(e) {
            // Throttle: trackpad fires many tiny events — accumulate until 60 units,
            // then lock for 180 ms so a fast swipe doesn't fly to max/min zoom.
            if (zoomCooldown.running) { e.accepted = true; return }
            tileMap._wheelAccum += e.angleDelta.y
            if (tileMap._wheelAccum >= 60) {
                tileMap._panOffX = 0; tileMap._panOffY = 0
                tileMap.zoom = Math.min(18, tileMap.zoom + 1)
                tileMap._wheelAccum = 0
                zoomCooldown.restart()
            } else if (tileMap._wheelAccum <= -60) {
                tileMap._panOffX = 0; tileMap._panOffY = 0
                tileMap.zoom = Math.max(8, tileMap.zoom - 1)
                tileMap._wheelAccum = 0
                zoomCooldown.restart()
            }
            e.accepted = true
        }
    }
}
