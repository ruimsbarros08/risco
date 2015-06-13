 "use strict";

(function($) {
$( document ).ready(function() {


    $('label[for="point"]').hide();
    $('label[for="area"]').hide();
    $('label[for="fault"]').hide();
    $('label[for="occur_rates"]').hide();
    $('label[for="nodal_plane_dist"]').hide();
    $('label[for="hypo_depth_dist"]').hide();

    if ( $('#id_mag_freq_dist_type').val() == 'TRUNC' ){   
        $( "#id_bin_width" ).attr('disabled', true);
        $( "#occur_rates-tags input" ).attr('disabled', true);
    }

    $('#id_mag_freq_dist_type').on('change', function() {
        if (this.value == 'TRUNC'){
            $( "#id_bin_width" ).attr('disabled', true);
            $( "#occur_rates-tags input" ).attr('disabled', true);

            $( "#id_a" ).attr('disabled', false);
            $( "#id_b" ).attr('disabled', false);
            $( "#id_max_mag" ).attr('disabled', false);
        }
        else {
            $( "#id_bin_width" ).attr('disabled', false);
            $( "#occur_rates-tags input" ).attr('disabled', false);

            $( "#id_a" ).attr('disabled', true);
            $( "#id_b" ).attr('disabled', true);
            $( "#id_max_mag" ).attr('disabled', true);

        }
    });


    if ( $('#id_source_type').val() != 'SIMPLE_FAULT' ){
        $( "#id_dip" ).attr('disabled', true);
        $( "#id_rake" ).attr('disabled', true);
    }


    $('#id_source_type').on('change', function() {
        if (this.value == 'SIMPLE_FAULT'){
            $( "#probability_nodal_plane_dist" ).attr('disabled', true);
            $( "#strike" ).attr('disabled', true);
            $( "#dip" ).attr('disabled', true);
            $( "#rake" ).attr('disabled', true);
            $( "#add-prob" ).attr('disabled', true);
            
            $( "#probability_hypo_depth_dist" ).attr('disabled', true);
            $( "#depth" ).attr('disabled', true);
            $( "#add-prob-hypo-depth" ).attr('disabled', true);

            $( "#id_dip" ).attr('disabled', false);
            $( "#id_rake" ).attr('disabled', false);

            $('.leaflet-draw-draw-marker').hide();
            $('.leaflet-draw-draw-polyline').show();
            $('.leaflet-draw-draw-polygon').hide();

        }
        else {
            $( "#id_dip" ).attr('disabled', true);
            $( "#id_rake" ).attr('disabled', true);

            $( "#probability_nodal_plane_dist" ).attr('disabled', false);
            $( "#strike" ).attr('disabled', false);
            $( "#dip" ).attr('disabled', false);
            $( "#rake" ).attr('disabled', false);
            $( "#add-prob" ).attr('disabled', false);

            $( "#probability_hypo_depth_dist" ).attr('disabled', false);
            $( "#depth" ).attr('disabled', false);
            $( "#add-prob-hypo-depth" ).attr('disabled', false);

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


    //OCCUR RATES

    var rates = []

    var occur_rates_tags = $('#occur_rates-tags').tags({
        bootstrapVersion: 3,
        tagSize: 'lg',
        readOnly: false,
        popovers: false,
        promptText: 'Insert a float [0, 1] and press enter',
        popoverTrigger: 'hover',
        tagClass: 'btn-primary',
        //beforeAddingTag: function(tag){ console.log(tag); },
        afterAddingTag: function(tag){
            rates.push(tag);
            $('#id_occur_rates').val( JSON.stringify(rates) );
        },
        //beforeDeletingTag: function(tag){ remove_imt(tag); },
        afterDeletingTag: function(tag){
            var position = rates.indexOf(tag);
            rates.splice(position, 1);
            $('#id_occur_rates').val( JSON.stringify(rates) );
        },
        //definePopover: function(tag){
        //    return imt_l[tag].join(", ");
        //},
        excludes: function(tag){
            if ( isFloat(parseFloat(tag)) ){
                return false
            }
            else {
                return true
            }
        }
    });



    //NODAL PLANE DISTRIBUTION
    var prob_sum = 0;
    $('#add-prob').on('click', function(){
        var prob    = parseFloat($('#probability_nodal_plane_dist').val());
        var strike  = parseFloat($('#strike').val());
        var dip     = parseFloat($('#dip').val());
        var rake    = parseFloat($('#rake').val());

        if (isNaN(prob) || isNaN(strike) || isNaN(dip) ||isNaN(rake) ){
            alert('Please insert valid data');
            return;
        }

        if (prob > 1){
            alert('The probability value must be a value between 0 and 1');
            return;
        }

        if ( (prob_sum + prob) > 1){
            alert('The sum of the probabilities must be equal to 1');
            return;
        }
        prob_sum += prob;

        nodal_plane_dist_data.push([prob, strike, dip, rake]);

        $('#id_nodal_plane_dist').val( JSON.stringify(nodal_plane_dist_data) );

        add_nodal_plane_dist_row(prob, strike, dip, rake)

    });


    var add_nodal_plane_dist_row = function(prob, strike, dip, rake){

        var $new_tr = $("<tr>\
                    <td>"+prob+"</td>\
                    <td>"+strike+"º</td>\
                    <td>"+dip+"º</td>\
                    <td>"+rake+"º</td>\
                    <td><button class='btn btn-danger btn-sm' type='button'> <span class='glyphicon glyphicon-remove' aria-hidden='true'></span> </button></td>\
                </tr>");

        $new_tr.hide().prependTo($("#nodal_plane_dist_table tbody")).fadeIn(400);
        
        $new_tr.on('click', 'td:last button', function (){

            prob_sum -= prob;

            var position = nodal_plane_dist_data.length-1 - $(this).parent().parent().index();

            nodal_plane_dist_data.splice(position ,1);
            $('#id_nodal_plane_dist').val( JSON.stringify(nodal_plane_dist_data) );

            var $tr = $(this).closest('tr');
            $tr.fadeOut(400, function(){
                this.remove();
            });
        });
    }

    if ($('#id_nodal_plane_dist').val()){
        var nodal_plane_dist_data = JSON.parse($('#id_nodal_plane_dist').val());
        for (var i = 0; i<nodal_plane_dist_data.length; i++ ){
            add_nodal_plane_dist_row( nodal_plane_dist_data[i][0], nodal_plane_dist_data[i][1], nodal_plane_dist_data[i][2], nodal_plane_dist_data[i][3] );
        }
    }
    else{
        var nodal_plane_dist_data = [];
    }


    //HYPO DEPTH DISTRIBUTION
    var depth_prob_sum = 0;
    $('#add-prob-hypo-depth').on('click', function(){
        var prob    = parseFloat($('#probability_hypo_depth_dist').val());
        var depth    = parseFloat($('#depth').val());

        if (isNaN(prob) || isNaN(depth) ){
            alert('Please insert valid data');
            return;
        }

        if (prob > 1){
            alert('The probability value must be a value between 0 and 1');
            return;
        }

        if ( (depth_prob_sum + prob) > 1){
            alert('The sum of the probabilities must be equal to 1');
            return;
        }
        depth_prob_sum += prob;

        hypo_depth_dist_data.push([prob, depth]);

        $('#id_hypo_depth_dist').val( JSON.stringify(hypo_depth_dist_data) );

        add_hypo_depth_dist_row(prob, depth)

    });


    var add_hypo_depth_dist_row = function(prob, depth){

        var $new_tr = $("<tr>\
                    <td>"+prob+"</td>\
                    <td>"+depth+" km</td>\
                    <td><button class='btn btn-danger btn-sm' type='button'> <span class='glyphicon glyphicon-remove' aria-hidden='true'></span> </button></td>\
                </tr>");

        $new_tr.hide().prependTo($("#hypo_depth_dist_table tbody")).fadeIn(400);
        
        $new_tr.on('click', 'td:last button', function (){

            depth_prob_sum -= prob;

            var position = hypo_depth_dist_data.length-1 - $(this).parent().parent().index();

            hypo_depth_dist_data.splice(position ,1);
            $('#id_hypo_depth_dist').val( JSON.stringify(hypo_depth_dist_data) );

            var $tr = $(this).closest('tr');
            $tr.fadeOut(400, function(){
                this.remove();
            });
        });
    }

    if ($('#id_hypo_depth_dist').val()){
        var hypo_depth_dist_data = JSON.parse($('#id_hypo_depth_dist').val());
        for (var i = 0; i<hypo_depth_dist_data.length; i++ ){
            add_hypo_depth_dist_row( hypo_depth_dist_data[i][0], hypo_depth_dist_data[i][1] );
        }
    }
    else{
        var hypo_depth_dist_data = [];
    }



    var map = new L.Map('map', {
        fullscreenControl: true,
        fullscreenControlOptions: {
            position: 'topleft'
        }
    });
    map.setView(new L.LatLng(0, 0),2);
    bw.addTo(map);

    var control = L.control.layers(baseLayers).addTo(map);

    var url = document.URL.split('/');
    var model_id = url[url.length -2];

    var getContentPopup = function(feature) {

        if (feature.properties.source_type != 'SIMPLE_FAULT'){
            
            var nodal_plane_dist_rows = [];
            for (var i = 0; i < feature.properties.nodal_plane_dist.length; i++){
                var new_row = '<tr>'+
                                    '<td>'+feature.properties.nodal_plane_dist[i][0]+'</td>'+
                                    '<td>'+feature.properties.nodal_plane_dist[i][1]+'º</td>'+
                                    '<td>'+feature.properties.nodal_plane_dist[i][2]+'º</td>'+
                                    '<td>'+feature.properties.nodal_plane_dist[i][3]+'º</td>'+
                                '</tr>' 
                nodal_plane_dist_rows.push(new_row);
            }

            nodal_plane_dist_rows = nodal_plane_dist_rows.join();

            var hypo_depth_dist_rows = [];
            for (var i = 0; i < feature.properties.hypo_depth_dist.length; i++){
                var new_row = '<tr>'+
                                    '<td>'+feature.properties.hypo_depth_dist[i][0]+'</td>'+
                                    '<td>'+feature.properties.hypo_depth_dist[i][1]+' km</td>'+
                                '</tr>'
                hypo_depth_dist_rows.push(new_row);
            }

            hypo_depth_dist_rows = hypo_depth_dist_rows.join();
        }



        return '<h5>ID: '+feature.id+' - '+feature.properties.name+'</h5>'+
                '<ul>'+
                    '<li><b>Tectonic region:</b> '+feature.properties.tectonic_region+'</li>'+
                    '<li><b>Magnitude scale relation:</b> '+
                    ( feature.properties.mag_scale_rel == 'WC1994' ? 'Wells and Coopersmith 1994' : 'Thomas et al. 2012 (PEER)')+
                    '</li>'+
                    '<li><b>Rupture Aspect Ratio:</b> '+feature.properties.rupt_aspect_ratio+'</li>'+
                    ( feature.properties.mag_freq_dist_type == 'TRUNC' ? '<li><b>Magnitude frequency distribution:</b> Truncated Guttenberg Richer </li>'+
                                                                            '<li><b>a:</b> '+feature.properties.a+' </li>'+
                                                                            '<li><b>b:</b> '+feature.properties.b+' </li>'+
                                                                            '<li><b>Min magnitude:</b> '+feature.properties.min_mag+' </li>'+
                                                                            '<li><b>Max magnitude:</b> '+feature.properties.max_mag+' </li>'
                    : '<li><b>Magnitude frequency distribution:</b> Truncated Guttenberg Richer </li>'+
                                                                                '<li><b>Min magnitude:</b> '+feature.properties.min_mag+' </li>'+
                                                                                '<li><b>Bin width:</b> '+feature.properties.bin_width+' </li>'+
                                                                                '<li><b>Occur rates:</b> '+feature.properties.occur_rates+' </li>')+
                     '<li><b>Upper depth:</b> '+feature.properties.upper_depth+' km</li>'+
                     '<li><b>Lower depth:</b> '+feature.properties.lower_depth+' km</li>'+
                    ( feature.properties.source_type != 'SIMPLE_FAULT' ? '<li><b>Nodal plane distribution:</b> '+'<table class="table table-hover table-striped">'+
                                                                                                                    '<thead>'+
                                                                                                                        '<tr>'+
                                                                                                                            '<th>Probability</th>'+
                                                                                                                            '<th>Strike</th>'+
                                                                                                                            '<th>Dip</th>'+
                                                                                                                            '<th>Rake</th>'+
                                                                                                                        '</tr>'+
                                                                                                                    '</thead>'+
                                                                                                                    '<tbody>'+nodal_plane_dist_rows+
                                                                                                                    '</tbody>'+
                                                                                                                '</table>'+' </li>'+
                                                                            '<li><b>Hypo depth distribution:</b> '+'<table class="table table-hover table-striped">'+
                                                                                                                    '<thead>'+
                                                                                                                        '<tr>'+
                                                                                                                            '<th>Probability</th>'+
                                                                                                                            '<th>Depth</th>'+
                                                                                                                        '</tr>'+
                                                                                                                    '</thead>'+
                                                                                                                    '<tbody>'+hypo_depth_dist_rows+
                                                                                                                    '</tbody>'+
                                                                                                                '</table>'+' </li>'
                    : '<li><b>Dip:</b> '+feature.properties.dip+'º </li>'+
                        '<li><b>Rake:</b> '+feature.properties.rake+'º </li>')+
                '</ul>'
    }
    
    $.ajax('/models/sources/'+model_id+'/ajax' )
    .done(function(data) {

        var bounds = [];

        if (data.pointSource.features.length != 0){

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

            bounds.push(pointSourceLayer.getBounds());
        
        }

        if (data.areaSource.features.length != 0){

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

            bounds.push(areaSourceLayer.getBounds());


        }

        if (data.faultSource.features.length != 0){

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

            bounds.push(faultSourceLayer.getBounds());

        }

        if (bounds.length != 0){
            map.fitBounds(bounds);
        }

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