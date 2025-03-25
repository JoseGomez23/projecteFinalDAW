function toggleFavorite(productId, isFavorite) {
    let button = document.getElementById(`favoriteButton${productId}`);
    let url = isFavorite ? `/removeFavorite/${productId}/` : `/addFavorite/${productId}/`;
    let newImageSrc = isFavorite ? "/static/en.png" : "/static/ea.png";
    let newOnClick = `toggleFavorite('${productId}', ${!isFavorite})`;

    fetch(url, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),  
            "Content-Type": "application/json"
        },
        body: JSON.stringify({})
    })
    .then(response => response.json())
    .then(data => {
        if (button) {
            button.innerHTML = `<img style="width: 16px; height: 16px;" src="${newImageSrc}" alt="${isFavorite ? 'Afegir a favorits' : 'Treure de favorits'}">`;
            button.setAttribute("onclick", newOnClick);
        } else {
            console.error("Error: Botón no encontrado.");
        }
    })
    .catch(error => console.error("Error:", error));
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}