 "use strict";

(function($) {
$( document ).ready(function() {


    $( "#vulnerability-selector li:first-child" ).addClass( "active" );
    $( "#myTabContent div:first-child" ).addClass( "tab-pane fade active in" );
    
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


    var level = 0;
    var country;
    var taxonomy;
    var taxonomies;

    $('#adm_back').attr("disabled", true);


    var zoom_out_adm = function(){
        //country = undefined;
        level -= 1;
        if (level == 0){
            country = undefined;
        }
        else if (level == 1){
            country = $('#country').val();
        }
        else if (level == 2){
            country = $('#level1').val();
        }

        get_data(country, level);   
    }

    $('#adm_back').on('click', zoom_out_adm);

    $('#country').on('change', function(){
        if ( $(this).val() == 'undefined'){
            zoom_out_adm();
            return;
        }
        else {
            level = 1;
        }
        country = $(this).val();
        get_data(country, level);
    });

    $('#level1').on('change', function(){
        if ( $(this).val() == 'undefined'){
            zoom_out_adm();
            return;
        }
        else {
            level = 2;
        }
        country = $(this).val();
        get_data(country, level);
    });

    $('#taxonomy').on('change', function(){
        taxonomy = $(this).val();
        get_data(country, level);
    });


    var url = document.URL.split('/');
    var job_id = url[url.length -2];
    var regions;
    var job;
    var exposure_model;
    var losses_data;
    var lossesLayer;
    var losses_options;

    var chart_data = [];
    var insured_chart_data = [];
    var tax_chart_data = [];

    var chart_options = {
        //Number - The percentage of the chart that we cut out of the middle
        percentageInnerCutout : 50, // This is 0 for Pie charts
        //Number - Amount of animation steps
        animationSteps : 100,
        //String - Animation easing effect
        animationEasing : "easeOutBounce",
        //Boolean - Whether we animate the rotation of the Doughnut
        animateRotate : true,
    };


    var lossesGroup = new L.LayerGroup();

    var clean_losses_layers = function(lossesGroup){
        lossesGroup.eachLayer(function (layer) {
            map.removeLayer(layer);
            control.removeLayer(layer);
        });
    }

    var get_data = function(country, next_level){
        level = next_level;
        var adm_1;
        var adm_0;
        if (level == 1){
            adm_0 = country;
        }
        else if (level == 2){
            adm_1 = country;
        }
        $.ajax( '/jobs/psha/risk/results_maps/'+job_id+'/?adm_1='+adm_1+'&country='+adm_0+'&taxonomy='+taxonomy )
        .done(function(data) {
            display_data(data)
        });
    }

    var get_locations = function(country){
        $.ajax( '/jobs/psha/risk/results_locations/'+job_id+'/?country='+country+'&taxonomy='+taxonomy)
        .done(function(data) {
            display_locations(data);
        });
    }

    var get_curves = function(country, lat, lon){
        $.ajax( '/jobs/psha/risk/results_curves/'+job_id+'/?country='+country+'&lat='+lat+'&lon='+lon)
        .done(function(data) {
            display_curves(data);
        });
    }

    $('#level1').attr("disabled", true);
    $('#level2').attr("disabled", true);
    var fill_regions_dropdowns = function(regions){
        if (level == 0){
            var $elem = $("#country");
            $("#level1").empty();
            $("#level2").empty();
            $('#level2').attr("disabled", true);
            $('#level1').attr("disabled", true);
        }
        else if (level == 1){
            $("#country").val(country);
            var $elem = $("#level1");
            $("#level2").empty();
            $('#level1').attr("disabled", false);
            $('#level2').attr("disabled", true);
        }
        else if (level == 2){
            $("#level1").val(country);
            var $elem = $("#level2");
            $('#level2').attr("disabled", false);
        }
        $elem.empty();
        $elem.append('<option value="undefined">All</option>');
        for (var i = 0; i < regions.features.length; i++){
            $elem.append('<option value='+regions.features[i].properties.id+'>'+regions.features[i].properties.name+'</option>');
        }
    }

    var fill_taxonomy_dropdown = function(taxs){
        taxonomies = [];
        $('#taxonomy').append("<option value='undefined'>All</option>");
        for (var j = 0; j < taxs.length; j++){
            $('#taxonomy').append('<option value='+taxs[j].id+'>'+taxs[j].name+'</option>');    
            taxonomies.push( {id: taxs[j].id, name: taxs[j].name} )
        }
    }

    var clean_charts = function(tab) {

        $('#'+tab+'_insured').html('<div class="panel panel-default"> \
                                      <div class="panel-heading">Insurance data (average):</div> \
                                      <div class="panel-body"> \
                                        <canvas id="'+tab+'_insured_chart" \
                                                    width="200" height="200"></canvas> \
                                      </div> \
                                      <div class="panel-footer" id="'+tab+'_insured_chart_legend"><ul></ul> \
                                    </div>');
        $('#'+tab+'_region').html('<div class="panel panel-default"> \
                                      <div class="panel-heading">Average losses per region:</div> \
                                      <div class="panel-body"> \
                                        <canvas id="'+tab+'_chart" \
                                                    width="200" height="200"></canvas> \
                                      </div> \
                                      <div class="panel-footer" id="'+tab+'_chart_legend"><ul></ul> \
                                    </div>');
        $('#'+tab+'_taxonomy').html('<div class="panel panel-default"> \
                                      <div class="panel-heading">Average losses per taxonomy:</div> \
                                      <div class="panel-body"> \
                                        <canvas id="'+tab+'_tax_chart" \
                                                    width="200" height="200"></canvas></div> \
                                        <div class="panel-footer" id="'+tab+'_tax_chart_legend"><ul></ul> \
                                      </div> \
                                    </div>');
    }

    var enable_back_button = function(){
        if ( level == 0 ){
            $('#adm_back').attr("disabled", true);
        }
        else {
            $('#adm_back').attr("disabled", false);
        }
    }


    var display_chart = function(type, data, units){

        chart_data = [];
        var ctx = $('#'+type+'_chart').get(0).getContext("2d");

        for (var j = 0; j < data.values.length; j++ ){
            var color = getRandomColor();
            $('#'+data.name+'_chart_legend ul').append('<li class="no-bullets"> <span class="glyphicon glyphicon-stop" style="color:'+color+';" aria-hidden="true"></span> <b> '+
                        data.values[j].name+'</b>: '+
                        Humanize.intword(data.values[j].value, 'M', 1)+' +- '+
                        Humanize.intword(data.values[j].stddev, 'M', 1)+' '+
                        units+'</li>');
            chart_data.push({value: data.values[j].value,
                            label: data.values[j].name,
                            color: color,
                            highlight: "#EBD800",});
        }

        var chart = new Chart(ctx).Pie(chart_data, chart_options);
        
        $('#'+type+'_chart').on('click', function(evt){
            try {  
                var selectedLabel = chart.getSegmentsAtEvent(evt)[0].label;
                for (var k = 0; k < regions.features.length; k++){
                    if (selectedLabel == regions.features[k].properties.name){
                        country = regions.features[k].id;
                        $("#country").val(country);
                        level = level+1;
                        get_data(country, level);
                    }
                }
            }
            catch(err){
                console.log('Click on a slice')
            }
        });

    }


    var locationsGroup = new L.LayerGroup();
    control.addOverlay(locationsGroup, 'Locations');

    var display_locations = function(data){
        locationsGroup.clearLayers();

        var locations = data.locations;
        var bounds = [];

        if (job.status == 'FINISHED'){
            
            for (var i = 0; i<locations.length; i++){

                var marker = L.marker(L.latLng(locations[i].lat, locations[i].lon), {icon: blueIcon});
                bounds.push([locations[i].lat, locations[i].lon]);
                marker.bindPopup( '<b>Latitude: </b>'+locations[i].lat + '<br><b>Longitude:</b> '+locations[i].lon + '<br><b>Name:</b> '+locations[i].adm_2 );
                locationsGroup.addLayer(marker);

                marker.on('click', function(){

                    locationsGroup.eachLayer(function (layer){
                        layer.setIcon( blueIcon );
                    });

                    this.setIcon( redIcon );
                });

            }
            locationsGroup.addTo(map);
            map.fitBounds(bounds);

        }

    }





    var display_data = function(data){

        enable_back_button();
        clean_losses_layers(lossesGroup);

        regions = data.geojson;
        fill_regions_dropdowns(regions);

        losses_data = data.losses;
        job = data.job[0].fields;
        exposure_model = data.exposure_model[0].fields;

        if (job.status == 'FINISHED'){

            var $active_tab = $("#myTabContent div.active");
            
            for (var i = 0; i<losses_data.length; i++){

                var $tab_elem = $( "#"+losses_data[i].name );
                $tab_elem.addClass( "tab-pane fade active in" );

                if (taxonomies == undefined){
                    fill_taxonomy_dropdown( losses_data[i].values_per_taxonomy );
                }
                
                clean_charts(losses_data[i].name);

                //UNITS
                if ( losses_data[i].name == 'occupants_vulnerability' ){
                    var units = 'fatalities';
                }
                else {
                    var units = exposure_model.currency;
                }
                chart_options.tooltipTemplate = "<%= label %>: <%= Humanize.intword(value, 'M', 1) %> "+units;

                //MAP DVF OPTIONS
                losses_options = get_losses_options(regions, losses_data[i].max);
                losses_options.onEachRecord = function(layer, record){
                    layer.on('click', function () {
                        country = record.id;
                        var next_level = level+1;
                        if (level != 2){
                            get_data(country, next_level);
                        }
                        else {
                            get_locations(country);
                        }
                    });
                }

                $tab_elem.removeClass( "active in" );

                //ADD LAYERS

                map.on('overlayadd', function (layer){
                    var name_array = layer.name.split(' ');
                    for (var i=0; i<losses_data.length;i++){
                        if (name_array[0] == losses_data[i].name){
                            var poe = parseFloat(name_array[2]);
                            if (name_array.length > 3){
                                var quantile = name_array[4];
                            }

                            for (var j=0; j<losses_data[i].values_per_region.length; j++){
                                if (losses_data[i].values_per_region[j].poe == poe){
                                    if (losses_data[i].values_per_region[j].quantile == quantile){

                                        display_chart(losses_data[i].name, losses_data[i].values_per_region[j], 'EUR');
                                    }
                                }
                            }                                                        
                        }  
                    }
                });

                for (var j=0; j<losses_data[i].values_per_region.length;j++){
                    lossesLayer = new L.ChoroplethDataLayer(losses_data[i].values_per_region[j], losses_options);

                    if (j==0){
                        lossesLayer.addTo(map);
                    }

                    lossesGroup.addLayer(lossesLayer);
                    if (losses_data[i].values_per_region[j].quantile){
                        var layer_name = losses_data[i].name + ' Poe: ' + losses_data[i].values_per_region[j].poe + ' Quantile: ' + losses_data[i].values_per_region[j].quantile 
                    }
                    else {
                        var layer_name = losses_data[i].name + ' Poe: ' + losses_data[i].values_per_region[j].poe + ' Mean'
                    }
                    
                    control.addOverlay(lossesLayer ,layer_name);
                    map.fitBounds(lossesLayer.getBounds());
                    
                }

            }
            $active_tab.addClass('active in');
        }


    }

    get_data(country, level);




});
})($); 