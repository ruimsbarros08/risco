 "use strict";

(function($) {
$( document ).ready(function() {

    var map = new L.Map('map');
    map.setView(new L.LatLng(40, -8),5);
    osm.addTo(map);


    //add standard controls
    //L.control.coordinates().addTo(map);
    //add configured controls
    L.control.coordinates({
        position:"bottomleft",
        decimals:2,
        decimalSeperator:",",
        labelTemplateLat:"Latitude: {y}",
        labelTemplateLng:"Longitude: {x}"
    }).addTo(map);


    L.control.layers(baseMaps).addTo(map);

    var getContentPopup = function(feature) {
        return '<h5>'+feature.id+' - '+feature.properties.name+'</h5>'
    }

    $.ajax(BASE_URL+'/models/rupture/ajax' )
    .done(function(data) {

        var pointSourceLayer = L.geoJson(data.pointSource, {
            //style: style,
            onEachFeature: function (feature, layer) {
                layer.on('click', function () {
                    var popupContent = getContentPopup(feature);
                    layer.bindPopup(popupContent).openPopup();
                });
            }
        }).addTo(map);


        var faultSourceLayer = L.geoJson(data.faultSource, {
            //style: style,
            onEachFeature: function (feature, layer) {
                layer.on('click', function () {
                    var popupContent = getContentPopup(feature);
                    layer.bindPopup(popupContent).openPopup();
                });
            }
        }).addTo(map);


        map.fitBounds([pointSourceLayer.getBounds() ,faultSourceLayer.getBounds()]);

    });


    // Initialise the FeatureGroup to store editable layers
    var drawnItems = new L.FeatureGroup();
    map.addLayer(drawnItems);


    
    var polylineOptions = {
                allowIntersection: false,
                shapeOptions: {
                    color: '#f00',
                    weight: 3
                }
            };
    

    // Initialise the draw control and pass it the FeatureGroup of editable layers
    var drawControl = new L.Control.Draw({
        edit: {
            featureGroup: drawnItems,
            //edit: false,
            //remove: false
        },
        draw: {
            polyline: polylineOptions,
            polygon: false,
            rectangle: false,
            circle: false,
            //marker: false
        }
    });
    map.addControl(drawControl);


    map.on('draw:created', function (e) {
        var type = e.layerType,
            layer = e.layer;
        
        if (type == 'marker'){
            $('.leaflet-draw-draw-marker').hide();
            $("#id_location").attr('value', toWKT(layer));
        }
        if (type == 'polyline'){
            $('.leaflet-draw-draw-polyline').hide();
            $("#id_rupture_geom").attr('value', toWKT(layer));
        }
        

        drawnItems.addLayer(layer);
    });


    map.on('draw:edited', function (e) {
        var layers = e.layers;
        layers.eachLayer(function (layer) {
            
            if (layer instanceof L.Marker){
                $("#id_location").attr('value', toWKT(layer));  
            }
            if (layer instanceof L.Polyline){
                $("#id_rupture_geom").attr('value', toWKT(layer));
            }
        });
    });

    map.on('draw:deleted', function (e) {
        var layers = e.layers;
        layers.eachLayer(function (layer) {
            if (layer instanceof L.Marker){
                $('.leaflet-draw-draw-marker').show();
                $("#id_location").attr('value', '');
            }
            if (layer instanceof L.Polyline){
                $('.leaflet-draw-draw-polyline').show();
                $("#id_rupture_geom").attr('value', '');
            }
            
        });
    });


    $( "label[for='location']" ).hide();
    $( "label[for='rupture_geom']" ).hide();

    $( "label[for='xml']" ).hide();
    $( "#id_xml" ).hide();
    
    $('#id_input_type').on('change', function() {
        if (this.value == 'CUSTOM_RUPTURE'){
            $( "label[for='rupture_type']" ).show( "fast");
            $( "#id_rupture_type" ).show( "fast");
            $( "label[for='rake']" ).show( "fast");
            $( "#id_rake" ).show( "fast");
            $( "label[for='upper_depth']" ).show( "fast");
            $( "#id_upper_depth" ).show( "fast");
            $( "label[for='lower_depth']" ).show( "fast");
            $( "#id_lower_depth" ).show( "fast");
            $( "label[for='dip']" ).show( "fast");
            $( "#id_dip" ).show( "fast");
            $( "label[for='magnitude']" ).show( "fast");
            $( "#id_magnitude" ).show( "fast");
            $( "label[for='depth']" ).show( "fast");
            $( "#id_depth" ).show( "fast");

            $( "label[for='xml']" ).hide( "fast");
            $( "#id_xml" ).hide( "fast");
        }
        else {
            $( "label[for='rupture_type']" ).hide( "fast");
            $( "#id_rupture_type" ).hide( "fast");
            $( "label[for='rake']" ).hide( "fast");
            $( "#id_rake" ).hide( "fast");
            $( "label[for='upper_depth']" ).hide( "fast");
            $( "#id_upper_depth" ).hide( "fast");
            $( "label[for='lower_depth']" ).hide( "fast");
            $( "#id_lower_depth" ).hide( "fast");
            $( "label[for='dip']" ).hide( "fast");
            $( "#id_dip" ).hide( "fast");
            $( "label[for='magnitude']" ).hide( "fast");
            $( "#id_magnitude" ).hide( "fast");
            $( "label[for='depth']" ).hide( "fast");
            $( "#id_depth" ).hide( "fast");

            $( "label[for='xml']" ).show( "fast");
            $( "#id_xml" ).show( "fast");
        }
    });

    //$('.leaflet-draw-draw-marker').hide();
    $('#id_rupture_type').on('change', function() {
        if (this.value == 'POINT'){
            //$('.leaflet-draw-draw-marker').show();
            $('.leaflet-draw-draw-polyline').hide();
            $("#id_rupture_geom").attr('value', '');
            drawnItems.clearLayers();
        }
        else {
            //$('.leaflet-draw-draw-marker').hide();
            $('.leaflet-draw-draw-polyline').show();
            //$("#id_location").attr('value', '');
            drawnItems.clearLayers();
        }
    })


});
})($); 