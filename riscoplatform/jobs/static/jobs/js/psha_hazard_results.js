 "use strict";

(function($) {
$( document ).ready(function() {
    
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
    var job_id = url[url.length -2];

    var cells;
    var hazard_data;
    var hazard_options;
    var hazardLayer;
    var job;

    var clicked_cells = [];

    $.ajax( BASE_URL+'/jobs/psha/hazard/results_maps/'+job_id )
    .done(function(data) {

        cells = data.geojson;
        hazard_data = data.hazard;
        job = data.job[0].fields;
        hazard_options = get_hazard_options(cells);

        hazard_options.onEachRecord = function(layer, record){
            layer.on('click', function () {

                if ( $.inArray(record.id, clicked_cells) == -1 ){
                    get_curves(record.id);
                }
                clicked_cells.push(record.id);
            });
        }

        if (job.status == 'FINISHED'){

            for (var i = 0; i<hazard_data.length; i++){

                hazardLayer = new L.ChoroplethDataLayer(hazard_data[i], hazard_options);

                if (i == 0){
                    hazardLayer.addTo(map);
                }

                if (hazard_data[i].quantile != null){
                    var layerName = hazard_data[i].imt+', '+hazard_data[i].quantile+' Quantile, PoE: '+hazard_data[i].poe 
                }
                else {
                    var layerName = hazard_data[i].imt+', Mean results, PoE: '+hazard_data[i].poe 
                }

                control.addOverlay(hazardLayer ,layerName);
                map.fitBounds(hazardLayer.getBounds());

            }
        }

    });

    var curve_markers = L.featureGroup();

    curve_markers.addTo(map);
    control.addOverlay(curve_markers, 'Point Curves');

    var hazard_curves_chart_opts = {legendTemplate: "<ul class=\"<%=name.toLowerCase()%>-legend\"><%for(var i=0;i<datasets.length;i++){%><li><span class=\"<%=name.toLowerCase()%>-legend-marker\" style=\"background-color:<%=datasets[i].strokeColor%>\"></span><%=datasets[i].label%></li><%}%></ul>"}

    var get_curves = function(cell){

        $.ajax(BASE_URL+ '/jobs/psha/hazard/results_curves/'+job_id+'?cell='+cell )
        .done(function(data) {

            var new_markers = L.featureGroup();

            for (var i = 0; i < data.points.length; i++){
 
                var chart_data = {}; 

                for (var j = 0; j< data.points[i].curves.length; j++){

                    var imt = data.points[i].curves[j].fields.imt;

                    if (imt == 'SA'){
                        imt = 'SA('+data.points[i].curves[j].fields.sa_period+')'; 
                    }

                    if (chart_data[imt] == undefined ){
                        chart_data[imt] = [];
                    }

                    var new_dataset =     {
                        data: []
                    }

                    if (data.points[i].curves[j].fields.statistics == 'mean'){
                        new_dataset.label  = 'Mean';
                        new_dataset.strokeColor = '#f00';
                        new_dataset.pointColor = '#f00';
                        new_dataset.pointStrokeColor = '#f00';
                    }
                    else if (data.points[i].curves[j].fields.statistics == 'quantile'){
                        new_dataset.label = data.points[i].curves[j].fields.quantile+' Quantile';
                        new_dataset.strokeColor = '#ff0';
                        new_dataset.pointColor = '#ff0';
                        new_dataset.pointStrokeColor = '#ff0';
                    }
                    else {
                        new_dataset.label  = 'Realization. SM LT branches: '+data.points[i].curves[j].fields.sm_lt_path+'GMPE LT branches: '+data.points[i].curves[j].fields.gsim_lt_path;
                        new_dataset.strokeColor = '#9C9C9C';
                        new_dataset.pointColor = '#9C9C9C';
                        new_dataset.pointStrokeColor = '#9C9C9C';
                    }
                                    

                    var imls = data.points[i].curves[j].fields.imls.replace("[", "").replace("]", "").split(',');
                    var poes = data.points[i].curves[j].fields.poes.replace("[", "").replace("]", "").split(',');
                    
                    for (var k=0; k<imls.length; k++ ){
                        new_dataset.data.push( { x: imls[k], y: poes[k] } );
                    }

                    chart_data[imt].push(new_dataset);

                }

                var charts_html = '';
                for (var imt in chart_data){
                    var imt_id = imt.replace("(", "").replace(")", "").replace(".", "")
                    charts_html+='<div><h4>'+imt+'</h4><canvas id="'+imt_id+'_chart" width="500" height="200"></canvas></div>'
                }

                var marker = L.marker([ data.points[i].lat, data.points[i].lon ], {icon: blueIcon});
                marker.bindPopup('<b>Latitude:</b> '+data.points[i].lat+'<br> <b>Longitude:</b> '+data.points[i].lon + charts_html);


                marker.on('click', function(){

                    for (var imt in chart_data) {
                        var imt_id = imt.replace("(", "").replace(")", "").replace(".", "")
                        var ctx = $("#"+imt_id+"_chart").get(0).getContext("2d");
                        var chart = new Chart(ctx).Scatter(chart_data[imt], hazard_curves_chart_opts);
                    }

                    curve_markers.eachLayer(function (layer){
                        layer.setIcon( blueIcon );
                    });

                    this.setIcon( redIcon );
                });

                new_markers.addLayer(marker);
                curve_markers.addLayer(marker);
            }

            map.fitBounds(new_markers.getBounds());

        });

    }




});
})($); 