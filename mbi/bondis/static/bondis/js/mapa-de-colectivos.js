var map;
var div_map = document.getElementById('map');
var bondis = []

function initMap() {
    map = new google.maps.Map(div_map, 
                                {center: 
                                {lat: -31.256834, lng: -64.299055},
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
        show_side_bondis();
    });
}

function show_side_bondis() {
    // mostrar la lista de los colectivos
    $('#options').empty();
    
    $.each(bondis.features, function(i, bondi){
        let b = bondi.properties;
        let res = 'En <b>' + b.falta_minutos + ' minutos </b>';
        res += ' llega ' + b.opcion_espera.origen.empresa.nombre;
        res += '<div class="extra_bondi">'+b.info+'</div>';
        $('#options').append('<div data-bondi_id="' + bondi.id + '" class="bondi">' + res + '</div>');
        if (i > 5) {
            return false;
        }
      });
    
    $('.bondi').on('click', function(){
        // extender info y centrar en el mapa
        $('.extra_bondi').hide();
        $(this).children('.extra_bondi').toggle();
        
        let bondi_id = $(this).data('bondi_id');
        map.data.forEach(function (feature) {
            if (feature.getId() == bondi_id) {
                if (feature.getGeometry()) {
                map.setCenter(feature.getGeometry().get());
                map.setZoom(16);
                }
            else {
                map.setZoom(12);
                alert('No tiene GPS activado');
                }
            }
        });
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
