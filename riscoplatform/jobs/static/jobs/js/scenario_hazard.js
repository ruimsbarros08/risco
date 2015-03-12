 "use strict";

(function($) {
$( document ).ready(function() {

    //hide-show    
    $( "label[for='region']" ).hide( "fast");
    $( "label[for='site_model']" ).hide( "fast");


    $( "label[for='site_model']" ).hide( "fast");
    $( "#id_site_model" ).hide( "fast");
    $('#id_sites_type').on('change', function() {
        if (this.value == 'VARIABLE_CONDITIONS'){
            $( "label[for='vs30']" ).hide( "fast", 'swing');
            $( "#id_vs30" ).hide( "fast", 'swing');
            $( "label[for='vs30type']" ).hide( "fast", 'swing');
            $( "#id_vs30type" ).hide( "fast", 'swing');
            $( "label[for='z1pt0']" ).hide( "fast", 'swing');
            $( "#id_z1pt0" ).hide( "fast", 'swing');
            $( "label[for='z2pt5']" ).hide( "fast", 'swing');
            $( "#id_z2pt5" ).hide( "fast", 'swing');

            $( "label[for='site_model']" ).show( "fast", 'swing');
            $( "#id_site_model" ).show( "fast", 'swing');
        }
        else {
            $( "label[for='vs30']" ).show( "fast", 'swing');
            $( "#id_vs30" ).show( "fast", 'swing');
            $( "label[for='vs30type']" ).show( "fast", 'swing');
            $( "#id_vs30type" ).show( "fast", 'swing');
            $( "label[for='z1pt0']" ).show( "fast", 'swing');
            $( "#id_z1pt0" ).show( "fast", 'swing');
            $( "label[for='z2pt5']" ).show( "fast", 'swing');
            $( "#id_z2pt5" ).show( "fast", 'swing');

            $( "label[for='site_model']" ).hide( "fast", 'swing');
            $( "#id_site_model" ).hide( "fast", 'swing');

        }
    });


    $('#id_correlation_model').change( function() {
        if ($(this).is(":checked")){
            $( "label[for='vs30_clustering']" ).show( "fast");
            $( "#id_vs30_clustering" ).show( "fast");
        }
        else {
            $( "label[for='vs30_clustering']" ).hide( "fast");
            $( "#id_vs30_clustering" ).hide( "fast");
        }
    });


    var map = new L.Map('map');
    map.setView(new L.LatLng(40, -8),5);
    osm.addTo(map);
    L.control.layers(baseMaps).addTo(map);

    // Initialize the FeatureGroup to store editable layers
    var drawnItems = new L.FeatureGroup();
    map.addLayer(drawnItems);


    var polygonOptions = {
                showArea: true,
            };

    // Initialise the draw control and pass it the FeatureGroup of editable layers
    var drawControl = new L.Control.Draw({
        edit: {
            featureGroup: drawnItems,
            //edit: false,
            //remove: false
        },
        draw: {
            polyline: false,
            polygon: polygonOptions,
            rectangle: false,
            circle: false,
            marker: false
        }
    });
    map.addControl(drawControl);


    map.on('draw:created', function (e) {
        var type = e.layerType,
            layer = e.layer;

        if (type == 'polygon'){
            $('.leaflet-draw-draw-polygon').hide();
            $("#id_region").attr('value', toWKT(layer));
        }

        drawnItems.addLayer(layer);
    });


    map.on('draw:edited', function (e) {
        var layers = e.layers;
        layers.eachLayer(function (layer) {

            if (layer instanceof L.Polygon){
                $("#id_region").attr('value', toWKT(layer));
            }
        });
    });

    map.on('draw:deleted', function (e) {
        var layers = e.layers;
        layers.eachLayer(function (layer) {

            if (layer instanceof L.Polygon){
                $('.leaflet-draw-draw-polygon').show();
                $("#id_region").attr('value', '');
            }
        });
    });




});
})($); 