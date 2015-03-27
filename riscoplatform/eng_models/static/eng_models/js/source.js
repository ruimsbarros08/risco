 "use strict";

(function($) {
$( document ).ready(function() {


    $('label[for="point"]').hide();
    $('label[for="area"]').hide();
    $('label[for="fault"]').hide();

    //hide-show    
    $( "label[for='bin_width']" ).hide();
    $( "#id_bin_width" ).hide();
    $( "label[for='occur_rates']" ).hide();
    $( "#id_occur_rates" ).hide();
    $('#id_mag_freq_dist_type').on('change', function() {
        if (this.value == 'TRUNC'){
            $( "label[for='bin_width']" ).hide( "fast");
            $( "#id_bin_width" ).hide( "fast");
            $( "label[for='occur_rates']" ).hide( "fast");
            $( "#id_occur_rates" ).hide( "fast");

            $( "label[for='a']" ).show( "fast");
            $( "#id_a" ).show( "fast");
            $( "label[for='b']" ).show( "fast");
            $( "#id_b" ).show( "fast");
            $( "label[for='max_mag']" ).show( "fast");
            $( "#id_max_mag" ).show( "fast");
        }
        else {
            $( "label[for='bin_width']" ).show( "fast");
            $( "#id_bin_width" ).show( "fast");
            $( "label[for='occur_rates']" ).show( "fast");
            $( "#id_occur_rates" ).show( "fast");

            $( "label[for='a']" ).hide( "fast");
            $( "#id_a" ).hide( "fast");
            $( "label[for='b']" ).hide( "fast");
            $( "#id_b" ).hide( "fast");
            $( "label[for='max_mag']" ).hide( "fast");
            $( "#id_max_mag" ).hide( "fast");

        }
    });


    //hide-show    
    $( "label[for='dip']" ).hide();
    $( "#id_dip" ).hide();
    $( "label[for='rake']" ).hide();
    $( "#id_rake" ).hide();

    $('#id_source_type').on('change', function() {
        if (this.value == 'SIMPLE_FAULT'){
            $( "label[for='nodal_plane_dist']" ).hide( "fast");
            $( "#id_nodal_plane_dist" ).hide( "fast");
            $( "label[for='hypo_depth_dist']" ).hide( "fast");
            $( "#id_hypo_depth_dist" ).hide( "fast");

            $( "label[for='dip']" ).show( "fast");
            $( "#id_dip" ).show( "fast");
            $( "label[for='rake']" ).show( "fast");
            $( "#id_rake" ).show( "fast");

            $('.leaflet-draw-draw-marker').hide();
            $('.leaflet-draw-draw-polyline').show();
            $('.leaflet-draw-draw-polygon').hide();

        }
        else {
            $( "label[for='dip']" ).hide( "fast");
            $( "#id_dip" ).hide( "fast");
            $( "label[for='rake']" ).hide( "fast");
            $( "#id_rake" ).hide( "fast");

            $( "label[for='nodal_plane_dist']" ).show( "fast");
            $( "#id_nodal_plane_dist" ).show( "fast");
            $( "label[for='hypo_depth_dist']" ).show( "fast");
            $( "#id_hypo_depth_dist" ).show( "fast");

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
    map.setView(new L.LatLng(40, -8),5);
    osm.addTo(map);
    var control = L.control.layers(baseMaps).addTo(map);

    var url = document.URL.split('/');
    var model_id = url[url.length -2];

    var getContentPopup = function(feature) {
        return '<h5>'+feature.id+' - '+feature.properties.name+'</h5>'
                /*<ul> \
                <li>Tectonic region:'+feature.properties.tectonic_region+'</li> \
                <li>Magnitude scale relation:'+feature.properties.mag_scale_rel+'</li> \
                <li>Rupture Aspect Ratio:'+feature.properties.rupt_aspect_ratio+'</li> \
                <li>Magnitude frequency distribution:'+feature.properties.mag_freq_dist_type+'</li> \
                </ul>*/
    }
    
    $.ajax('/models/sources/'+model_id+'/ajax' )
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
        control.addOverlay(pointSourceLayer, 'Point Sources');


        var areaSourceLayer = L.geoJson(data.areaSource, {
            //style: style,
            onEachFeature: function (feature, layer) {
                layer.on('click', function () {
                    var popupContent = getContentPopup(feature);
                    layer.bindPopup(popupContent).openPopup();

                });
            }
        }).addTo(map);
        control.addOverlay(areaSourceLayer, 'Area Sources');


        var faultSourceLayer = L.geoJson(data.faultSource, {
            //style: style,
            onEachFeature: function (feature, layer) {
                layer.on('click', function () {
                    var popupContent = getContentPopup(feature);
                    layer.bindPopup(popupContent).openPopup();
                });
            }
        }).addTo(map);
        control.addOverlay(faultSourceLayer, 'Fault Sources');

        map.fitBounds([areaSourceLayer.getBounds(), faultSourceLayer.getBounds(), pointSourceLayer.getBounds()]);

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