var map;
var markers = [];

function initMap() {
    var location = getLocation();
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 14,
        center: location,
        mapTypeId: 'terrain'
    }); 
    addMarker(location, map);;
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

function getLocation() {
    var latitud = document.getElementById("latitud").value;
    var longitud = document.getElementById("longitud").value;
    var location = {lat: parseFloat(latitud), lng: parseFloat(longitud)};
    return location
}









