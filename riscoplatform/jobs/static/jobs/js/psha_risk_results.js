"use strict";

var riskResultsApp = angular.module('riskResultsApp', ['chart.js']).config(function($interpolateProvider){
    $interpolateProvider.startSymbol('[[').endSymbol(']]');
});

riskResultsApp.controller('riskResultsCtrl', function($scope) {

    $('label[for="location"]').hide();

    var map = new L.Map('map', {
        fullscreenControl: true,
        fullscreenControlOptions: {
            position: 'topleft'
        }
    });
    map.setView(new L.LatLng(0, 0),2);
    osm.addTo(map);

    var control = L.control.layers(baseLayers).addTo(map);
    var legendControl = new L.Control.Legend();
    var lossesLayer;
    var markerList;

    var regions_control;
    var taxonomies_control;
    var poe_control;
    var statistics_control;
    var vulnerability_control;
    var insurance_control;
    var charts_control;

    var url = document.URL.split('/');
    var job_id = url[url.length -2];

    var job;
    var exposure_model;

    var level = 0;
    var region;
    var taxonomy;
    var poe;
    var statistics = 'mean';
    var vulnerability;
    var insured = false;

    $scope.disableAllTaxonomies = true;
    $scope.disableLossCurve = false;

    $scope.disableHome = true; 
    $scope.disableUp = true;
    $scope.region0Disabled = false; 
    $scope.region1Disabled = true;
    $scope.region2Disabled = true;

    $scope.region_labels = [];
    $scope.region_data = [];

    $scope.taxonomiesDisabled = false;
    $scope.poesDisabled = false;
    $scope.statisticsDisabled = false;
    $scope.vulnerabilityDisabled = false;
    $scope.insuranceDisabled = false;

    $scope.taxonomies_labels = [];
    $scope.taxonomies_data = [];

    $scope.insured_available == false;
    $scope.insurance_opts = [{name: 'Insured losses', value: true},
                            {name: 'Total losses', value: false}];
    $scope.insured = false;
    $scope.asset;

    $scope.regionChart;

    $scope.charts_options = {   
        tooltipTemplate: "<%if (label){%><%=label%>: <%}%><%= Humanize.intword( value, '', 4)  %>",
    };

    $scope.selectRegion = function(l, r){
        level = l;
        region = r;
        load_data(level, region, taxonomy, poe, statistics, vulnerability, insured);
    }

    $scope.goHome = function(){
        level = 0;
        region = undefined;
        load_data(level, region, taxonomy, poe, statistics, vulnerability, insured);
    }

    $scope.upOneLevel = function(){
        level -= 1;
        load_data(level, region, taxonomy, poe, statistics, vulnerability, insured);
    }

    $scope.setTaxonomy = function(tx){
        taxonomy = tx;
        load_data(level, region, taxonomy, poe, statistics, vulnerability, insured);
        $scope.disableAllTaxonomies = false;
    }

    $scope.allTaxonomies = function(){
        taxonomy = undefined;
        load_data(level, region, taxonomy, poe, statistics, vulnerability, insured);
        $scope.disableAllTaxonomies = true;
        $scope.taxonomy = undefined;
    }

    $scope.setPoe = function(p){
        poe = p;
        load_data(level, region, taxonomy, poe, statistics, vulnerability, insured);
    }

    $scope.setQuantile = function(stat){
        statistics = stat; 
        load_data(level, region, taxonomy, poe, statistics, vulnerability, insured)
    }

    $scope.setVulnerability = function(vul){
        vulnerability = vul; 
        load_data(level, region, taxonomy, poe, statistics, vulnerability, insured)
    }

    $scope.setInsurance = function(ins){
        insured = ins;
        load_data(level, region, taxonomy, poe, statistics, vulnerability, insured)
    }

    var fill_regions_dropdowns = function(level, regions){

        if (level == 0){

            $scope.region1Disabled = true;
            $scope.region2Disabled = true;

            $scope.disableHome = true; 
            $scope.disableUp = true; 

            $scope.regions0 = regions;
            $scope.regions1 = [];
            $scope.regions2 = [];
        }
        if (level == 1){

            $scope.region1Disabled = false;
            $scope.region2Disabled = true;

            $scope.disableHome = false; 
            $scope.disableUp = false; 

            $scope.regions1 = regions;
            $scope.regions2 = [];
        }
        if (level == 2){
            $scope.region2Disabled = false;
            $scope.regions2 = regions;
        }

        $scope.$apply();
    }



    var load_data = function(level, region, taxonomy, poe, statistics, vulnerability, insured) {

        if (level > 0 && region == undefined){
            return
        }
        else {

            $.ajax(BASE_URL+'/jobs/psha/risk/results_maps/'+job_id+'/?vulnerability='+vulnerability+'&level='+level+'&region='+region+'&statistics='+statistics+'&poe='+poe+'&taxonomy='+taxonomy+'&insured='+insured )
            .done(function (data) {
                display_data(data);
            }).fail(function() {

            });
        }
    };

    var load_curves = function(asset, marker){

        $.ajax(BASE_URL+'/jobs/psha/risk/results_curves/'+job_id+'/?vulnerability='+vulnerability+'&asset='+asset+'&statistics='+statistics+'&insured='+insured )
        .done(function (data) {

            $scope.asset = data;
            $scope.asset.asset_value = Humanize.intword($scope.asset.asset_value, '', 2)+' '+$scope.currency;
            $scope.asset.average_loss_ratio = Humanize.intword($scope.asset.average_loss_ratio, '', 4);
            $scope.asset.stddev_loss_ratio = Humanize.intword($scope.asset.stddev_loss_ratio, '', 4);

            $scope.asset.name = marker.name;
            $scope.asset.loss = Humanize.intword(marker.number, '', 2)+' '+$scope.currency;

            var dataset = [{
                              label: 'Loss curve',
                              strokeColor: '#F16220',
                              pointColor: '#F16220',
                              pointStrokeColor: '#fff',
                              data: []
                            }]

            for (var i = 0; i<data.poes.length; i++){
                dataset[0].data.push({x: data.poes[i], y: data.loss_ratios[i] });
            }

            var ctx = document.getElementById("loss_curve").getContext("2d");
            var chart = new Chart(ctx).Scatter(dataset, {scaleLabel: "<%=Humanize.intword(value, '', 2)%>"});
            
            $scope.$apply();

            var elem = angular.element('#marker-popup').html();

            marker.bindPopup(elem);
            marker.openPopup();
        }).fail(function() {

        });

    }

    var add_controls = function(data){
        //regions
        fill_regions_dropdowns(level, data.losses_per_region)

        if (regions_control == undefined){
            regions_control = new RegionSelectControl().addTo(map);
        }

        //taxonomies
        $scope.taxonomies = [];
        for (var i=0; i<data.losses_per_taxonomy.length; i++){
            $scope.taxonomies.push({id:data.losses_per_taxonomy[i].id, name: data.losses_per_taxonomy[i].name});
        }
        if ( taxonomies_control == undefined ){
            taxonomies_control = new TaxonomySelectControl().addTo(map);
        }

        //poes
        if ( poe_control == undefined ){
            $scope.poes = [];
            var poes_list = job.poes.split(',');
            for (var i = 0; i< poes_list.length; i++){
                var new_poe = poes_list[i].replace("[", "").replace("]", "").trim();
                $scope.poes.push(new_poe);
            }
            $scope.poe = data.poe.toString();
            poe = data.poe;
            poe_control = new PoeSelectControl().addTo(map);
        }

        //statistics
        if ( statistics_control == undefined ){
            $scope.quantiles = ['mean'];
            var statistics_list = job.quantile_loss_curves.split(',');
            for (var i = 0; i< statistics_list.length; i++){
                var new_quantile = statistics_list[i].replace("[", "").replace("]", "").trim();
                $scope.quantiles.push(new_quantile);
            }
            $scope.statistics = data.statistics.toString();
            statistics_control = new StatisticsSelectControl().addTo(map);
        }

        //vulnerability
        if ( vulnerability_control == undefined ){
            $scope.vulnerabilities = data.vulnerabilities;
            $scope.vulnerability = data.vulnerability;
            vulnerability = data.vulnerability;
            vulnerability_control = new vulnerabilitySelectControl().addTo(map);
        }

        if ( insurance_control == undefined && job.insured_losses == true ){
            $scope.insured_available == true;
            insurance_control = new insuranceSelectControl().addTo(map);
        }

        //charts
        if ( charts_control == undefined ){
            charts_control = new chartsControl().addTo(map);
        }
    }

    var display_data = function(data) {

            job = data.job[0].fields;
            exposure_model = data.exposure_model[0].fields;



            if (job.status == 'FINISHED'){
               
                add_controls(data);
                
                $scope.region_labels = [];
                $scope.region_data = [];

                $scope.taxonomies_labels = [];
                $scope.taxonomies_data = [];

                var max_value = 0;
                for (var i=0; i < data.losses_per_region.length; i++){
                    if (data.losses_per_region[i].value > max_value){
                        max_value = data.losses_per_region[i].value;
                    }

                    $scope.region_labels.push(data.losses_per_region[i].name);
                    $scope.region_data.push(data.losses_per_region[i].value);
                }

                $scope.onRegionChartClick = function(points, evt){
                    try {
                        var selectedLabel = points[0].label;
                        for (var k = 0; k < data.geojson.features.length; k++){
                            if (selectedLabel == data.geojson.features[k].properties.name){
                                region = data.geojson.features[k].id;
                                level = level+1;
                                $scope.selectRegion(level, region);
                            }
                        }

                    }
                    catch(err){
                        console.log('Click on a slice')
                    }
            
                };


                $scope.onTaxonomyChartClick = function(points, evt){
                    try {
                        var selectedLabel = points[0].label;
                        for (var k = 0; k < data.losses_per_taxonomy.length; k++){
                            if (selectedLabel == data.losses_per_taxonomy[k].name){
                                $scope.setTaxonomy(data.losses_per_taxonomy[k].id);
                            }
                        }

                    }
                    catch(err){
                        console.log('Click on a slice')
                    }
            
                };

                for (var i=0; i < data.losses_per_taxonomy.length; i++){
                    $scope.taxonomies_labels.push(data.losses_per_taxonomy[i].name);
                    $scope.taxonomies_data.push(data.losses_per_taxonomy[i].value);
                }

                try{
                    map.removeLayer( lossesLayer );
                    // legendControl.removeFrom( map );
                }
                catch(err){
                }

                //AGGREGATE PML
                try {
                    var dataset = [{
                                      label: 'PML',
                                      strokeColor: '#F16220',
                                      pointColor: '#F16220',
                                      pointStrokeColor: '#fff',
                                      data: []
                                    }]

                    for (var i = 0; i<data.pml.at_loss_rates_agg.length; i++){
                        dataset[0].data.push({x: data.pml.at_loss_rates_agg[i], y: data.pml.it_loss_values_agg[i] });
                    }

                    var ctx = document.getElementById("agg_chart").getContext("2d");
                    var agg_chart = new Chart(ctx).Scatter(dataset, {scaleLabel: "<%=Humanize.intword(value, '', 2)%>"});
                }
                catch(err){}


                //OCCURRENCES PML
                try {
                    var dataset = [{
                                      label: 'PML',
                                      strokeColor: '#F16220',
                                      pointColor: '#F16220',
                                      pointStrokeColor: '#fff',
                                      data: []
                                    }]

                    for (var i = 0; i<data.pml.at_loss_rates_occ.length; i++){
                        dataset[0].data.push({x: data.pml.at_loss_rates_occ[i], y: data.pml.it_loss_values_occ[i] });
                    }

                    var ctx = document.getElementById("occ_chart").getContext("2d");
                    var occ_chart = new Chart(ctx).Scatter(dataset, {scaleLabel: "<%=Humanize.intword(value, '', 2)%>"});
                }
                catch(err){}

                try {

                    // if (data.pml.default_periods_agg.length >= data.pml.default_periods_occ.length){
                    //     $scope.greater_list = data.pml.default_periods_agg;
                    // }
                    // else {
                    //     $scope.greater_list = data.pml.default_periods_occ;
                    // }
                    $scope.pml = data.pml;

                    for (var key in $scope.pml){
                        if (key !== 'default_periods_agg' && key !== 'default_periods_occ' ){
                            for (var i = 0; i<$scope.pml[key].length; i++){
                                $scope.pml[key][i] = Humanize.intword( $scope.pml[key][i], '', 3);
                            }
                        }
                    }

                    $scope.pml.aal_agg = Humanize.intword( $scope.pml['aal_agg'], '', 3);
                    $scope.pml.aal_occ = Humanize.intword( $scope.pml['aal_occ'], '', 3);
                }
                catch(err){}

                //loss maps layer
                if (level != 3){

                    if (data.vulnerability == 'structural_vulnerability'){
                        $scope.currency = exposure_model.struct_cost_currency;
                    }
                    else if (data.vulnerability == 'nonstructural_vulnerability'){
                        $scope.currency = exposure_model.non_struct_cost_currency;
                    }
                    else if (data.vulnerability == 'contents_vulnerability'){
                        $scope.currency = exposure_model.contents_cost_currency;
                    }
                    else if (data.vulnerability == 'business_int_vulnerability'){
                        $scope.currency = exposure_model.business_int_cost_currency;
                    }
                    else {
                        $scope.currency = 'fatalities';
                    }

                    $scope.disableLossCurve = false;
                    var losses_options = get_losses_options(data.geojson, max_value, 'losses_per_region');
                    losses_options.onEachRecord = function(layer, record){
                        layer.on('click', function () {
                            region = record.id;
                            level = level+1;
                            $scope.selectRegion(level, region);
                        });
                    }


                    lossesLayer = new L.ChoroplethDataLayer(data, losses_options);

                    lossesLayer.addTo(map);
                    map.fitBounds(lossesLayer.getBounds());
                    
                    legendControl.addTo(map);
                }
                else {
                    $scope.disableLossCurve = true;
                    markerList = [];
                    lossesLayer = new L.markerClusterGroup({
                        iconCreateFunction: function (cluster) {
                            var markers = cluster.getAllChildMarkers();
                            var n = 0;
                            for (var i = 0; i < markers.length; i++) {
                                n += markers[i].number;
                            }
                            return L.divIcon({ html: Humanize.intword(n, '', 2)+' '+$scope.currency, className: 'cluster', iconSize: L.point(40, 40) });
                        },
                    });

                    for (var i=0; i<data.losses_per_region.length; i++){

                        var marker = L.marker(L.latLng(data.losses_per_region[i].lat, data.losses_per_region[i].lon));
                        
                        marker.name = data.losses_per_region[i].name;
                        marker.number = data.losses_per_region[i].value;
                        marker.index = i;

                        marker.on('click', function (){
                            load_curves(data.losses_per_region[ this.index ].id, this);
                        });
                        markerList.push(marker);

                    };

                    lossesLayer.addLayers(markerList);
                    map.addLayer(lossesLayer);
                    // control.addOverlay(lossesLayer, 'Assets');

                    map.fitBounds(lossesLayer);


                }

                $scope.$apply();

            }
            else {
                $scope.region0Disabled = true;
                $scope.taxonomiesDisabled = true;
                $scope.poesDisabled = true;
                $scope.statisticsDisabled = true;
                $scope.vulnerabilityDisabled = true;
                $scope.insuranceDisabled = true;
                add_controls(data);

            }

        }

    load_data(level, region, taxonomy, poe, statistics, vulnerability, insured);

});



