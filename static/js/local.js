
debugger;

function renderMap(results) {
    mapboxgl.accessToken = 'pk.eyJ1Ijoia2FyYXlvdW50IiwiYSI6ImNpa3l3NjNoODA5M3J1YWtzbWN5bjFxd2MifQ.lpKDreQHp7X-urPys6nmSg';
    var markers = results;

    var map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/streets-v8',
        center: [-122.4, 37.77],
        zoom: 9.5
    });

    map.on('style.load', function () {
        map.addSource("markers", markers);

        map.addLayer({
            "id": "markers",
            "interactive": true,
            "type": "symbol",
            "source": "markers",
            "layout": {
                "icon-image": "{marker-symbol}-15",
                "icon-allow-overlap": true
            }
        });
    });

    var popup = new mapboxgl.Popup();

    map.on('click', function (e) {
        map.featuresAt(e.point, {
            radius: 7.5,
            includeGeometry: true,
            layer: 'markers'
        }, function (err, features) {

            if (err || !features.length) {
                popup.remove();
                return;
            }

            var feature = features[0];

            popup.setLngLat(feature.geometry.coordinates)
                .setHTML(feature.properties.description)
                .addTo(map);
        });
    });

    map.on('mousemove', function (e) {
        map.featuresAt(e.point, {
            radius: 7.5,
            layer: 'markers'
        }, function (err, features) {
            map.getCanvas().style.cursor = (!err && features.length) ? 'pointer' : '';
        });
    });
    }

$.get("/get_markers.json", renderMap);
