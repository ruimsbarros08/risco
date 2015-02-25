 "use strict";

(function($) {
$( document ).ready(function() {

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
    $('#id_point').unwrap();
    $('#id_area').unwrap();
    $('#id_fault').unwrap();

    //dividers
    $('<hr>').insertAfter('#id_rake');

    //hide-show    
    $( "label[for='id_bin_width']" ).hide( "fast");
    $( "#id_bin_width" ).parent().hide( "fast");
    $( "label[for='id_occur_rates']" ).hide( "fast");
    $( "#id_occur_rates" ).parent().hide( "fast");
    $('#id_mag_freq_dist_type').on('change', function() {
        if (this.value == 'TRUNC'){
            $( "label[for='id_bin_width']" ).hide( "fast");
            $( "#id_bin_width" ).parent().hide( "fast");
            $( "label[for='id_occur_rates']" ).hide( "fast");
            $( "#id_occur_rates" ).parent().hide( "fast");

            $( "label[for='id_a']" ).show( "fast");
            $( "#id_a" ).parent().show( "fast");
            $( "label[for='id_b']" ).show( "fast");
            $( "#id_b" ).parent().show( "fast");
            $( "label[for='id_max_mag']" ).show( "fast");
            $( "#id_max_mag" ).parent().show( "fast");
        }
        else {
            $( "label[for='id_bin_width']" ).show( "fast");
            $( "#id_bin_width" ).parent().show( "fast");
            $( "label[for='id_occur_rates']" ).show( "fast");
            $( "#id_occur_rates" ).parent().show( "fast");

            $( "label[for='id_a']" ).hide( "fast");
            $( "#id_a" ).parent().hide( "fast");
            $( "label[for='id_b']" ).hide( "fast");
            $( "#id_b" ).parent().hide( "fast");
            $( "label[for='id_max_mag']" ).hide( "fast");
            $( "#id_max_mag" ).parent().hide( "fast");

        }
    });


    //hide-show    
    $( "label[for='id_dip']" ).hide( "fast");
    $( "#id_dip" ).parent().hide( "fast");
    $( "label[for='id_rake']" ).hide( "fast");
    $( "#id_rake" ).parent().hide( "fast");

    $('#id_source_type').on('change', function() {
        if (this.value == 'SIMPLE_FAULT'){
            $( "label[for='id_nodal_plane_dist']" ).hide( "fast");
            $( "#id_nodal_plane_dist" ).parent().hide( "fast");
            $( "label[for='id_hypo_depth_dist']" ).hide( "fast");
            $( "#id_hypo_depth_dist" ).parent().hide( "fast");

            $( "label[for='id_dip']" ).show( "fast");
            $( "#id_dip" ).parent().show( "fast");
            $( "label[for='id_rake']" ).show( "fast");
            $( "#id_rake" ).parent().show( "fast");

            $('.leaflet-draw-draw-marker').hide();
            $('.leaflet-draw-draw-polyline').show();
            $('.leaflet-draw-draw-polygon').hide();

        }
        else {
            $( "label[for='id_dip']" ).hide( "fast");
            $( "#id_dip" ).parent().hide( "fast");
            $( "label[for='id_rake']" ).hide( "fast");
            $( "#id_rake" ).parent().hide( "fast");

            $( "label[for='id_nodal_plane_dist']" ).show( "fast");
            $( "#id_nodal_plane_dist" ).parent().show( "fast");
            $( "label[for='id_hypo_depth_dist']" ).show( "fast");
            $( "#id_hypo_depth_dist" ).parent().show( "fast");

            if (this.value == 'POINT'){
                $('.leaflet-draw-draw-marker').show();
                $('.leaflet-draw-draw-polyline').hide();
                $('.leaflet-draw-draw-polygon').hide();
            }
            else {
                $('.leaflet-draw-draw-marker').hide();
                $('.leaflet-draw-draw-polyline').hide();
                $('.leaflet-draw-draw-polygon').show();
            }


        }
    });



	var map = new L.Map('map');
	var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
	var osmAttrib='Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
	var osm = new L.TileLayer(osmUrl, {minZoom: 3, maxZoom: 16, attribution: osmAttrib});

	map.setView(new L.LatLng(40, -8),5);
	map.addLayer(osm);


    var url = document.URL.split('/');
    var model_id = url[url.length -2];

    
    $.ajax( BASE_URL+'models/sources/'+model_id+'/ajax' )
    .done(function(data) {

    var pointSourceLayer = L.geoJson(data.pointSource, {
        //style: style,
        onEachFeature: function (feature, layer) {
            //layer.setStyle({"fillColor": feature.properties.color});
            layer.on('click', function () {
                //info.update(layer.feature.properties);
                //layer.setStyle(hoverStyle);
                var popupContent = '<b>ID</b>: '+feature.id+'<br><b>Name</b>: '+feature.properties.name;
                layer.bindPopup(popupContent).openPopup();
            });
        }
    }).addTo(map);


    var areaSourceLayer = L.geoJson(data.areaSource, {
        //style: style,
        onEachFeature: function (feature, layer) {
            //layer.setStyle({"fillColor": feature.properties.color});
            layer.on('click', function () {
                //info.update(layer.feature.properties);
                //layer.setStyle(hoverStyle);
                var popupContent = '<b>ID</b>: '+feature.id+'<br><b>Name</b>: '+feature.properties.name;
                layer.bindPopup(popupContent).openPopup();

            });
        }
    }).addTo(map);


    var faultSourceLayer = L.geoJson(data.faultSource, {
        //style: style,
        onEachFeature: function (feature, layer) {
            //layer.setStyle({"fillColor": feature.properties.color});
            layer.on('click', function () {
                //info.update(layer.feature.properties);
                //layer.setStyle(hoverStyle);
                var popupContent = '<b>ID</b>: '+feature.id+'<br><b>Name</b>: '+feature.properties.name;
                layer.bindPopup(popupContent).openPopup();
            });
        }
    }).addTo(map);


    //map.fitBounds(areaSourceLayer.getBounds());

    })
    .fail(function() {
        alert( "error" );
    })
    .always(function() {
        //alert( "complete" );
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
            //polygon: false,
            rectangle: false,
            circle: false,
            //marker: false
        }
    });
    map.addControl(drawControl);

    $('.leaflet-draw-draw-polyline').hide();
    $('.leaflet-draw-draw-polygon').hide();
    map.on('draw:created', function (e) {
        var type = e.layerType,
            layer = e.layer;
        if (type == 'marker'){
            $('.leaflet-draw-draw-marker').hide();
            $("#id_point").attr('value', toWKT(layer));
        }
        if (type == 'polyline'){
            $('.leaflet-draw-draw-polyline').hide();
            $("#id_fault").attr('value', toWKT(layer));
        }
        if (type == 'polygon'){
            $('.leaflet-draw-draw-polygon').hide();
            $("#id_area").attr('value', toWKT(layer));
        }

        drawnItems.addLayer(layer);
    });


    map.on('draw:edited', function (e) {
        var layers = e.layers;
        layers.eachLayer(function (layer) {
            if (layer instanceof L.Marker){
                $("#id_point").attr('value', toWKT(layer));
            }
            if (layer instanceof L.Polyline){
                $("#id_fault").attr('value', toWKT(layer));
            }
            if (layer instanceof L.Polygon){
                $("#id_area").attr('value', toWKT(layer));
            }
        });
    });

    map.on('draw:deleted', function (e) {
        var layers = e.layers;
        layers.eachLayer(function (layer) {
            if (layer instanceof L.Marker){
                if ($('#id_source_type').val() == 'POINT'){
                    $('.leaflet-draw-draw-marker').show();
                }
                $("#id_point").attr('value', '');
            }
            if (layer instanceof L.Polyline){
                if ($('#id_source_type').val() == 'SIMPLE_FAULT'){
                    $('.leaflet-draw-draw-polyline').show();
                }
                $("#id_fault").attr('value', '');
            }
            if (layer instanceof L.Polygon){
                if ($('#id_source_type').val() == 'AREA'){
                    $('.leaflet-draw-draw-polygon').show();
                }
                $("#id_area").attr('value', '');
            }
        });
    });



});
})($);