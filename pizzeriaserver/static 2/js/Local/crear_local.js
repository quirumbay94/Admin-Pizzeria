var map;
var markers = [];

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 12,
        center: {lat: -2.169366, lng: -79.919217},
        mapTypeId: 'terrain'
    }); 

    google.maps.event.addListener(map, 'click', function(event) {
        //AGREGANDO COORDENADA
        anadirPosicionEnHtml(event.latLng.lat(), event.latLng.lng());
        addMarker(event.latLng, map);
    });

    cargarMarcador();
}

// Adds a marker to the map.
function addMarker(location, map) {
    setMapOnAll(null);
    var marker = new google.maps.Marker({
        position: location,
        label: "*",
        map: map
    });
    if (markers.length > 0) {
        markers[0] = marker;
    } else {
        markers.push(marker);
    }
    setMapOnAll(map);
}

function setMapOnAll(map) {
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(map);
    }
}

function anadirPosicionEnHtml(lat, lng){
    var input = document.getElementById("coordenada");
    input.value = (lat + "|" + lng);
}

function cargarMarcador() {
    var latitud = document.getElementById("latitud").value;
    var longitud = document.getElementById("longitud").value;
    var location = {lat: parseFloat(latitud), lng: parseFloat(longitud)};
    addMarker(location, map);
}












