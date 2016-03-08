
function buildMarkerList(markerJSON) {
    var data = markerJSON;
    var markers = [];
    for (var i = 1; i <= Object.keys(data).length; i++) {
        var biz = data[i];
        var bizLat = biz.biz_lat;
        var bizLng = biz.biz_long;
        var bizName = biz.biz_name;
        var bizAddr = biz.biz_addr;
        var bizCity = biz.biz_city;
        var bizURL = biz.biz_url;
        var bizNum = biz.biz_num;

        var bizContentString = '<div id="content">' +
            '<h4 class="firstHeading">' + bizName + '</h4>' +
            '<div id="bodyContent">' +
            '<span>' + bizAddr + '<br>' + bizCity + '</span><br><a href="' +
            bizURL + '">find on Yelp</a></div></div>';

        var current = {
            "lat": bizLat,
            "lng": bizLng,
            "name": bizName,
            "content": bizContentString,
            "num": bizNum
        };
        markers.push(current);
    }
    return markers;
}

function initMap(result) {
    var markerData = buildMarkerList(result);
    var SFCenter = new google.maps.LatLng(37.79, -122.34);
    var myOptions = {
        zoom: 11,
        center: SFCenter,
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        mapTypeControl: false
    };
    var map = new google.maps.Map(document.getElementById("map"),myOptions);

    var markers = [];
    var infoWindows = [];
    var codePointA = 'A'.charCodeAt(0);

    for (i = 0; i < markerData.length; i++) {
        biz = markerData[i];
        var markerLabel = String.fromCodePoint(codePointA + i);
        marker = new google.maps.Marker({
            position: new google.maps.LatLng(biz.lat, biz.lng),
            map: map,
            title: biz.name,
            content: biz.content,
            label: markerLabel
        });
        var infoWindow = new google.maps.InfoWindow(), marker, i;
        markers.push(marker);
        infoWindows.push(infoWindow);
        google.maps.event.addListener(marker, 'click', (function(marker) {
            return function() {
                infoWindow.setContent(marker.content);
                infoWindow.open(map, marker);
            }
        })(markers[i]));
    }
}

$.get("/get_businesses_for_markers.json", initMap);