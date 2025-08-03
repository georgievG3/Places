document.addEventListener('DOMContentLoaded', function () {
        const latElement = document.getElementById('lat');
        const lngElement = document.getElementById('lng');

        const lat = parseFloat(latElement?.textContent);
        const lng = parseFloat(lngElement?.textContent);

        if (!isNaN(lat) && !isNaN(lng)) {
            const map = L.map('map').setView([lat, lng], 10);

            L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
                gestureHandling: true,
                maxZoom: 19,
                attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
            }).addTo(map);

            L.marker([lat, lng]).addTo(map);
        } else {
            console.error('Координатите не са валидни:', lat, lng);
        }
    });