var labels = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
var labelIndex = 0;
var coordenadas_poligono = [];
var poligono;
var map;
var markers = [];

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 13,
        center: {lat: -2.169366, lng: -79.919217},
        mapTypeId: 'terrain'
    }); 

    crearPoligonoInicial();

    google.maps.event.addListener(map, 'click', function(event) {
        //AGREGANDO COORDENADA A LISTA
        coordenadas_poligono.push({lat: event.latLng.lat(), lng: event.latLng.lng()})
        crearPoligono();
        anadirPosicionEnHtml(event.latLng.lat(), event.latLng.lng());
        addMarker(event.latLng, map);
    });
}

function crearPoligonoInicial() {
    var posiciones = document.getElementsByClassName("position_sample_obj");
    for (var i = 1; i < posiciones.length; i++) {
        var coordenada = posiciones[i].value.split("|");
        var location = {lat: parseFloat(coordenada[0]), lng: parseFloat(coordenada[1])}
        coordenadas_poligono.push(location); 
        addMarker(location, map);   
    }
    crearPoligono();
}

function crearPoligono() {
    //BORRANDO PREVIO POLIGONO
    if (poligono) {
        poligono.setMap(null);
    }

    //COSTRUYENDO POLIGONO
    poligono = new google.maps.Polygon({
        paths: coordenadas_poligono,
        strokeColor: '#FF0000',
        strokeOpacity: 0.8,
        strokeWeight: 2,
        fillColor: '#FF0000',
        fillOpacity: 0.35
    });
    poligono.setMap(map);
}

// Adds a marker to the map.
function addMarker(location, map) {
    var marker = new google.maps.Marker({
        position: location,
        label: labels[labelIndex++ % labels.length],
        map: map
    });
    markers.push(marker);
}

function setMapOnAll(map) {
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(map);
    }
}

function undo() {
    //REMOVIENDO ELEMENTO EN HTML
    var form = document.getElementById("guardarForm");
    var coordenada = document.getElementsByClassName("position_sample_obj");
    form.removeChild(coordenada[coordenada.length - 1]);

    //DECREMENTANDO UN INDEX DEL MARCADOR BORRADO
    labelIndex--;

    //QUITANDO TODOS LOS MARCADORES
    setMapOnAll(null);

    //BORRANDO ULTIMA COORDENADA DE POLIGONO Y MARCADOR
    coordenadas_poligono.pop();
    markers.pop();

    //CREANDO NUEVAMENTE UN POLIGONO Y MARCADORES
    setMapOnAll(map);
    crearPoligono();
}

function anadirPosicionEnHtml(lat, lng){
    var input = document.getElementsByClassName("position_sample_obj")[0];
    var nuevo_input = input.cloneNode(true);
    nuevo_input.value = (lat + "|" + lng);
    document.getElementById("guardarForm").appendChild(nuevo_input);
}



