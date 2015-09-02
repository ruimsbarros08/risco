 "use strict";

(function($) {
$( document ).ready(function() {

    //TO DO:
    //
    // * INSURANCE MAPS
    // * OTHER CHARTS


    $( "#vulnerability-selector li:first-child" ).addClass( "active" );
    $( "#myTabContent div:first-child" ).addClass( "tab-pane fade active in" );
    
    //hide-show    
    $( "label[for='region']" ).hide( "fast");

    var map = new L.Map('map', {
        fullscreenControl: true,
        fullscreenControlOptions: {
            position: 'topleft'
        }
    });
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

    $.ajax( BASE_URL+'/jobs/scenario/hazard/results_ajax/'+hazard_job_id )
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
        $.ajax(BASE_URL+ '/jobs/scenario/risk/results_ajax/'+job_id+'/?adm_1='+adm_1+'&country='+adm_0+'&taxonomy='+taxonomy )
        .done(function(data) {
            display_data(data)
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
                losses_options = get_losses_options(regions, losses_data[i].total_scale, 'values');
                losses_options.onEachRecord = function(layer, record){
                    layer.on('click', function () {
                        country = record.id;
                        var next_level = level+1;
                        get_data(country, next_level);
                    });
                }

                //INSURED DATA
                if (job.insured_losses){
                    $('#'+losses_data[i].name+'_total').html( '<b>Total loss:</b> ' + Humanize.intword(losses_data[i].total, 'M', 1) +
                        ' +- ' + Humanize.intword(losses_data[i].stddev, 'M', 1) + ' ' + units);
                
                    var ctx_insured = $('#'+losses_data[i].name+'_insured_chart').get(0).getContext("2d");
                    
                    var color_not_insured = getRandomColor();
                    var color_insured = getRandomColor();

                    $('#'+losses_data[i].name+'_insured_chart_legend ul').append('<li class="no-bullets"> <span class="glyphicon glyphicon-stop" style="color:'+color_not_insured+';" aria-hidden="true"></span> <b>Not insured:</b> '+
                                Humanize.intword(losses_data[i].total_not_insured, 'M', 1)+' +- '+
                                Humanize.intword(losses_data[i].stddev_not_insured, 'M', 1)+' '+
                                units+'</li>');
                    $('#'+losses_data[i].name+'_insured_chart_legend ul').append('<li class="no-bullets"> <span class="glyphicon glyphicon-stop" style="color:'+color_insured+';" aria-hidden="true"></span> <b>Insured:</b> '+
                                Humanize.intword(losses_data[i].total_insured, 'M', 1)+' +- '+
                                Humanize.intword(losses_data[i].stddev_insured, 'M', 1)+' '+
                                units+'</li>');

                    insured_chart_data = [{value: losses_data[i].total_not_insured,
                                            label: 'Not insured loss',
                                            color: color_not_insured,
                                            highlight: "#EBD800"},
                                        {value: losses_data[i].total_insured,
                                            label: 'Insured loss',
                                            color: color_insured,
                                            highlight: "#EBD800"}];
                    var insured_chart = new Chart(ctx_insured).Pie(insured_chart_data, chart_options);
                }

                else {
                    $('#'+losses_data[i].name+'_total').html( '<b>Total loss:</b> ' + Humanize.intword(losses_data[i].total, 'M', 1) + ' ' + units )
                }
                

                //DATA PER REGION
                var ctx = $('#'+losses_data[i].name+'_chart').get(0).getContext("2d");

                chart_data = [];
                for (var j = 0; j < losses_data[i].values.length; j++ ){
                    var color = getRandomColor();
                    $('#'+losses_data[i].name+'_chart_legend ul').append('<li class="no-bullets"> <span class="glyphicon glyphicon-stop" style="color:'+color+';" aria-hidden="true"></span> <b> '+
                                losses_data[i].values[j].name+'</b>: '+
                                Humanize.intword(losses_data[i].values[j].value, 'M', 1)+' +- '+
                                Humanize.intword(losses_data[i].values[j].stddev, 'M', 1)+' '+
                                units+'</li>');
                    chart_data.push({value: losses_data[i].values[j].value,
                                    label: losses_data[i].values[j].name,
                                    color: color,
                                    highlight: "#EBD800",});
                }
                var chart = new Chart(ctx).Pie(chart_data, chart_options);
                $('#'+losses_data[i].name+'_chart').on('click', function(evt){
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


                //DATA PER TAXONOMY
                if ( losses_data[i].values_per_taxonomy ){
                    var ctx_tax = $('#'+losses_data[i].name+'_tax_chart').get(0).getContext("2d");
                    tax_chart_data = [];
                    for (var j = 0; j < losses_data[i].values_per_taxonomy.length; j++ ){
                        var color = getRandomColor();
                        $('#'+losses_data[i].name+'_tax_chart_legend ul').append('<li class="no-bullets"> <span class="glyphicon glyphicon-stop" style="color:'+color+';" aria-hidden="true"></span> <b> '+
                                    losses_data[i].values_per_taxonomy[j].name+'</b>: '+
                                    Humanize.intword(losses_data[i].values_per_taxonomy[j].value, 'M', 1)+' +- '+
                                    Humanize.intword(losses_data[i].values_per_taxonomy[j].stddev, 'M', 1)+' '+
                                    units+'</li>');
                        
                        tax_chart_data.push({value: losses_data[i].values_per_taxonomy[j].value,
                                            label: losses_data[i].values_per_taxonomy[j].name,
                                            color: color,
                                            highlight: "#EBD800"});
                    }
                    var chart_per_taxonomy = new Chart(ctx_tax).Pie(tax_chart_data, chart_options);
                    $('#'+losses_data[i].name+'_tax_chart').on('click', function(evt){
                        try {
                            var selectedLabel = chart_per_taxonomy.getSegmentsAtEvent(evt)[0].label;
                            for (var k = 0; k < taxonomies.length; k++){
                                if (selectedLabel == taxonomies[k].name){
                                    taxonomy = taxonomies[k].id;
                                    $("#taxonomy").val(taxonomy);
                                    get_data(country, level);
                                }
                            }
                        }
                        catch(err) {
                            console.log('Click on a slice');
                        }
                    });

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
        else {
            try {
                hazardLayer.addTo(map);
            }
            catch(err) {
                console.log('Hazard is not ready yet');
            }
        }

    }

    get_data(country, level);


});
})($); 