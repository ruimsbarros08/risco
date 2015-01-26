 "use strict";

(function($) {
$( document ).ready(function() {


    var map = new L.Map('map');
    var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
    var osmAttrib='Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
    var osm = new L.TileLayer(osmUrl, {minZoom: 3, maxZoom: 16, attribution: osmAttrib});

    map.setView(new L.LatLng(40, -8),5);
    map.addLayer(osm);



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


    $('label').addClass('control-labels col-lg-2');
    $('input').addClass('form-control');
    $('select').addClass('form-control');
    $('textarea').addClass('form-control');
    $('input').wrap('<div class="col-lg-10"></div>');
    $('select').wrap('<div class="col-lg-10"></div>');
    $('textarea').wrap('<div class="col-lg-10"></div>');
    $('<div class="form-group">').insertBefore('label');
    $('</div>').insertAfter('</input>');
    $('</div>').insertAfter('</textarea>');
    $('</div>').insertAfter('</select>');
    
    $('input[name="csrfmiddlewaretoken"]').unwrap();
    $('#id_location').unwrap();
    $('#id_rupture_geom').unwrap();

    //dividers
    $('<hr>').insertAfter('#id_xml');

    $( "label[for='id_xml']" ).hide( "fast");
    $( "#id_xml" ).hide( "fast");
    $('#id_input_type').on('change', function() {
        if (this.value == 'CUSTOM_RUPTURE'){
            $( "label[for='id_rupture_type']" ).show( "fast");
            $( "#id_rupture_type" ).show( "fast");
            $( "label[for='id_rake']" ).show( "fast");
            $( "#id_rake" ).show( "fast");
            $( "label[for='id_upper_depth']" ).show( "fast");
            $( "#id_upper_depth" ).show( "fast");
            $( "label[for='id_lower_depth']" ).show( "fast");
            $( "#id_lower_depth" ).show( "fast");
            $( "label[for='id_dip']" ).show( "fast");
            $( "#id_dip" ).show( "fast");
            $( "label[for='id_magnitude']" ).show( "fast");
            $( "#id_magnitude" ).show( "fast");
            $( "label[for='id_depth']" ).show( "fast");
            $( "#id_depth" ).show( "fast");

            $( "label[for='id_xml']" ).hide( "fast");
            $( "#id_xml" ).hide( "fast");
        }
        else {
            $( "label[for='id_rupture_type']" ).hide( "fast");
            $( "#id_rupture_type" ).hide( "fast");
            $( "label[for='id_rake']" ).hide( "fast");
            $( "#id_rake" ).hide( "fast");
            $( "label[for='id_upper_depth']" ).hide( "fast");
            $( "#id_upper_depth" ).hide( "fast");
            $( "label[for='id_lower_depth']" ).hide( "fast");
            $( "#id_lower_depth" ).hide( "fast");
            $( "label[for='id_dip']" ).hide( "fast");
            $( "#id_dip" ).hide( "fast");
            $( "label[for='id_magnitude']" ).hide( "fast");
            $( "#id_magnitude" ).hide( "fast");
            $( "label[for='id_depth']" ).hide( "fast");
            $( "#id_depth" ).hide( "fast");

            $( "label[for='id_xml']" ).show( "fast");
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