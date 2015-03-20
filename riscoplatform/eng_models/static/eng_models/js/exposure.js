 "use strict";

(function($) {
$( document ).ready(function() {

    $('label[for="location"]').hide();

    var map = new L.Map('map');
    map.setView(new L.LatLng(40, -8),5);
    osm.addTo(map);
    var control = L.control.layers(baseMaps).addTo(map);

    // Initialize the FeatureGroup to store editable layers
    var drawnItems = new L.FeatureGroup();
    map.addLayer(drawnItems);
    
    // Initialize the draw control and pass it the FeatureGroup of editable layers
    var drawControl = new L.Control.Draw({
        edit: {
            featureGroup: drawnItems,
        },
        draw: {
            polyline: false,
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
        
        $('.leaflet-draw-draw-marker').hide();
        $("#id_location").attr('value', toWKT(layer));
        drawnItems.addLayer(layer);
    });


    map.on('draw:edited', function (e) {
        var layers = e.layers;
        layers.eachLayer(function (layer) {
            $("#id_location").attr('value', toWKT(layer));  
        });
    });

    map.on('draw:deleted', function (e) {
        var layers = e.layers;
        layers.eachLayer(function (layer) {
            $('.leaflet-draw-draw-marker').show();
            $("#id_location").attr('value', '');            
        });
    });


    var url = document.URL.split('/');
    var model_id = url[url.length -2];

    var marker;
    var showOnMap = function(index){
        var asset = assets[0][index]; 
        var location = asset.fields.location;
        var latlng = wktToLatLng(location)
        if (marker == undefined){
            marker = L.marker(latlng).addTo(map);
        }
        else {
            marker.setLatLng(latlng);
        }
        marker.bindPopup("<h3>"+  asset.fields.name + "</h3> \
                    <ul> \
                        <li><b>Taxonomy: </b>"+  asset.fields.taxonomy + "</li> \
                        <li><b>Buildings: </b>"+  asset.fields.n_buildings + "</li> \
                        <li><b>Area: </b>"+  asset.fields.area + "</li> \
                        <li><b>Structural cost: </b>"+  asset.fields.struct_cost + "</li> \
                        <li><b>Structural deductible value: </b>"+  asset.fields.struct_deductible + "</li> \
                        <li><b>Structural insurance limit: </b>"+  asset.fields.struct_insurance_limit + "</li> \
                        <li><b>Structural retrofitting cost: </b>"+  asset.fields.retrofitting_cost + "</li> \
                        <li><b>Non-structural cost: </b>"+  asset.fields.non_struct_cost + "</li> \
                        <li><b>Non-structural deductible value: </b>"+  asset.fields.non_struct_deductible + "</li> \
                        <li><b>Non-structural insurance limit: </b>"+  asset.fields.non_struct_insurance_limit + "</li> \
                        <li><b>Contents cost: </b>"+  asset.fields.contents_cost + "</li> \
                        <li><b>Contents deductible: </b>"+  asset.fields.contents_deductible + "</li> \
                        <li><b>Contents insurance limit: </b>"+  asset.fields.contents_insurance_limit + "</li> \
                        <li><b>Business interruption cost: </b>"+  asset.fields.business_int_cost + "</li> \
                        <li><b>Business interruption deductible: </b>"+  asset.fields.business_int_deductible + "</li> \
                        <li><b>Business interruption insurance limit: </b>"+  asset.fields.business_int_insurance_limit + "</li> \
                        <li><b>Occupation (day): </b>"+  asset.fields.oc_day + "</li> \
                        <li><b>Occupation (night): </b>"+  asset.fields.oc_night + "</li> \
                        <li><b>Occupation (transit): </b>"+  asset.fields.oc_transit + "</li> \
                    </ul>").openPopup(); 
    }

    
    $( "#assets_table tbody" ).on( "click", "tr", function() {
        var index = parseInt($( this ).attr('asset_id'));
        showOnMap(index);
    });


    var page = 1;
    var assets = []
    var load_assets = function(page) {
        $.ajax( BASE_URL+'models/exposure/'+model_id+'/assets?page='+page )
        .done(function(data) {
            if (page == 1){assets = [];}
            for(var i=0; i<data.length; i++){
                $('#assets_table tbody').append("<tr asset_id="+assets.length+i+"> \
                    <td><a href='#'>"+  data[i].fields.name + "</a></td> \
                    <td><a href='#'>"+  data[i].fields.taxonomy + "</a></td> \
                    <td>"+  data[i].fields.n_buildings + "</td> \
                    <td>"+  data[i].fields.area + "</td> \
                    <td>"+  data[i].fields.struct_cost + "</td> \
                    </tr>");
            };
            assets.push(data);
            page += 1;
        });
    };

    var heat;
    var load_heat_layer = function() {

        $.ajax( BASE_URL+'models/exposure/'+model_id+'/heat_assets' )
        .done(function(data) {
            heat = L.heatLayer(data, {radius: 10}).addTo(map);
            control.addOverlay(heat, 'Assets heatmap');
            map.fitBounds(data);
        });
    }

    var load_countries = function() {
        $.ajax( BASE_URL+'countries')
        .done(function(data){
            for (var i = 0; i<data.length; i++){
                $("#country").append('<option value='+data[i][0]+'>'+data[i][1]+'</option>');
            }
        });
    }

    $("#level1").remoteChained({
        parents : "#country",
        url : "/level1"
    });

    $("#level2").remoteChained({
        parents : "#level1",
        url : "/level2"
    });

    $("#level3").remoteChained({
        parents : "#level2",
        url : "/level3"
    });

    load_assets(page);
    load_heat_layer();
    load_countries();


    $('#assets_table_container').infinitescroll({
        behavior: 'local',
        binder: $('#assets_table_container'), // scroll on this element rather than on the window
        dataType: 'json',
        appendCallback: false
    }, function(json, opts){
        console.log('hey');
        // Get current page
        var page = opts.state.currPage;
        // Do something with JSON data, create DOM elements, etc ..
    });



});
})($);