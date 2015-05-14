 "use strict";

(function($) {
$( document ).ready(function() {

    //hide-show    
    $( "label[for='region']" ).hide( "fast");

    var map = new L.Map('map');
    map.setView(new L.LatLng(0, 0),2);
    bw.addTo(map);

    var control = L.control.layers(baseLayers).addTo(map);

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