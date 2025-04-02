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


function addProductToCart(productId) {
    let url = `/addProductToList/${productId}/`;

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
        if (data.quantity !== undefined) {
            let button = document.getElementById(`addToCartButton${productId}`);
            button.innerText = `En el carret: ${data.quantity}`;
        }
    })
    .catch(error => console.error("Error:", error));
}

function addOne(productId) {
    let url = `/addOneProduct/${productId}/`;

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
        if (data.quantity !== undefined) {
            let p = document.getElementById(`quantity${productId}`);
            p.innerText = `${data.quantity}`;
        }


        return fetch(`/shoppingCartList/`, {
            method: "GET",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
                "Content-Type": "application/json"
            }
        });
    })
    .then(response => response.text())
    .then(html => {
        let parser = new DOMParser();
        let doc = parser.parseFromString(html, "text/html");
        let totalElement = doc.querySelector("#total");
        if (totalElement) {
            let totalPriceElement = document.getElementById("total");
            if (totalPriceElement) {
                totalPriceElement.innerText = totalElement.innerText;
            }
        }
    })
    .catch(error => console.error("Error:", error));
}

function deleteOne(productId) {
    let url = `/removeOneProduct/${productId}/`;

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
        if (data.quantity !== undefined) {
            let p = document.getElementById(`quantity${productId}`);    
            if (p) {
                p.innerText = `${data.quantity}`;
            }
        }

        return fetch(`/shoppingCartList/`, {
            method: "GET",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
                "Content-Type": "application/json"
            }
        });
    })
    .then(response => response.text())
    .then(html => {
        let parser = new DOMParser();
        let doc = parser.parseFromString(html, "text/html");
        let totalElement = doc.querySelector("#total");
        if (totalElement) {
            let totalPriceElement = document.getElementById("total");
            if (totalPriceElement) {
                totalPriceElement.innerText = totalElement.innerText;
            }
        }
    })
    .catch(error => console.error("Error:", error));
}

function removeProduct(productId) {
    let url = `/removeProduct/${productId}/`;

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
        if (data.quantity !== undefined) {
            let p = document.getElementById(`quantity${productId}`);    
           
            if (p) {
                p.innerText = `${data.quantity}`;
            }
        }
        let product = document.getElementById(`product${productId}`);
        product.remove();

        return fetch(`/shoppingCartList/`, {
            method: "GET",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
                "Content-Type": "application/json"
            }
        });
    })
    .then(response => response.text())
    .then(html => {
        let parser = new DOMParser();
        let doc = parser.parseFromString(html, "text/html");
        let totalElement = doc.querySelector("#total");
        if (totalElement) {
            let totalPriceElement = document.getElementById("total");
            if (totalPriceElement) {
                totalPriceElement.innerText = totalElement.innerText;
            }
        }
    })
    .catch(error => console.error("Error:", error));
}

function checkProduct(productId) {

    let checkbox = document.getElementById(`checkbox${productId}`);
    let div = document.getElementById(`product${productId}`);
    let name = document.getElementById(`name${productId}`);
    let price = document.getElementById(`price${productId}`);
    let quantity = document.getElementById(`quantity${productId}`);
    let minus = document.getElementById(`-${productId}`);
    let plus = document.getElementById(`+${productId}`);
    let image = document.getElementById(`image${productId}`);
    let remove = document.getElementById(`removeButton${productId}`);
    

    if (checkbox.checked) {

        div.style.backgroundColor = "#d4fcd4";
        name.style.filter = "blur(2px)";
        price.style.filter = "blur(2px)";
        quantity.style.filter = "blur(2px)";
        minus.style.filter = "blur(2px)";
        minus.disabled = true;
        plus.style.filter = "blur(2px)";
        plus.disabled = true;
        image.style.filter = "blur(2px)";
        remove.style.filter = "blur(2px)";
        remove.backgroundColor = "#d4fcd4";
        remove.disabled = true;

        div.style.transition = "background-color 0.3s ease, filter 0.3s ease";
        
    } else {

        div.style.backgroundColor = "#ffffff";
        name.style.filter = "blur(0px)";
        price.style.filter = "blur(0px)";
        quantity.style.filter = "blur(0px)";
        minus.style.filter = "blur(0px)";
        minus.disabled = false;
        plus.style.filter = "blur(0px)";
        plus.disabled = false;
        image.style.filter = "blur(0px)";
        remove.style.filter = "blur(0px)";
        remove.disabled = false;
    }
}

function buyProducts(){
    let url = `/removeChecked/`;

    fetch(url, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),  
            "Content-Type": "application/json"
        },
        body: JSON.stringify({})
    })
    .then(response => response.json())
    .catch(error => console.error("Error:", error));
}

function addProductHistory(productId, ticketId) {
    let url = `/addFromHistory/${productId}/${ticketId}/`;

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

        let buttons = document.querySelectorAll(`[id^="addButton${productId}"]`);
        buttons.forEach(button => {
            button.outerHTML = `<button class="tickButton" id="addedButton${productId}" type="button">
                    <img class="buttonImg" src="/static/tick.png" alt="Producte ja a la llista">
                    </button>`;
        });
    })
    .catch(error => console.error("O aqui:", error));
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