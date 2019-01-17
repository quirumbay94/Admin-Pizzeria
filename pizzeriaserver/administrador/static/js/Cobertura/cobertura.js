var labels = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
var labelIndex = 0;
var poligonos = [];
var poligonos_objs = [];
var map;
var markers = [];

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 12,
        center: {lat: -2.169366, lng: -79.919217},
        mapTypeId: 'terrain'
    }); 

    google.maps.event.addListener(map, 'click', function(event) {
        //AGREGANDO COORDENADA A LISTA
        coordenadas_poligono.push({lat: event.latLng.lat(), lng: event.latLng.lng()})
        crearPoligono();
        anadirPosicionEnHtml(event.latLng.lat(), event.latLng.lng());
        addMarker(event.latLng, map);
    });

    makeRequest("http://127.0.0.1:8000/menu/cobertura/get_poligonos");
}

function crearPoligonoInicial(posiciones) {
    posiciones.forEach(function(element) {
        var color = element["COLOR"]
        var coordenadas = element["COORDENADAS"]
        var coordenadas_poligono = [];
        coordenadas.forEach(function(coordenada) {
            var location = {lat: parseFloat(coordenada[0]), lng: parseFloat(coordenada[1])}
            coordenadas_poligono.push(location);
        });
        poligonos.push({
            "COLOR" : color,
            "COORDENADAS" : coordenadas_poligono
        })

    });
    crearPoligono();
}

function crearPoligono() {
    //BORRANDO PREVIO POLIGONO
    if (poligonos_objs.length > 0) {
        poligonos_objs.forEach(function(element) {
            element.setMap(null);
        });
    }

    console.log(poligonos_objs.length);

    //COSTRUYENDO POLIGONOS
    poligonos.forEach(function(element) {
        poligono = new google.maps.Polygon({
            paths: element["COORDENADAS"],
            strokeColor: element["COLOR"],
            strokeOpacity: 0.8,
            strokeWeight: 2,
            fillColor: element["COLOR"],
            fillOpacity: 0.35
        });
        poligono.setMap(map);
        poligonos_objs.push(poligono);
    });

    console.log(poligonos_objs);
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

function makeRequest(url) {

        http_request = false;

        if (window.XMLHttpRequest) { // Mozilla, Safari,...
            http_request = new XMLHttpRequest();
            if (http_request.overrideMimeType) {
                http_request.overrideMimeType('text/xml');
                // Ver nota sobre esta linea al final
            }
        } else if (window.ActiveXObject) { // IE
            try {
                http_request = new ActiveXObject("Msxml2.XMLHTTP");
            } catch (e) {
                try {
                    http_request = new ActiveXObject("Microsoft.XMLHTTP");
                } catch (e) {}
            }
        }

        if (!http_request) {
            alert('Falla :( No es posible crear una instancia XMLHTTP');
            return false;
        }
        http_request.onreadystatechange = alertContents;
        http_request.open('GET', url, true);
        http_request.send();

    }

    function alertContents() {

        if (http_request.readyState == 4) {
            if (http_request.status == 200) {
                var obj = JSON.parse(http_request.responseText);
                crearPoligonoInicial(obj["RESPONSE"]);

            } else {
                alert('Hubo problemas con la petición.');
            }
        }

    }

