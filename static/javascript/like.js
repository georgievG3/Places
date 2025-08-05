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

document.querySelectorAll('.listing-like').forEach(container => {
    const button = container.querySelector('.like-btn, a');
    if (!button) return;

    container.setAttribute('data-listing-id', container.getAttribute('data-listing-id') || button.closest('[data-listing-id]')?.getAttribute('data-listing-id'));

    button.addEventListener('click', async (e) => {
        e.preventDefault();

        const listingId = container.getAttribute('data-listing-id');
        if (!listingId) return;

        try {
            const response = await fetch(`/listings/like/${listingId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Accept': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                },
                credentials: 'same-origin',
            });

            if (!response.ok) throw new Error('Network response not ok');

            const data = await response.json();

            if (data.liked) {
                button.innerHTML = '<i class="fa-solid fa-heart" style="color:#ed4040;"></i>';
            } else {
                const userListingCard = container.closest('.user-listing-card');
                if (userListingCard) {
                    userListingCard.remove();
                } else {
                    button.innerHTML = '<i class="fa-regular fa-heart"></i>';
                }
            }
        } catch (error) {
            alert('Неуспешно харесване, опитай пак.');
            console.error(error);
        }
    });
});
