var map = L.map('map').setView([42.5, 24.5], 7);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    gestureHandling: true,
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

let marker;

    map.on('click', function(e) {
        const lat = e.latlng.lat.toFixed(6);
        const lng = e.latlng.lng.toFixed(6);

        if (marker) {
            map.removeLayer(marker);
        }

        marker = L.marker([lat, lng]).addTo(map);

        document.getElementById('id_latitude').value = lat;
        document.getElementById('id_longitude').value = lng;
    });