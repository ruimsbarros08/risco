 "use strict";

(function($) {
$( document ).ready(function() {

    $('label[for="location"]').hide();

    var map = new L.Map('map', {
        fullscreenControl: true,
        fullscreenControlOptions: {
            position: 'topleft'
        }
    });
    map.setView(new L.LatLng(0, 0),2);
    bw.addTo(map);

    var control = L.control.layers(baseLayers).addTo(map);

    var regions_control = new RegionSelectControl().addTo(map);

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


    var asset_categories = [];
    var cost_asset_series = [];

    var show_asset_details = function(index){

        asset_categories = [];
        cost_asset_series = [];
        //deductible_asset_series = [];
        //insurance_limit_asset_series = [];
        var a = assets[index];

        $('#asset_info').empty();

        $('#asset_info').append("<table id='asset_details' class='table table-striped table-hover'> \
                        <caption>"+a[3]+"</caption> \
                            <thead> \
                                <tr> \
                                  <th>Type</th> \
                                  <th>Cost</th> \
                                  <th>Deductible</th> \
                                  <th>Insurance Limit</th> \
                                  <th>Retrofitted <span class='glyphicon glyphicon-wrench' aria-hidden='true'></span></th> \
                                </tr> \
                            </thead> \
                            <tbody> \
                            </tbody> \
                        </table>");
    

            if (a[7] != null){
                asset_categories.push('Structural');
                cost_asset_series.push(a[7]);

                //if (a[8] != null){
                //    deductible_asset_series.push(a[7]*a[8]);
                //}

                $('#asset_details tbody').append("<tr> \
                    <td>Structural</td> \
                    <td>"+a[7]+"</td> \
                    <td>"+a[8]*100+"%</td> \
                    <td>"+a[9]*100+"%</td> \
                    <td>"+a[10]+"</td> \
                    </tr>");
            }

            if (a[11] != null){
                asset_categories.push('Nonstructural');
                cost_asset_series.push(a[11]);
                $('#asset_details tbody').append("<tr> \
                    <td>Nonstructural</td> \
                    <td>"+a[11]+"</td> \
                    <td>"+a[12]*100+"%</td> \
                    <td>"+a[13]*100+"%</td> \
                    <td></td> \
                    </tr>");
            }

            if (a[14] != null){
                asset_categories.push('Contents');
                cost_asset_series.push(a[14]);
                $('#asset_details tbody').append("<tr> \
                    <td>Contents</td> \
                    <td>"+a[14]+"</td> \
                    <td>"+a[15]*100+"%</td> \
                    <td>"+a[16]*100+"%</td> \
                    <td></td> \
                    </tr>");
            }

            if (a[17] != null){
                asset_categories.push('Business Interruption');
                cost_asset_series.push(a[17]);
                $('#asset_details tbody').append("<tr> \
                    <td>Business Interruption</td> \
                    <td>"+a[17]+"</td> \
                    <td>"+a[18]*100+"%</td> \
                    <td>"+a[19]*100+"%</td> \
                    <td></td> \
                    </tr>");
            }


        $('#asset_info').append('<div id="asset_chart"></div>')

        show_asset_chart();

        if (a[20] != null || a[21] != null || a[22] != null ){


        $('#asset_info').append("<table id='occupancies_table' class='table table-striped table-hover'> \
                        <caption>Occupancies</caption> \
                            <thead> \
                                <tr> \
                                  <th>Period <span class='glyphicon glyphicon-time' aria-hidden='true'></span></th> \
                                  <th>Occupancy <span class='glyphicon glyphicon-user' aria-hidden='true'></span></th> \
                                </tr> \
                            </thead> \
                            <tbody> \
                            </tbody> \
                        </table>");

                if (a[20] != null){
                    $('#occupancies_table tbody').append("<tr> \
                        <td>Day</td> \
                        <td>"+a[20]+"</td> \
                        </tr>");
                }
                if (a[21] != null){
                    $('#occupancies_table tbody').append("<tr> \
                        <td>Night</td> \
                        <td>"+a[21]+"</td> \
                        </tr>");
                }
                if (a[22] != null){
                    $('#occupancies_table tbody').append("<tr> \
                        <td>Day</td> \
                        <td>"+a[22]+"</td> \
                        </tr>");
                }

            }

    }


    var show_asset_chart = function(){

        return new Highcharts.Chart({
            chart: {
                type: 'bar',
                renderTo: 'asset_chart',
            },
            title: {
                text: 'Asset costs'
            },
            xAxis: {
                categories: asset_categories
            },
            yAxis: {
                min: 0,
                title: {
                    text: 'Costs'
                }
            },
            legend: {
                reversed: true
            },
            plotOptions: {
                series: {
                    stacking: 'normal'
                }
            },
            series: [{
                name: 'Cost',
                data: cost_asset_series
            }]
        });

    }



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

        show_asset_details(index);

    });

    //var page = 1;
    var country = undefined;
    var adm1 = undefined;
    var assets;
    var heat;


    //var markers = L.markerClusterGroup();
    var markers = undefined;
    var markerList = [];


    var load_assets = function(country, adm1) {
        $.ajax('/models/exposure/'+model_id+'/assets?'+'country='+country+'&adm1='+adm1 )
        .done(function(data) {

            if (markers != undefined) {
                map.removeLayer(markers);
                map.removeLayer(heat);
            }

            markerList = [];
            markers = new L.markerClusterGroup();

            //markers = L.markerClusterGroup();
            //markerList = [];
            assets = data.assets;
            append_data(page, assets);
            for(var i=0; i<data.assets.length; i++){

                var marker = L.marker(L.latLng(data.assets[i][0], data.assets[i][1]));
                marker.bindPopup(data.assets[i][3]);
                markerList.push(marker);

                };

            markers.addLayers(markerList);
            map.addLayer(markers);
            control.addOverlay(markers, 'Assets');

            heat = new L.heatLayer(data.assets, {radius: 10});
            control.addOverlay(heat, 'Heatmap');

            map.fitBounds(data.assets);

        });
    };


    //get_world();
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
        $('#assets_table tbody').empty();

        if (assets.length>0){
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
        else {
            $('#assets_table tbody').append('<p>No assets for this region</p>');

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