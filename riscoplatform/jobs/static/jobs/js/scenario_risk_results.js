 "use strict";

(function($) {
$( document ).ready(function() {

    $( "#vulnerability-selector li:first-child" ).addClass( "active" );
    $( "#myTabContent div:first-child" ).addClass( "tab-pane fade active in" );
    
    //hide-show    
    $( "label[for='region']" ).hide( "fast");


    var map = new L.Map('map');
    map.setView(new L.LatLng(0, 0),2);
    bw.addTo(map);

    var control = L.control.layers(baseLayers).addTo(map);
    
    var legendControl;
    legendControl = new L.Control.Legend();
    legendControl.addTo(map);


////////////////
//   HAZARD   //
////////////////


    var hazard_url = $('#hazard_id').attr("href").split('/');
    var hazard_job_id = hazard_url[hazard_url.length -2];
    var cells;
    var hazard_data;
    var hazardLayer;
    var hazard_options;

    $.ajax( '/jobs/scenario/hazard/results_ajax_test/'+hazard_job_id )
    .done(function(data) {

        cells = data.geojson;
        hazard_data = data.hazard;
        
        hazard_options = get_hazard_options(cells);

        for (var i = 0; i<hazard_data.length; i++){

            hazardLayer = new L.ChoroplethDataLayer(hazard_data[i], hazard_options);

            control.addOverlay(hazardLayer ,hazard_data[i].name);
            map.fitBounds(hazardLayer.getBounds());

        }

    });


////////////////
//   LOSSES   //
////////////////
    
    var first_time = true;
    var level = 0;
    var country;
    var taxonomy;
    var taxonomies;

    $('#adm_back').attr("disabled", true);

    $('#adm_back').on('click', function(){
        country = undefined;
        level -= 1;
        get_data(country, level);   
    });

    $('#country').on('change', function(){
        if ( $(this).val() == 'undefined'){
            level = 0;
        }
        else {
            level = 1;
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
        tooltipTemplate: "<%= label %>: <%= Humanize.intword(value, 'M', 1) %>",
        //Boolean - Whether we should show a stroke on each segment
        segmentShowStroke : true,
        //String - The colour of each segment stroke
        segmentStrokeColor : "#fff",
        //Number - The width of each segment stroke
        segmentStrokeWidth : 2,
        //Number - The percentage of the chart that we cut out of the middle
        percentageInnerCutout : 50, // This is 0 for Pie charts
        //Number - Amount of animation steps
        animationSteps : 100,
        //String - Animation easing effect
        animationEasing : "easeOutBounce",
        //Boolean - Whether we animate the rotation of the Doughnut
        animateRotate : true,
        //Boolean - Whether we animate scaling the Doughnut from the centre
        animateScale : false,
        //String - A legend template
        legendTemplate : "<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<segments.length; i++){%><li><span style=\"background-color:<%=segments[i].fillColor%>\"></span><%if(segments[i].label){%><%=segments[i].label%><%}%></li><%}%></ul>"
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

        $.ajax( '/jobs/scenario/risk/results_ajax/'+job_id+'/?country='+country+'&taxonomy='+taxonomy )
        .done(function(data) {
            display_data(data)
        });
    }


    var fill_regions_dropdowns = function(regions){
        if (level == 0){
            var $elem = $("#country");
            $("#level1").empty();
        }
        else if (level == 1){
            var $elem = $("#level1");
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
        for (var i = 0; i < taxs.length; i++){
            $('#taxonomy').append('<option value='+taxs[i].id+'>'+taxs[i].name+'</option>');    
            taxonomies.push[{id: taxs[i].id, name: taxs[i].name}]
        }
        return taxonomies;
    }

    var clean_charts = function(tab) {

        $('#'+tab+'_insured').html("<h4>Insured data:</h4> \
                                                    <canvas id='"+tab+"_insured_chart' \
                                                    width='200' height='200'></canvas>");
        $('#'+tab+'_region').html("<h4>Losses per region:</h4> \
                                                    <canvas id='"+tab+"_chart' \
                                                    width='200' height='200'></canvas>");
        $('#'+tab+'_taxonomy').html("<h4>Losses per taxonomy:</h4> \
                                                    <canvas id='"+tab+"_tax_chart' \
                                                    width='200' height='200'></canvas>");
    }

    var enable_back_button = function(){
        if ( level == 0 ){
            $('#adm_back').attr("disabled", true);
        }
        else {
            $('#adm_back').attr("disabled", false);
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

        var $active_tab = $("#myTabContent div.active");
        
        for (var i = 0; i<losses_data.length; i++){

            var $tab_elem = $( "#"+losses_data[i].name );
            $tab_elem.addClass( "tab-pane fade active in" );

            if (taxonomies == undefined){
                taxonomies = fill_taxonomy_dropdown( losses_data[i].values_per_taxonomy );
            }
            
            clean_charts(losses_data[i].name);

            //UNITS
            if ( losses_data[i].name == 'occupants_vulnerability' ){
                var units = 'fatalities';
            }
            else {
                var units = losses_data[i].currency;
            }

            //MAP DVF OPTIONS
            losses_options = get_losses_options(regions, losses_data[i].total_scale);
            losses_options.onEachRecord = function(layer, record){
                layer.on('click', function () {
                    var next_level = level+1;
                    get_data(record.id, next_level);
                });
            }

            //INSURED DATA
            if (job.insured_losses){
                $('#'+losses_data[i].name+'_total').html( '<b>Total loss:</b> ' + Humanize.intword(losses_data[i].total, 'M', 1) + ' ' + units 
                                                    +'<br><b>Insured Loss:</b> ' + Humanize.intword(losses_data[i].total_insured, 'M', 1) + ' ' + units
                                                    +'<br><b>Not insured Loss:</b> ' + Humanize.intword(losses_data[i].total - losses_data[i].total_insured, 'M', 1) + ' ' + units
                                                    );
            
                var ctx_insured = $('#'+losses_data[i].name+'_insured_chart').get(0).getContext("2d");

                insured_chart_data = [{value: losses_data[i].total - losses_data[i].total_insured,
                                        label: 'Not insured loss',
                                        color: getRandomColor(),},
                                    {value: losses_data[i].total_insured,
                                        label: 'Insured loss',
                                        color: getRandomColor(),}];
                var insured_chart = new Chart(ctx_insured).Pie(insured_chart_data, chart_options);
            }

            else {
                $('#'+losses_data[i].name+'_total').html( '<b>Total loss:</b> ' + Humanize.intword(losses_data[i].total, 'M', 1) + ' ' + units )
            }
            

            //DATA PER REGION
            var ctx = $('#'+losses_data[i].name+'_chart').get(0).getContext("2d");

            chart_data = [];
            for (var j = 0; j < losses_data[i].values.length; j++ ){
                chart_data.push({value: losses_data[i].values[j].value,
                                label: losses_data[i].values[j].place,
                                color: getRandomColor(),});
            }

            var chart = new Chart(ctx).Pie(chart_data, chart_options);


            //DATA PER TAXONOMY
            if ( losses_data[i].values_per_taxonomy ){
                var ctx_tax = $('#'+losses_data[i].name+'_tax_chart').get(0).getContext("2d");
                tax_chart_data = [];
                for (var j = 0; j < losses_data[i].values_per_taxonomy.length; j++ ){
                    tax_chart_data.push({value: losses_data[i].values_per_taxonomy[j].value,
                                        label: losses_data[i].values_per_taxonomy[j].name,
                                        color: getRandomColor(),});
                }
                var chart_per_taxonomy = new Chart(ctx_tax).Pie(tax_chart_data, chart_options);
            }
            else {
                $('#'+losses_data[i].name+'_taxonomy').empty();
            }

            $tab_elem.removeClass( "active in" );

            //ADD LAYERS
            lossesLayer = new L.ChoroplethDataLayer(losses_data[i], losses_options);

            if (i==0){
                lossesLayer.addTo(map);
            }

            lossesGroup.addLayer(lossesLayer);
            control.addOverlay(lossesLayer ,losses_data[i].name);
            map.fitBounds(lossesLayer.getBounds());

        }

        $active_tab.addClass('active in');

    }

    get_data(country, level);



});
})($); 