/**
 * Created by Kara on 2/29/16.
 */

debugger;

function renderMap(results) {
    mapboxgl.accessToken = 'pk.eyJ1Ijoia2FyYXlvdW50IiwiYSI6ImNpa3l3NjNoODA5M3J1YWtzbWN5bjFxd2MifQ.lpKDreQHp7X-urPys6nmSg';
    var markers = results;

    var map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/streets-v8',
        center: [-122.45, 37.77],
        zoom: 11
    });

    map.on('style.load', function () {
        // Add marker data as a new GeoJSON source.
        map.addSource("markers", markers);


        // Add a layer showing the markers.
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

    // When a click event occurs near a marker icon, open a popup at the location of
    // the feature, with description HTML from its properties.
    map.on('click', function (e) {
        map.featuresAt(e.point, {
            radius: 7.5, // Half the marker size (15px).
            includeGeometry: true,
            layer: 'markers'
        }, function (err, features) {

            if (err || !features.length) {
                popup.remove();
                return;
            }

            var feature = features[0];

            // Popuplate the popup and set its coordinates
            // based on the feature found.
            popup.setLngLat(feature.geometry.coordinates)
                .setHTML(feature.properties.description)
                .addTo(map);
        });
    });

    // Use the same approach as above to indicate that the symbols are clickable
    // by changing the cursor style to 'pointer'.
    map.on('mousemove', function (e) {
        map.featuresAt(e.point, {
            radius: 7.5, // Half the marker size (15px).
            layer: 'markers'
        }, function (err, features) {
            map.getCanvas().style.cursor = (!err && features.length) ? 'pointer' : '';
        });
    });
    }

$.get("/get_markers.json", renderMap);
