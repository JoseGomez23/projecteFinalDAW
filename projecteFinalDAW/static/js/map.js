mapboxgl.accessToken = 'pk.eyJ1Ijoiam9zZTA4MDUiLCJhIjoiY205Y3R5MTZ4MDZybDJqcXRvaXQ2YWtzeiJ9.jaLJjbJH6dZ6a-21MjnayA';

navigator.geolocation.getCurrentPosition(successLocation, errorLocation, {
    enableHighAccuracy: true
});

let map;

function successLocation(position) {
    const userCoords = [position.coords.longitude, position.coords.latitude];
    mostrarMapaConUbicacion(userCoords);
    buscarMercadonas(userCoords);
}

function errorLocation() {
    alert("Habilita la geolocalització per poder veure el mapa");
}

function mostrarMapaConUbicacion(center) {
    map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/streets-v11',
        center: center,
        zoom: 14
    });

    new mapboxgl.Marker({ color: 'red' })
        .setLngLat(center)
        .setPopup(new mapboxgl.Popup().setText("La teva ubicació"))
        .addTo(map);
}

async function buscarMercadonas(coord) {
    const [lng, lat] = coord;

    const apiKey = '126b536ee8b64c9087568b3bd7d32334';  
    const url = `https://api.opencagedata.com/geocode/v1/json?q=Lidl&key=${apiKey}&limit=10&countrycode=es`;

    const response = await fetch(url);
    const data = await response.json();

    mercadona1 = new mapboxgl.Marker({ color: 'yellow' })
        .setLngLat([2.7767185 ,41.6775732])
        .setPopup(new mapboxgl.Popup().setText("Mercadona"))
        .addTo(map);
    
    mercadona2 = new mapboxgl.Marker({ color: 'yellow' })
        .setLngLat([2.779908 ,41.667829])
        .setPopup(new mapboxgl.Popup().setText("Mercadona"))
        .addTo(map);
    
    lidl1 = new mapboxgl.Marker({ color: 'purple' })
        .setLngLat([2.774523 ,41.677298])
        .setPopup(new mapboxgl.Popup().setText("Lidl"))
        .addTo(map);
    
        
    data.results.forEach((place) => {
        const marker = new mapboxgl.Marker({ color: 'blue' })
            .setLngLat([place.geometry.lng, place.geometry.lat])
            .setPopup(new mapboxgl.Popup().setHTML(`<strong>${place.formatted}</strong>`))
            .addTo(map);
    });

    const url2 = `https://api.opencagedata.com/geocode/v1/json?q=Mercadona&key=${apiKey}&limit=10&countrycode=es`;

    const response2 = await fetch(url2);
    const data2 = await response2.json();

    data2.results.forEach((place) => {
        const marker = new mapboxgl.Marker({ color: 'green' })
            .setLngLat([place.geometry.lng, place.geometry.lat])
            .setPopup(new mapboxgl.Popup().setHTML(`<strong>${place.formatted}</strong>`))
            .addTo(map);
    });
}