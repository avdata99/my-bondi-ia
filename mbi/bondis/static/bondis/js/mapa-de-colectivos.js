var map;
var div_map = document.getElementById('map');
var bondis = []

function initMap() {
    map = new google.maps.Map(div_map, 
                                {center: {lat: -31.256834, lng: -64.299055},
                                 gestureHandling: 'greedy',
                                 zoom: 12,
                                 mapTypeId: google.maps.MapTypeId.TERRAIN  // ROADMAP HYBRID
                                });
    var styleControl = document.getElementById('style-selector-control');
    map.controls[google.maps.ControlPosition.LEFT_BOTTOM].push(styleControl);

    load_bondis();

}

function load_bondis() {
    clean_map();
    let url = '/bondis/resultados/?espera=1';
    let xhr = $.getJSON(url);
    xhr.done(function(){
        bondis = xhr.responseJSON.results;
        map.data.addGeoJson(bondis);
        style_bondis();
        show_side_bondis();
        map.data.addListener('click', function(event) {clickBondi(event);});
    });
}

function clickBondi(event) {
    // click en alguno de mis puntos en el mapa.
    let feature = event.feature;
    
    $('.bondi').removeClass('selected');
    let $side = $('[data-bondi_id="' + feature.getId() + '"]')
    $side.addClass('selected');
    $('.extra_bondi').hide();
    $side.children('.extra_bondi').show();

    }

function show_side_bondis() {
    // mostrar la lista de los colectivos
    $('#options').empty();
    
    $.each(bondis.features, function(i, bondi){
        let b = bondi.properties;
        let res = b.opcion_espera.origen.empresa.nombre_corto + ' en <b>' + b.falta_minutos + ' minutos </b>';
        
        res += '<div class="extra_bondi">'+b.info+'</div>';
        $('#options').append('<div data-bondi_id="' + bondi.id + '" class="bondi">' + res + '</div>');
        if (i > 5) {
            return false;
        }
      });
    
    $('.bondi').on('click', function(){
        // extender info y centrar en el mapa
        $('.bondi').removeClass('selected');
        $('.extra_bondi').hide();
        $(this).children('.extra_bondi').show();
        $(this).addClass('selected');
        
        let bondi_id = $(this).data('bondi_id');
        map.data.forEach(function (feature) {
            if (feature.getId() == bondi_id) {
                if (feature.getGeometry()) {
                map.setCenter(feature.getGeometry().get());
                map.setZoom(15);
                }
            else {
                map.setZoom(12);
                // alert('No tiene GPS activado');
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

function style_bondis() {
    map.data.setStyle(function(feature) {  // https://developers.google.com/maps/documentation/javascript/reference/#Data.StyleOptions
      
        let sizeX=25;
        let sizeY=25;
        
        let opcion = feature.getProperty('opcion_espera');
        let empresa_color = (opcion.origen.empresa.color)? opcion.origen.empresa.color: '000000';
        var bondi = {
            path: 'M41.162 25h-32.02c-.933 0-1.701-.802-1.701-1.714 0-.152.028-.324.059-.462l1.704-11.899c.145-.773.841-.925 1.674-.925h28.553c.827 0 1.529.139 1.672.909l1.704 12.116c.026.141.06.224.06.376-.001.912-.773 1.599-1.705 1.599zm-1.281 13.345c-1.803 0-3.265-1.419-3.265-3.188 0-1.757 1.462-3.174 3.265-3.174 1.791 0 3.256 1.417 3.256 3.174 0 1.769-1.465 3.188-3.256 3.188zm-29.501 0c-1.79 0-3.253-1.419-3.253-3.188 0-1.757 1.463-3.174 3.253-3.174 1.808 0 3.268 1.417 3.268 3.174 0 1.769-1.46 3.188-3.268 3.188zm5.62-35.345h20v3h-20c-2 0-2-3 0-3zm28.202 4.59c-.584-2.813-2.29-3.946-5.073-5.078-2.778-1.128-9.216-2.48-14.058-2.48-4.863 0-11.334 1.353-14.115 2.48-2.782 1.133-4.46 2.265-5.039 5.078l-1.917 15.659v21.751h3v2c0 4 5 4 5 0v-2h25v2c0 4 6 4 6 0v-2h3v-21.751l-1.798-15.659z',
            fillColor: '#' + empresa_color,
            fillOpacity: 0.6,
            scale: 0.8,
            strokeColor: '#' + empresa_color,
            strokeWeight: 3
        };

        return {icon: bondi};
        
    
      });
}

$( document ).ready(function() {
    setInterval("load_bondis()", 30000);
    });
