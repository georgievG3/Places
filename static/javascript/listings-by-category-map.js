var map = L.map('map').setView([42.5, 24.5], 7);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    gestureHandling: true,
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

if (typeof listingLocations !== "undefined" && listingLocations.length) {
    listingLocations.forEach(listing => {
        const popupContent = `
            <div style="text-align: center;">
                <img src="${listing.image}" alt="${listing.title}" style="width: 100px; height: 70px; object-fit: cover; border-radius: 8px;">
                <h4 style="margin: 5px 0;">${listing.title}</h4>
                <p>от ${listing.price} лв.</p>
                <a href="/listings/listing/${listing.slug}/" class="map-popup-link">Виж обявата</a>
            </div>
        `;
        L.marker([listing.lat, listing.lng])
            .addTo(map)
            .bindPopup(popupContent);
    });

    const bounds = listingLocations.map(loc => [loc.lat, loc.lng]);
    map.fitBounds(bounds, { padding: [35, 35] });
}