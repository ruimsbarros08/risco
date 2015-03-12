 "use strict";

(function($) {
$( document ).ready(function() {

    $('label[for="location"]').hide('fast');

    var map = new L.Map('map');
    map.setView(new L.LatLng(40, -8),5);
    osm.addTo(map);
    L.control.layers(baseMaps).addTo(map);

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
                        <li><b>Structural Cost: </b>"+  asset.fields.struct_cost + "</li> \
                    </ul>").openPopup(); 
    }

    
    $( "#assets_table tbody" ).on( "click", "tr", function() {
        var index = parseInt($( this ).attr('asset_id'));
        showOnMap(index);
    });


    var url = document.URL.split('/');
    var model_id = url[url.length -2];
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
                    <td>"+  data[i].fields.struct_cost + "</td></tr>")

            assets.push(data);
            page += 1;
        });
    }


    var heat;
    var load_heat_layer = function() {

        $.ajax( BASE_URL+'models/exposure/'+model_id+'/heat_assets' )
        .done(function(data) {
            heat = L.heatLayer(data, {radius: 10}).addTo(map);
            map.fitBounds(data);
        });
    }


    load_assets(page);
    load_heat_layer();

});
})($);