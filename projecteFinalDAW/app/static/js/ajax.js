function getSelectedGroupId() {

    value = document.getElementById('groupsDropdown').value;
    //alert(value);
    return value;
}

function toggleFavorite(productId, isFavorite, group_id) {
    let button = document.getElementById(`favoriteButton${productId}`);
    //alert(group_id);

    if(group_id == undefined){
        
        group_id = "user";
    }
    //let url = "";

    if(group_id != "user") {

        url = isFavorite ? `/removeGroupFavorite/${productId}/${group_id}/` : `/addGroupFavorite/${productId}/${group_id}/`;
    } else {

        url = isFavorite ? `/removeFavorite/${productId}/` : `/addFavorite/${productId}/`;
    }
    let newImageSrc = isFavorite ? "/static/en.png" : "/static/ea.png";
    let newOnClick = `toggleFavorite('${productId}', ${!isFavorite}, '${group_id}')`;

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


function addProductToCart(productId, group_id) {

    if(group_id == undefined) {
        group_id = "user";
    }

    if (group_id != "user") {
        url = `/addProductToList/${productId}/${group_id}/`;
    } else {
        url = `/addProductToList/${productId}/`;
    }

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
            let button = document.getElementById(`addToCartButton${productId}`, getSelectedGroupId());
            button.innerText = `En el carret: ${data.quantity}`;
        }
    })
    .catch(error => console.error("Error:", error));
}

function addOne(productId, group_id) {

    if(group_id == undefined || group_id == "") {
        group_id = "user";
    }


    let url = "";

    if (group_id != "user") {
        url = `/addOneProduct/${productId}/${group_id}/`;
    } else {
        url = `/addOneProduct/${productId}/`;
    }

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

        let url2 = "";

        if (url == `/addOneProduct/${productId}/${group_id}/`){

            url2 = `/shoppingCartList/${group_id}/`;
        } else {

            url2 = `/shoppingCartList/`;
        }

        return fetch(url2 , {
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

function deleteOne(productId, group_id) {

    if(group_id == undefined || group_id == "") {
        group_id = "user";
    }

    let url = "";

    if (group_id != "user") {
        url = `/removeOneProduct/${productId}/${group_id}/`;
    } else {
        url = `/removeOneProduct/${productId}/`;
    }

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

        let url2 = "";
        if (url == `/removeOneProduct/${productId}/${group_id}/`){

            url2 = `/shoppingCartList/${group_id}/`;
        } else{

            url2 = `/shoppingCartList/`;
        }  

        return fetch(url2 , {
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

function removeProduct(productId, group_id) {
    
    if(group_id == undefined || group_id == "") {
        group_id = "user";
    }

    let url = "";
    
    if (group_id != "user") {
        url = `/removeProduct/${productId}/${group_id}/`;
    } else {
        url = `/removeProduct/${productId}/`;
    }

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

        let url2 = "";

        if (url == `/removeProduct/${productId}/${group_id}/`){
            url2 = `/shoppingCartList/${group_id}/`;
        } else {
            url2 = `/shoppingCartList/`;
        }

        return fetch(url2 , {
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

function getCategoryId() {
    const pathParts = window.location.pathname.split('/');
    return pathParts[2];
}

function refreshGroupProducts(group_id) {
    let url = "";

    category = getCategoryId();

    if (group_id != "user") {
        url = `/products/${category}/${group_id}`;
    } else {
        url = `/products/${category}/`;
    }

    fetch(url, {
        method: "GET",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json"
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Server response error");
        }
        return response.text();
    })
    .then(html => {
        let parser = new DOMParser();
        let doc = parser.parseFromString(html, "text/html");
        let productsElement = doc.querySelector("#productsContainer");
        if (productsElement) {
            let productsContainer = document.getElementById("productsContainer");
            if (productsContainer) {
                productsContainer.innerHTML = productsElement.innerHTML;
            } else {
                console.error("Error: No hi ha cap contenedor de productes en el document actual.");
            }
        } else {
            console.error("Error: Contenidor no trobat");
        }
    })
    .catch(error => console.error("Error:", error));
}

function refreshFavoriteGroups(group_id) {
    let url = "";

    if (group_id != "user") {
        url = `/favorites/${group_id}`;
    } else {
        url = `/favorites/`;
    }

    fetch(url, {
        method: "GET",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json"
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Server response error");
        }
        return response.text();
    })
    .then(html => {
        let parser = new DOMParser();
        let doc = parser.parseFromString(html, "text/html");
        let productsElement = doc.querySelector(".divProducts-container"); 
        if (productsElement) {
            let productsContainer = document.querySelector(".divProducts-container");
            if (productsContainer) {
                productsContainer.innerHTML = productsElement.innerHTML;
            } else {
                console.error("Error: No se encontró el contenedor de productos en el documento actual.");
            }
        } else {
            console.error("Error: Contenedor de productos no encontrado en la respuesta.");
        }
    })
    .catch(error => console.error("Error:", error));
}


function refreshGroupsList(group_id) {
    if (!group_id) {
        group_id = "user";
    }

    let url = "";

    if (group_id != "user") {
        url = `/shoppingCartList/${group_id}/`;
    }
    else {
        url = `/shoppingCartList/`;
    }

    fetch(url, {
        method: "GET",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json"
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Error en la respuesta del servidor");
        }
        return response.text();
    })
    .then(html => {
        let parser = new DOMParser();
        let doc = parser.parseFromString(html, "text/html");

        let newProducts = doc.querySelectorAll(".divCartProducts");

        let newTotal = doc.querySelector(".divTotal");

        let cartContainer = document.querySelector(".content");
        cartContainer.querySelectorAll(".divCartProducts").forEach(el => el.remove());

        newProducts.forEach(product => cartContainer.appendChild(product));

        let currentTotal = cartContainer.querySelector(".divTotal");
        if (currentTotal && newTotal) {
            currentTotal.innerHTML = newTotal.innerHTML;
        }
    })
    .catch(error => console.error("Error:", error));
}

function refreshGroupTickets(group_id) {
    let url = "";

    if (group_id != "user") {
        url = `/history/${group_id}`;
    } else {
        url = `/history/`;
    }

    fetch(url, {
        method: "GET",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json"
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Server response error");
        }
        return response.text();
    })
    .then(html => {
        let parser = new DOMParser();
        let doc = parser.parseFromString(html, "text/html");
        let ticketsElement = doc.querySelector("#ticketsContainer"); // Selecciona el contenedor de tickets
        if (ticketsElement) {
            let ticketsContainer = document.getElementById("ticketsContainer");
            if (ticketsContainer) {
                ticketsContainer.innerHTML = ticketsElement.innerHTML; // Actualiza el contenido del contenedor
            } else {
                console.error("Error: No se encontró el contenedor de tickets en el documento actual.");
            }
        } else {
            console.error("Error: Contenedor de tickets no encontrado en la respuesta.");
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