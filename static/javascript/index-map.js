document.addEventListener('DOMContentLoaded', function () {
    let zoomLevel = 7;

    if (window.innerWidth <= 768) {
        zoomLevel = 6;
    }

    var map = L.map('map').setView([42.5, 24.5], zoomLevel);

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    markersData.forEach(function (m) {
        var marker = L.marker([m.lat, m.lng]).addTo(map);
        marker.bindPopup(`
            <div style="text-align: center;">
                <img src="${m.image}" alt="${m.title}" style="width: 100px; height: 70px; object-fit: cover; border-radius: 8px;">
                <h4 style="margin: 5px 0;">${m.title}</h4>
                <p>от ${m.price} лв.</p>
                <a href="/listings/listing/${m.slug}/" class="map-popup-link">Виж обявата</a>
            </div>
        `);
    });
});