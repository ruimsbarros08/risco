 "use strict";

(function($) {
$( document ).ready(function() {

    $('label[for="location"]').hide();

    var map = new L.Map('map');
    map.setView(new L.LatLng(0, 0),2);
    osm.addTo(map);
    //var control = L.control.layers(baseMaps).addTo(map);
    var control = L.control.layers();
    control.addTo(map);

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

    /*
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
    */

    var selected_marker;    
    $( "#assets_table tbody" ).on( "click", "tr", function() {
        var index = parseInt($( this ).attr('asset_id'));

        if (selected_marker == undefined){
            selected_marker = markerList[index];
            selected_marker.addTo(map);
        }
        else {
            map.removeLayer(selected_marker);
            selected_marker = markerList[index];
            selected_marker.addTo(map);
        }


    });

    //var page = 1;
    var country = undefined;
    var adm1 = undefined;
    var assets;
    var heat;


    var markers = L.markerClusterGroup();
    var markerList = [];


    var load_assets = function(country, adm1) {
        $.ajax('/models/exposure/'+model_id+'/assets?'+'country='+country+'&adm1='+adm1 )
        .done(function(data) {
            //if (page == 1){assets = [];}
            assets = data.assets;
            append_data(page, assets)
            for(var i=0; i<data.assets.length; i++){

                var marker = L.marker(L.latLng(data.assets[i][0], data.assets[i][1]));
                marker.bindPopup(data.assets[i][3]);
                markerList.push(marker);

                };

            markers.addLayers(markerList);
            map.addLayer(markers);
            control.addBaseLayer(markers, 'Assets');

            heat = L.heatLayer(data.assets, {radius: 10});
            control.addBaseLayer(heat, 'Heatmap');

            map.fitBounds(data.assets);


        });
    };


    get_world();
    load_assets(country, adm1);

    $('#country').on('change', function(){
        page = 0;
        country = $(this).val();
        load_assets(country, adm1);

    });

    $('#level1').on('change', function(){
        page = 0;
        adm1 = $(this).val();
        load_assets(country, adm1);

    });


    var page = 0;
    var append_data = function(page, assets){
        for (var i=page*50; i<page*50+50; i++){
            if (i<assets.length){
                $('#assets_table tbody').append("<tr asset_id="+i+"> \
                    <td id='location'><img src='/static/img/marker.png' alt='marker' height='20px;' width='20px;'></td> \
                    <td>"+  assets[i][3] + "</td> \
                    <td>"+  assets[i][4] + "</td> \
                    <td>"+  assets[i][5] + "</td> \
                    <td>"+  assets[i][6] + "</td> \
                    </tr>");
            }
        }
    }

    $('#assets_table_container').bind('scroll',function (e){
        var elem = $(e.currentTarget);
        if (elem[0].scrollHeight * 0.90 < elem.outerHeight() + elem.scrollTop()) {
            page += 1;
            append_data(page, assets);

        }

    });




});
})($);