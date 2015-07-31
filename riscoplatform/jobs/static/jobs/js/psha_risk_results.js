"use strict";

var riskResultsApp = angular.module('riskResultsApp', ['chart.js']).config(function($interpolateProvider){
    // $interpolateProvider.startSymbol('[[').endSymbol(']]');
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
    
    var regions_control;
    var taxonomies_control;
    var poe_control;
    var statistics_control;
    var vulnerability_control;
    var charts_control;


    var url = document.URL.split('/');
    var job_id = url[url.length -2];

    var job;

    var level = 0;
    var region;
    var taxonomy;
    var poe;
    var statistics = 'mean';
    var vulnerability;
    var insured = false;

    $scope.disableAllTaxonomies = true;


    $scope.disableHome = true; 
    $scope.disableUp = true; 
    $scope.region1Disabled = true;
    $scope.region2Disabled = true;

    $scope.region_labels = [];
    $scope.region_data = [];

    $scope.taxonomies_labels = [];
    $scope.taxonomies_data = [];

    $scope.regionChart;

    var getRegion = function(level){
        if (level == 0){
            return undefined;
        }
        if (level == 1){
            return $scope.region0.id;
        }
        if (level == 2){
            return $scope.region1.id;
        }
        if (level == 3){
            return $scope.region2.id;
        }
    } 


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
        region = getRegion(level);
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

            $.ajax('/jobs/psha/risk/results_maps/'+job_id+'/?vulnerability='+vulnerability+'&level='+level+'&region='+region+'&statistics='+statistics+'&poe='+poe+'&taxonomy='+taxonomy+'&insured='+insured )
            .done(function (data) {
                display_data(data);
            }).fail(function() {

            });
        }
    };



    var display_data = function(data) {

            job = data.job[0].fields;

            //regions
            fill_regions_dropdowns(level, data.losses_per_region)

            if (regions_control == undefined){
                regions_control = new RegionSelectControl().addTo(map);
            }

            //taxonomies
            if ( taxonomies_control == undefined ){
                $scope.taxonomies = [];
                for (var i=0; i<data.losses_per_taxonomy.length; i++){
                    $scope.taxonomies.push({id:data.losses_per_taxonomy[i].id, name: data.losses_per_taxonomy[i].name});
                }
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
                vulnerability_control = new vulnerabilitySelectControl().addTo(map);
            }

            //charts
            if ( charts_control == undefined ){
                charts_control = new chartsControl().addTo(map);
            }
            
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

            //loss maps layer
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

            $scope.$apply();

        }

    load_data(level, region, taxonomy, poe, statistics, vulnerability, insured);

});



