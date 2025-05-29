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

function addProductToCart2(productId) {
    
    url = `/addProductToListMercadoLivre/${productId}/`;

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
            let button = document.getElementById(`addToCartButton2${productId}`);
            button.innerText = `En el carret: ${data.quantity}`;
        }
    })
    .catch(error => console.error("Error:", error));
}

function toggleFavorite2(productId, isFavorite) {
    let button = document.getElementById(`favoriteButton2${productId}`);
    
    let url = isFavorite ? `/removeFavoriteMercadoLivre/${productId}/` : `/addFavoriteMercadoLivre/${productId}/`;
    let newImageSrc = isFavorite ? "/static/en.png" : "/static/ea.png";
    let newOnClick = `toggleFavorite2('${productId}', ${!isFavorite})`;

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
    let supermarketImg = document.getElementById(`supermarket${productId}`);
    

    if (checkbox.checked) {

        div.style.backgroundColor = "#e0e0e0";
        name.style.textDecoration = "line-through";
        price.style.textDecoration = "line-through";
        quantity.style.textDecoration = "line-through";
        minus.disabled = true;
        plus.disabled = true;
        remove.backgroundColor = "#d4fcd4";
        remove.disabled = true;
        div.style.transition = "background-color 0.3s ease, filter 0.3s ease";
        
    } else {

        div.style.backgroundColor = "#ffffff";
        name.style.textDecoration = "none";
        price.style.textDecoration = "none";
        quantity.style.textDecoration = "none";
        minus.disabled = false;
        plus.disabled = false;
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

    //document.cookie = `group_id=${group_id}; path=/; max-age=86400`;

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

    document.cookie = `group_id=${group_id}; path=/; max-age=86400`;
    
    window.location.href = url;
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
        let ticketsElement = doc.querySelector("#ticketsContainer"); 
        if (ticketsElement) {
            let ticketsContainer = document.getElementById("ticketsContainer");
            if (ticketsContainer) {
                ticketsContainer.innerHTML = ticketsElement.innerHTML; 
            } else {
                console.error("Error: No se encontró el contenedor de tickets en el documento actual.");
            }
        } else {
            console.error("Error: Contenedor de tickets no encontrado en la respuesta.");
        }
    })
    .catch(error => console.error("Error:", error));
}

function addFromInfo(productId){

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
            let quantityElement = document.getElementById('totalProduct');
        if (quantityElement) {
            quantityElement.innerText = `Al carret: ${data.quantity}`;
        }
        }

    })

}

function addFirstFromInfo(productId){

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
        let actionsContainer = document.getElementById('actionsContainer');
        if (actionsContainer) {
            actionsContainer.innerHTML = `
            <div class="divHelper">
                <button class="buttonsContainer" id="removeFromCart" class="removeFromCart" onclick="removeFromInfo('${productId}')">-</button>
                <p id="totalProduct">Al carret: ${data.quantity !== undefined ? data.quantity : 0}</p>
                <button class="buttonsContainer" id="addToCart" class="addToCart" onclick="addFromInfo('${productId}')">+</button>
            </div>
            `;
        }
    })
}

function removeFromInfo(productId){

    let group_id = 1;

    let url = `/removeOneProduct/${productId}/${group_id}/`;

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


        let actionsContainer = document.getElementById('actionsContainer');
        if(data.quantity !== undefined) {
            let quantityElement = document.getElementById('totalProduct');
            if (quantityElement) {
                quantityElement.innerText = `Al carret: ${data.quantity}`;
            }
        }else {
            if (actionsContainer) {
                
                if(/[a-zA-Z]/.test(productId)){
                    actionsContainer.innerHTML = `
                        <button class="buttonsContainer" id="addToCartButton2{{ product.id }}" onclick="addFirstFromInfo2('${productId}')">Afegir producte</button>
                    `;
                }else{
                    actionsContainer.innerHTML = `
                        <button class="buttonsContainer" id="addToCartButton{{ product.id }}" onclick="addFirstFromInfo('${productId}')">Afegir producte</button>
                    `;
                }
            }
        }
    })
}

function addFirstFromInfo2(productId){

    let url = `/addProductToListMercadoLivre/${productId}/`;

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
        let actionsContainer = document.getElementById('actionsContainer');
        if (actionsContainer) {
            actionsContainer.innerHTML = `
            <div class="divHelper">
                <button class="buttonsContainer" id="removeFromCart" class="removeFromCart" onclick="removeFromInfo('${productId}')">-</button>
                <p id="totalProduct">Al carret: ${data.quantity !== undefined ? data.quantity : 0}</p>
                <button class="buttonsContainer" id="addToCart" class="addToCart" onclick="addFromInfo('${productId}')">+</button>
            </div>
            `;
        }
    })
}

function buscarProductos(variable) {
    const query = document.getElementById('search-input').value;
    let group_id = "user"; // Default group_id

    if (variable === "1") {
        group_id = getSelectedGroupId();
    }
    if (query.trim() === '') {
        document.getElementById('resultados-container').innerHTML = '';
        return;
    }

    let url = "";

    if (group_id != "user" ) {
        url = `/searchProducts/${encodeURIComponent(query)}/${group_id}`;
    } else {
        url = `/searchProducts/${encodeURIComponent(query)}/`;
    }

        
    fetch(url, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })

    .then(res => res.json())
    .then(data => {
        const container = document.getElementById('divProducts');
        container.innerHTML = '';

        if (data.length === 0) {
            container.innerHTML = '<p>No se encontraron productos.</p>';
            return;
        }

        if (data.user != null) {
            let contador = 0;

            //console.log(data.qnty);
            data.resultados.forEach(producto => {
                
                const divProducts = document.createElement('div');
                const div = document.createElement('div');
                div.className = 'divProducts';
               
                let addToCartButton = '';
                let favoriteButton = '';

                //console.log(data.qnty[producto.id[0]]);
                                
                if (data.shopingList && data.shopingList.includes(producto.id)) {
                    
                    addToCartButton = `<button class="buttonsContainer" id="addToCartButton${producto.id}" onclick="addProductToCart('${producto.id}', '${group_id}')">En el carret</button>`;
                } else {
                    addToCartButton = `<button class="buttonsContainer" id="addToCartButton${producto.id}" onclick="addProductToCart('${producto.id}', '${group_id}')">Afegir al carret</button>`;
                }

                
                if (data.favorites && data.favorites.includes(producto.id)) {
                    favoriteButton = `<button class="buttonsContainer" id="favoriteButton${producto.id}" onclick="toggleFavorite('${producto.id}', true, '${group_id}')"><img style="width: 16px; height: 16px;" src="/static/ea.png" alt="Afegir a favorits"></button>`;
                } else {

                    favoriteButton = `<button class="buttonsContainer" id="favoriteButton${producto.id}" onclick="toggleFavorite('${producto.id}', false, '${group_id}')"><img style="width: 16px; height: 16px;" src="/static/en.png" alt="Treure de favorits"></button>`;
                }

                div.innerHTML = `
                    <a class="afix" href="/productInfo/${producto.id}">
                        <img src="${producto.image}" alt="${producto.name}">
                    </a>
                    <strong>${producto.name}</strong>
                    <div class="price">
                        ${producto.price && producto.old_price ? `<span class="oldPrice">${producto.old_price}€</span>` : ''}
                        <span>${producto.price ? producto.price : ''}€</span>
                    </div>
                    <hr>
                    <a class="moreInfo" href="/productInfo/${producto.id}">Más información</a>
                    ${addToCartButton}
                    ${favoriteButton}
                `;
                container.appendChild(div);
            });

            ++contador;
        } else {
                
            data.resultados.forEach(producto => {
                const div = document.createElement('div');
                div.className = 'divProducts';
               
                                
                div.innerHTML = `
                    <a class="afix" href="/productInfo/${producto.id}">
                        <img src="${producto.image}" alt="${producto.name}">
                    </a>
                    <strong>${producto.name}</strong>
                    <div class="price">
                        ${producto.price && producto.old_price ? `<span class="oldPrice">${producto.old_price}€</span>` : ''}
                        <span>${producto.price ? producto.price : ''}€</span>
                    </div>
                    <hr>
                    <a class="moreInfo" href="/productInfo/${producto.id}">Más información</a>  
                `;
                container.appendChild(div);
            });
        }
    })
    .catch(error => console.error('Error:', error));
        
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