var map;
var div_map = document.getElementById('map');
var bondis = []

function initMap() {
    map = new google.maps.Map(div_map, 
                                {center: 
                                {lat: -31.4177131, lng: -64.1956264},
                                zoom: 12,
                                mapTypeId: google.maps.MapTypeId.TERRAIN  // ROADMAP HYBRID
                                });
    var styleControl = document.getElementById('style-selector-control');
    map.controls[google.maps.ControlPosition.LEFT_BOTTOM].push(styleControl);

    load_bondis();

}

function load_bondis() {
    clean_map();
    let url = 'http://localhost:8000/bondis/resultados/?espera=1';
    let xhr = $.getJSON(url);
    xhr.done(function(){
        bondis = xhr.responseJSON.results;
        map.data.addGeoJson(bondis);
    });
}

function clean_map() {
    map.data.forEach(function (feature) {
        map.data.remove(feature);
    });
}

$( document ).ready(function() {
    setInterval("load_bondis()", 30000);
    });
