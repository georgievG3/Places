function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.querySelectorAll('.listing-like .like-btn').forEach(button => {
    button.addEventListener('click', async (e) => {
        e.preventDefault();

        const container = button.closest('.listing-like');
        const listingId = container.getAttribute('data-listing-id');

        const response = await fetch(`/listings/like/${listingId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
            },
            credentials: 'same-origin',
        });

        if (response.ok) {
            const data = await response.json();
            if (data.liked) {
                button.innerHTML = '<i class="fa-solid fa-heart" style="color:#ed4040;"></i>';
            } else {
                button.innerHTML = '<i class="fa-regular fa-heart"></i>';
            }
        } else {
            alert('Неуспешно харесване, опитай пак.');
        }
    });
});