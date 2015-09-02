"use strict";

var exposureApp = angular.module('exposureApp', ['ui-notification']).config(function($interpolateProvider, NotificationProvider){
    $interpolateProvider.startSymbol('[[').endSymbol(']]');
        NotificationProvider.setOptions({
            delay: 10000,
            startTop: 20,
            startRight: 10,
            verticalSpacing: 20,
            horizontalSpacing: 20,
            positionX: 'left',
            positionY: 'bottom'
        });

});

exposureApp.controller('exposureCtrl', function($scope, Notification) {

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
    var regions_control;

    // Initialize the FeatureGroup to store editable layers
    //var drawnItems = new L.FeatureGroup();
    //map.addLayer(drawnItems);


    var url = document.URL.split('/');
    var model_id = url[url.length -2];


    var container = document.getElementById('assets_table_container');
    var table;

    var colHeaders;
    var dataSchema;
    var columns;

    var model;

    var level = 0;
    var region;
    var taxonomy;

    var markerList = [];
    var markers = new L.markerClusterGroup();

    var drawControl = new L.Control.Draw({
        edit: {
            featureGroup: markers,
        },
        draw: {
            polyline: false,
            polygon: false,
            rectangle: false,
            circle: false,
        }
    });
    map.addControl(drawControl);

    var assets;
    var assetsTags;
    var taxonomies = [];

    $scope.asset_name = 'Select an asset';
    $scope.disableSave = true;
    $scope.disableDelete = true;
    $scope.disableAllTaxonomies = true;

    $scope.stack = false;

    $scope.disableHome = true; 
    $scope.disableUp = true; 
    $scope.region1Disabled = true;
    $scope.region2Disabled = true;

    $scope.selectedAssets = [];

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


    $scope.selectRegion = function(l, region){
        level = l;
        load_assets(level, region, taxonomy);
    }

    $scope.goHome = function(){
        level = 0;
        load_assets(level, undefined, taxonomy);
    }

    $scope.upOneLevel = function(){
        level -= 1;
        region = getRegion(level);
        load_assets(level, region, taxonomy);
    }

    $scope.setTaxonomy = function(tx){
        taxonomy = tx;
        load_assets(level, region, taxonomy)
    }

    $scope.allTaxonomies = function(){
        taxonomy = undefined;
        load_assets(level, region, taxonomy);
    }

    $scope.scrollToTop = function(){
        table.selectCell(0,0)
    }

    $scope.scrollToEnd = function(){
        table.selectCell(table.countRows() -1 ,0)
    }

    $scope.saveData = function(){
        var tableData = table.getData();
        var uploadData = [];

        for (var i=0; i<tableData.length; i++){
            if (tableData[i].name && tableData[i].lat && tableData[i].lon && tableData[i].taxonomy ){
                uploadData.push(tableData[i]);
            }
        } 

        $.ajax(BASE_URL+'/models/exposure/'+model_id+'/assets/', {
            method: "POST",
            data: JSON.stringify(uploadData)
        })
        .done(function(data) {
            display_data(data);
            Notification.success('Assets uploaded');
        }).fail(function() {
            Notification.error('Error on the upload');
        });
    }

    $scope.deleteAssets = function(){
        var assets = assetsTags.getTags();

        $.ajax(BASE_URL+'/models/exposure/'+model_id+'/assets/', {
            method: "DELETE",
            data: JSON.stringify(assets)
        })
        .done(function(data) {
            display_data(data);
            Notification.success('Assets deleted');
        }).fail(function() {
            Notification.error('Error');
        });

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

    var asset_chart;
    var asset_occ_chart;
    var ctx = $("#asset_chart").get(0).getContext("2d");
    var ctx_occ = $("#asset_occ_chart").get(0).getContext("2d");
    
    var charts_assets = [];

    var draw_charts = function(asset, asset_chart_data){
        
        if ( asset_chart == undefined ){

            asset_chart_data.datasets[0].label = asset.name;

            if (asset.struct_cost){
                asset_chart_data.datasets[0].data.push(asset.struct_cost);

                if (asset.retrofitting_cost){
                    asset_chart_data.datasets[0].data.push(asset.retrofitting_cost);
                }
                else {
                    asset_chart_data.datasets[0].data.push(0);
                }
            }

            if (asset.non_struct_cost){
                asset_chart_data.datasets[0].data.push(asset.non_struct_cost);
            }
            if (asset.contents_cost){
                asset_chart_data.datasets[0].data.push(asset.contents_cost);
            }
            if (asset.business_int_cost){
                asset_chart_data.datasets[0].data.push(asset.business_int_cost);
            }

            var asset_occ_chart_data = {
                labels: [],
                datasets: [
                    {
                        fillColor: "rgba(220,220,220,0.5)",
                        strokeColor: "rgba(220,220,220,0.8)",
                        highlightFill: "rgba(220,220,220,0.75)",
                        highlightStroke: "rgba(220,220,220,1)",
                        data: []
                    },
                ]
            }

            asset_occ_chart_data.labels.push('Day');
            asset_occ_chart_data.labels.push('Night');
            asset_occ_chart_data.labels.push('Transit');
            if (asset.oc_day){
                asset_occ_chart_data.datasets[0].data.push(asset.oc_day);
            }
            else {
                asset_occ_chart_data.datasets[0].data.push(0);
            }

            if (asset.oc_night){
                asset_occ_chart_data.datasets[0].data.push(asset.oc_night);
            }
            else {
                asset_occ_chart_data.datasets[0].data.push(0);
            }

            if (asset.oc_transit){
                asset_occ_chart_data.datasets[0].data.push(asset.oc_transit);
            }
            else {
                asset_occ_chart_data.datasets[0].data.push(0);
            }

            asset_chart = new Chart(ctx).Bar(asset_chart_data, {responsive: true,
                                                                maintainAspectRatio: true,});
            
            asset_occ_chart = new Chart(ctx_occ).Bar(asset_occ_chart_data, {responsive: true,
                                                                            maintainAspectRatio: true,});

        }
        else {

            var idx;
            asset_chart.datasets[0].label = asset.name;
            if (asset.struct_cost){

                idx = asset_chart_data.labels.indexOf('Structural');
                asset_chart.datasets[0].bars[idx].value = asset.struct_cost;
                
                idx = asset_chart_data.labels.indexOf('Retrofit');
                if (asset.retrofitting_cost){
                    asset_chart.datasets[0].bars[idx].value = asset.retrofitting_cost;
                }
                else {
                    asset_chart.datasets[0].bars[idx].value = 0;
                }
            }

            if (asset.non_struct_cost){
                idx = asset_chart_data.labels.indexOf('Non structural');
                asset_chart.datasets[0].bars[idx].value = asset.non_struct_cost;
            }
            if (asset.contents_cost){
                idx = asset_chart_data.labels.indexOf('Contents');
                asset_chart.datasets[0].bars[idx].value = asset.contents_cost;
            }
            if (asset.business_int_cost){
                idx = asset_chart_data.labels.indexOf('Business Interruption');
                asset_chart.datasets[0].bars[idx].value = asset.business_int_cost;
            }

            if (asset.oc_day){
                asset_occ_chart.datasets[0].bars[0].value = asset.oc_day;
            }
            else {
                asset_occ_chart.datasets[0].bars[0].value = 0;
            }
            if (asset.oc_night){
                asset_occ_chart.datasets[0].bars[1].value = asset.oc_night;
            }
            else {
                asset_occ_chart.datasets[0].bars[1].value = 0;
            }
            if (asset.oc_transit){
                asset_occ_chart.datasets[0].bars[2].value = asset.oc_transit;
            }
            else {
                asset_occ_chart.datasets[0].bars[1].value = 0;
            }

            asset_chart.update();
            asset_occ_chart.update();
        }
}


    var draw_stacked_charts = function(model, asset, asset_chart_data){

        var deductible_dataset_index;
        var cost_dataset_index;
        var limit_dataset_index;

        if (model.insurance_limit){
            limit_dataset_index = 0;
            cost_dataset_index = 1;
            if (model.deductible){
                deductible_dataset_index = 2;
            }
        }
        else {
            cost_dataset_index = 0;
            if (model.deductible){
                deductible_dataset_index = 1;
            }
        }
        
        if ( asset_chart == undefined ){

            //asset_chart_data.datasets[0].label = asset.name;

            if (asset.struct_cost){
                var struct_deductible = 0;
                var struct_cost = asset.struct_cost;
                var struct_insurance_limit = 0;
                if (asset.struct_deductible){
                    if (model.deductible == 'relative'){
                        struct_deductible = asset.struct_cost * asset.struct_deductible;
                    }
                    else {
                        struct_deductible = asset.struct_deductible;
                    }
                    asset_chart_data.datasets[deductible_dataset_index].data.push(struct_deductible);
                    struct_cost = struct_cost - struct_deductible;

                    if (asset.struct_insurance_limit){
                        if (model.insurance_limit == 'relative'){
                            struct_insurance_limit = asset.struct_cost - asset.struct_cost * asset.struct_insurance_limit;
                        }
                        else {
                            struct_insurance_limit = asset.struct_cost - asset.struct_insurance_limit;
                        }
                        asset_chart_data.datasets[limit_dataset_index].data.push(struct_insurance_limit);
                        struct_cost = struct_cost - struct_insurance_limit;
                    }
                }
                asset_chart_data.datasets[cost_dataset_index].data.push(struct_cost);

                if (deductible_dataset_index != undefined){
                    asset_chart_data.datasets[deductible_dataset_index].data.push(0);
                }
                if (limit_dataset_index != undefined){
                    asset_chart_data.datasets[limit_dataset_index].data.push(0);
                }
                if (asset.retrofitting_cost){
                    asset_chart_data.datasets[cost_dataset_index].data.push(asset.retrofitting_cost);
                }
                else {
                    asset_chart_data.datasets[cost_dataset_index].data.push(0);
                }
            }

            if (asset.non_struct_cost){
                var non_struct_deductible = 0;
                var non_struct_cost = asset.non_struct_cost;
                var non_struct_insurance_limit = 0;
                if (asset.non_struct_deductible){
                    if (model.deductible == 'relative'){
                        non_struct_deductible = asset.non_struct_cost * asset.non_struct_deductible;
                    }
                    else {
                        non_struct_deductible = asset.non_struct_deductible;
                    }
                    asset_chart_data.datasets[deductible_dataset_index].data.push(non_struct_deductible);
                    non_struct_cost = non_struct_cost - non_struct_deductible;

                    if (asset.non_struct_insurance_limit){
                        if (model.insurance_limit == 'relative'){
                            non_struct_insurance_limit = asset.non_struct_cost - asset.non_struct_cost * asset.non_struct_insurance_limit;
                        }
                        else {
                            non_struct_insurance_limit = asset.non_struct_cost - asset.non_struct_insurance_limit;
                        }
                        asset_chart_data.datasets[limit_dataset_index].data.push(non_struct_insurance_limit);
                        non_struct_cost = non_struct_cost - non_struct_insurance_limit;
                    }
                }
                asset_chart_data.datasets[cost_dataset_index].data.push(non_struct_cost);

            }

            if (asset.contents_cost){
                var contents_deductible = 0;
                var contents_cost = asset.contents_cost;
                var contents_insurance_limit = 0;
                if (asset.contents_deductible){
                    if (model.deductible == 'relative'){
                        contents_deductible = asset.contents_cost * asset.contents_deductible;
                    }
                    else {
                        contents_deductible = asset.contents_deductible;
                    }
                    asset_chart_data.datasets[deductible_dataset_index].data.push(contents_deductible);
                    contents_cost = contents_cost - contents_deductible;

                    if (asset.contents_insurance_limit){
                        if (model.insurance_limit == 'relative'){
                            contents_insurance_limit = asset.contents_cost - asset.contents_cost * asset.contents_insurance_limit;
                        }
                        else {
                            contents_insurance_limit = asset.contents_cost - asset.contents_insurance_limit;
                        }
                        asset_chart_data.datasets[limit_dataset_index].data.push(contents_insurance_limit);
                        contents_cost = contents_cost - contents_insurance_limit;
                    }
                }
                asset_chart_data.datasets[cost_dataset_index].data.push(contents_cost);

            }


            if (asset.business_int_cost){
                var business_int_deductible = 0;
                var business_int_cost = asset.business_int_cost;
                var business_int_insurance_limit = 0;
                if (asset.business_int_deductible){
                    if (model.deductible == 'relative'){
                        business_int_deductible = asset.business_int_cost * asset.business_int_deductible;
                    }
                    else {
                        business_int_deductible = asset.business_int_deductible;
                    }
                    asset_chart_data.datasets[deductible_dataset_index].data.push(business_int_deductible);
                    business_int_cost = business_int_cost - business_int_deductible;

                    if (asset.business_int_insurance_limit){
                        if (model.insurance_limit == 'relative'){
                            business_int_insurance_limit = asset.business_int_cost - asset.business_int_cost * asset.business_int_insurance_limit;
                        }
                        else {
                            business_int_insurance_limit = asset.business_int_cost - asset.business_int_insurance_limit;
                        }
                        asset_chart_data.datasets[limit_dataset_index].data.push(business_int_insurance_limit);
                        business_int_cost = business_int_cost - business_int_insurance_limit;
                    }
                }
                asset_chart_data.datasets[cost_dataset_index].data.push(business_int_cost);

            }


            asset_chart = new Chart(ctx).StackedBar(asset_chart_data, {responsive: true,
                                                                maintainAspectRatio: false,});

            var asset_occ_chart_data = {
                labels: [],
                datasets: [
                    {
                        fillColor: "rgba(220,220,220,0.5)",
                        strokeColor: "rgba(220,220,220,0.8)",
                        highlightFill: "rgba(220,220,220,0.75)",
                        highlightStroke: "rgba(220,220,220,1)",
                        data: []
                    },
                ]
            }

            asset_occ_chart_data.labels.push('Day');
            asset_occ_chart_data.labels.push('Night');
            asset_occ_chart_data.labels.push('Transit');
            if (asset.oc_day){
                asset_occ_chart_data.datasets[0].data.push(asset.oc_day);
            }
            else {
                asset_occ_chart_data.datasets[0].data.push(0);
            }

            if (asset.oc_night){
                asset_occ_chart_data.datasets[0].data.push(asset.oc_night);
            }
            else {
                asset_occ_chart_data.datasets[0].data.push(0);
            }

            if (asset.oc_transit){
                asset_occ_chart_data.datasets[0].data.push(asset.oc_transit);
            }
            else {
                asset_occ_chart_data.datasets[0].data.push(0);
            }

            
            asset_occ_chart = new Chart(ctx_occ).Bar(asset_occ_chart_data, {responsive: true,
                                                                            maintainAspectRatio: false,});

        }
        else {


            var idx;
            //asset_chart.datasets[0].label = asset.name;


            if (asset.struct_cost){

                idx = asset_chart_data.labels.indexOf('Structural');

                var struct_deductible = 0;
                var struct_cost = asset.struct_cost;
                var struct_insurance_limit = 0;
                if (asset.struct_deductible){
                    if (model.deductible == 'relative'){
                        struct_deductible = asset.struct_cost * asset.struct_deductible;
                    }
                    else {
                        struct_deductible = asset.struct_deductible;
                    }
                    //asset_chart_data.datasets[deductible_dataset_index].data.push(struct_deductible);
                    asset_chart.datasets[deductible_dataset_index].bars[idx].value = struct_deductible;
                    struct_cost = struct_cost - struct_deductible;

                    if (asset.struct_insurance_limit){
                        if (model.insurance_limit == 'relative'){
                            struct_insurance_limit = asset.struct_cost - asset.struct_cost * asset.struct_insurance_limit;
                        }
                        else {
                            struct_insurance_limit = asset.struct_cost - asset.struct_insurance_limit;
                        }
                        //asset_chart_data.datasets[limit_dataset_index].data.push(struct_insurance_limit);
                        asset_chart.datasets[limit_dataset_index].bars[idx].value = struct_insurance_limit;
                        struct_cost = struct_cost - struct_insurance_limit;
                    }
                }
                //asset_chart_data.datasets[cost_dataset_index].data.push(struct_cost);
                asset_chart.datasets[cost_dataset_index].bars[idx].value = struct_cost;

                idx = asset_chart_data.labels.indexOf('Retrofit');
                if (deductible_dataset_index != undefined){
                    //asset_chart_data.datasets[deductible_dataset_index].data.push(0);
                    asset_chart.datasets[deductible_dataset_index].bars[idx].value = 0;
                }
                if (limit_dataset_index != undefined){
                    //asset_chart_data.datasets[limit_dataset_index].data.push(0);
                    asset_chart.datasets[limit_dataset_index].bars[idx].value = 0;
                }
                if (asset.retrofitting_cost){
                    //asset_chart_data.datasets[cost_dataset_index].data.push(asset.retrofitting_cost);
                    asset_chart.datasets[cost_dataset_index].bars[idx].value = asset.retrofitting_cost;
                }
                else {
                    //asset_chart_data.datasets[cost_dataset_index].data.push(0);
                    asset_chart.datasets[cost_dataset_index].bars[idx].value = 0;
                }
            }


            if (asset.non_struct_cost){

                idx = asset_chart_data.labels.indexOf('Non structural');
                var non_struct_deductible = 0;
                var non_struct_cost = asset.non_struct_cost;
                var non_struct_insurance_limit = 0;
                if (asset.non_struct_deductible){
                    if (model.deductible == 'relative'){
                        non_struct_deductible = asset.non_struct_cost * asset.non_struct_deductible;
                    }
                    else {
                        non_struct_deductible = asset.non_struct_deductible;
                    }
                    //asset_chart_data.datasets[deductible_dataset_index].data.push(non_struct_deductible);
                    asset_chart.datasets[deductible_dataset_index].bars[idx].value = non_struct_deductible;
                    non_struct_cost = non_struct_cost - non_struct_deductible;

                    if (asset.non_struct_insurance_limit){
                        if (model.insurance_limit == 'relative'){
                            non_struct_insurance_limit = asset.non_struct_cost - asset.non_struct_cost * asset.non_struct_insurance_limit;
                        }
                        else {
                            non_struct_insurance_limit = asset.non_struct_cost - asset.non_struct_insurance_limit;
                        }
                        //asset_chart_data.datasets[limit_dataset_index].data.push(non_struct_insurance_limit);
                        asset_chart.datasets[limit_dataset_index].bars[idx].value = non_struct_insurance_limit;
                        non_struct_cost = non_struct_cost - non_struct_insurance_limit;
                    }
                }
                //asset_chart_data.datasets[cost_dataset_index].data.push(non_struct_cost);
                asset_chart.datasets[cost_dataset_index].bars[idx].value = non_struct_cost;

            }

            if (asset.contents_cost){
                idx = asset_chart_data.labels.indexOf('Contents');
                var contents_deductible = 0;
                var contents_cost = asset.contents_cost;
                var contents_insurance_limit = 0;
                if (asset.contents_deductible){
                    if (model.deductible == 'relative'){
                        contents_deductible = asset.contents_cost * asset.contents_deductible;
                    }
                    else {
                        contents_deductible = asset.contents_deductible;
                    }
                    //asset_chart_data.datasets[deductible_dataset_index].data.push(contents_deductible);
                    asset_chart.datasets[deductible_dataset_index].bars[idx].value = contents_deductible;
                    contents_cost = contents_cost - contents_deductible;

                    if (asset.contents_insurance_limit){
                        if (model.insurance_limit == 'relative'){
                            contents_insurance_limit = asset.contents_cost - asset.contents_cost * asset.contents_insurance_limit;
                        }
                        else {
                            contents_insurance_limit = asset.contents_cost - asset.contents_insurance_limit;
                        }
                        //asset_chart_data.datasets[limit_dataset_index].data.push(contents_insurance_limit);
                        asset_chart.datasets[limit_dataset_index].bars[idx].value = contents_insurance_limit;
                        contents_cost = contents_cost - contents_insurance_limit;
                    }
                }
                //asset_chart_data.datasets[cost_dataset_index].data.push(contents_cost);
                asset_chart.datasets[cost_dataset_index].bars[idx].value = contents_cost;

            }


            if (asset.business_int_cost){
                idx = asset_chart_data.labels.indexOf('Business Interruption');
                var business_int_deductible = 0;
                var business_int_cost = asset.business_int_cost;
                var business_int_insurance_limit = 0;
                if (asset.business_int_deductible){
                    if (model.deductible == 'relative'){
                        business_int_deductible = asset.business_int_cost * asset.business_int_deductible;
                    }
                    else {
                        business_int_deductible = asset.business_int_deductible;
                    }
                    //asset_chart_data.datasets[deductible_dataset_index].data.push(business_int_deductible);
                    asset_chart.datasets[deductible_dataset_index].bars[idx].value = business_int_deductible;
                    business_int_cost = business_int_cost - business_int_deductible;

                    if (asset.business_int_insurance_limit){
                        if (model.insurance_limit == 'relative'){
                            business_int_insurance_limit = asset.business_int_cost - asset.business_int_cost * asset.business_int_insurance_limit;
                        }
                        else {
                            business_int_insurance_limit = asset.business_int_cost - asset.business_int_insurance_limit;
                        }
                        //asset_chart_data.datasets[limit_dataset_index].data.push(business_int_insurance_limit);
                        asset_chart.datasets[limit_dataset_index].bars[idx].value = business_int_insurance_limit;
                        business_int_cost = business_int_cost - business_int_insurance_limit;
                    }
                }
                //asset_chart_data.datasets[cost_dataset_index].data.push(business_int_cost);
                asset_chart.datasets[cost_dataset_index].bars[idx].value = business_int_cost;

            }




            // if (asset.struct_cost){

            //     idx = asset_chart_data.labels.indexOf('Structural');
            //     asset_chart.datasets[0].bars[idx].value = asset.struct_cost;
                
            //     idx = asset_chart_data.labels.indexOf('Retrofit');
            //     if (asset.retrofitting_cost){
            //         asset_chart.datasets[0].bars[idx].value = asset.retrofitting_cost;
            //     }
            //     else {
            //         asset_chart.datasets[0].bars[idx].value = 0;
            //     }
            // }

            // if (asset.non_struct_cost){
            //     idx = asset_chart_data.labels.indexOf('Non structural');
            //     asset_chart.datasets[0].bars[idx].value = asset.struct_cost;
            // }
            // if (asset.contents_cost){
            //     idx = asset_chart_data.labels.indexOf('Contents');
            //     asset_chart.datasets[0].bars[idx].value = asset.contents_cost;
            // }
            // if (asset.business_int_cost){
            //     idx = asset_chart_data.labels.indexOf('Business Interruption');
            //     asset_chart.datasets[0].bars[idx].value = asset.business_int_cost;
            // }

            if (asset.oc_day){
                asset_occ_chart.datasets[0].bars[0].value = asset.oc_day;
            }
            else {
                asset_occ_chart.datasets[0].bars[0].value = 0;
            }
            if (asset.oc_night){
                asset_occ_chart.datasets[0].bars[1].value = asset.oc_night;
            }
            else {
                asset_occ_chart.datasets[0].bars[1].value = 0;
            }
            if (asset.oc_transit){
                asset_occ_chart.datasets[0].bars[2].value = asset.oc_transit;
            }
            else {
                asset_occ_chart.datasets[0].bars[1].value = 0;
            }

            console.log(asset_chart);

            asset_chart.update();
            asset_occ_chart.update();
        }
}



    var load_assets = function(level, region, taxonomy) {
        $scope.info = false;
        $scope.error_info = false;

        if (level > 0 && region == undefined){
            return
        }
        else {
            $.ajax(BASE_URL+'/models/exposure/'+model_id+'/assets/?'+'level='+level+'&region='+region+'&taxonomy='+taxonomy )
            .done(function (data) {
                display_data(data);
            }).fail(function() {
                $scope.error_info = true;
                $scope.error_message = 'Error! Try again!';
            });
        }
    };



    var display_data = function(data) {

            model = data.model[0].fields;
            assets = data.assets;

            $scope.assets = assets;
            //$scope.$apply();

            fill_regions_dropdowns(level, data.regions)
            regions_control = new RegionSelectControl().addTo(map);

            if ( taxonomy == undefined ){

                $scope.disableAllTaxonomies = true;
                $scope.taxonomies = [];
                taxonomies = [];
                for (var i=0; i<data.taxonomies.length; i++){
                    taxonomies.push(data.taxonomies[i].fields.name);
                    $scope.taxonomies.push({id:data.taxonomies[i].pk, name: data.taxonomies[i].fields.name});
                }

            }
            else{
                $scope.disableAllTaxonomies = false;
            }

            $scope.$apply();


            //HANDSONTABLE

            colHeaders = ['<span class="glyphicon glyphicon-ok" aria-hidden="true"></span>', 'Asset', 'lat', 'lon', 'Taxonomy'];
            dataSchema = {id: null,
                            selected: null,
                            name: null,
                            lat: null,
                            lon: null,
                            taxonomy: null,
                            charts: null,
                            area: null,
                            n_buildings: null,
                            struct_cost: null,
                            retrofitting_cost: null,
                            struct_deductible: null,
                            struct_insurance_limit: null,
                            non_struct_cost: null,
                            non_struct_deductible: null,
                            non_struct_insurance_limit: null,
                            contents_cost: null,
                            contents_deductible: null,
                            contents_insurance_limit: null,
                            business_int_cost: null,
                            business_int_deductible: null,
                            business_int_insurance_limit: null,
                            oc_day: null,
                            oc_night: null,
                            oc_transit: null,
                        };
            columns = [
                  //{data: 'id'},
                  {data: 'selected', 
                    type: 'checkbox',},
                  {data: 'name'},
                  {data: 'lat',
                    type: 'numeric',
                    format: '0.00'},
                  {data: 'lon',
                    type: 'numeric',
                    format: '0.00'},
                  {data: 'taxonomy',
                        type: 'dropdown',
                        source: taxonomies
                    }
                ];
            

            var asset_chart_data = {
                labels: [],
                datasets: [],
            }

            if ($scope.stack){
                if ( model.insurance_limit ){
                    asset_chart_data.datasets.push({
                        fillColor: "rgba(125,150,255,0.5)",
                        strokeColor: "rgba(125,150,255,0.8)",
                        highlightFill: "rgba(125,150,255,0.75)",
                        highlightStroke: "rgba(125,150,255,1)",
                        data: []
                    });
                }
            }
            
            asset_chart_data.datasets.push({
                fillColor: "rgba(255,0,0,0.5)",
                strokeColor: "rgba(255,0,0,0.8)",
                highlightFill: "rgba(255,0,0,0.75)",
                highlightStroke: "rgba(255,0,0,1)",
                data: []
            });

            if ($scope.stack){

                if ( model.deductible ){
                    asset_chart_data.datasets.push({
                        fillColor: "rgba(125,150,255,0.5)",
                        strokeColor: "rgba(125,150,255,0.8)",
                        highlightFill: "rgba(125,150,255,0.75)",
                        highlightStroke: "rgba(125,150,255,1)",
                        data: []
                    });
                }
            }


            if ( model.area_type ){
                colHeaders.push('Area '+model.area_type+' <br> ('+model.area_unit+')');
                //dataSchema.area = null;
                columns.push({data: 'area',
                                type: 'numeric',
                                format: '0.00'});
            }

            if ( model.struct_cost_type == 'per_area' || model.non_struct_cost_type == 'per_area' || model.contents_cost_type == 'per_area' || model.business_int_cost_type == 'per_area' || model.struct_cost_type == 'per_unit' || model.non_struct_cost_type == 'per_unit' || model.contents_cost_type == 'per_unit' || model.business_int_cost_type == 'per_unit' ){
                colHeaders.push('Number <br> of units');
                //dataSchema.n_buildings = null;
                columns.push({data: 'n_buildings',
                                type: 'numeric',
                                format: '0'});
            }



            if ( model.struct_cost_type ){

                asset_chart_data.labels.push('Structural');
                asset_chart_data.labels.push('Retrofit');

                colHeaders.push('Structural cost <br>'+model.struct_cost_type+' ('+model.struct_cost_currency+')' );
                colHeaders.push('Retrofit cost <br>'+model.struct_cost_type+' ('+model.struct_cost_currency+')' );
                //dataSchema.struct_cost = null;
                //dataSchema.retrofitting_cost = null;

                if (model.struct_cost_currency == 'USD'){
                    //var language = 'en';
                    var format = '$ 0,0.00';
                }
                else if (model.struct_cost_currency == 'EUR'){
                    //var language = 'fr';
                    var format = '€ 0,0.00';
                }

                columns.push({data: 'struct_cost',
                                type: 'numeric',
                                format: format,
                                language: 'en' });
                columns.push({data: 'retrofitting_cost',
                                type: 'numeric',
                                format: format,
                                language: 'en' });
                
                if ( model.deductible ){
                    //dataSchema.struct_deductible = null;
                    if ( model.deductible == 'relative' ){
                        colHeaders.push('Structural deductible  <br>'+model.struct_cost_type+' (%)');
                        columns.push({data: 'struct_deductible',
                                    type: 'numeric',
                                    format: '0.00 %'});
                    }
                    else if ( model.deductible == 'absolute' ){
                        colHeaders.push('Structural deductible  <br>'+model.struct_cost_type+' ('+model.struct_cost_currency+')');
                        columns.push({data: 'struct_deductible',
                                    type: 'numeric',
                                    format: format,
                                    language: 'en' });
                    }
                }

                if ( model.insurance_limit ){
                    //dataSchema.struct_insurance_limit = null;
                    if ( model.insurance_limit == 'relative' ){
                        colHeaders.push('Structural insurance limit  <br>'+model.struct_cost_type+' (%)');
                        columns.push({data: 'struct_insurance_limit',
                                    type: 'numeric',
                                    format: '0.00 %'});
                    }
                    else if ( model.insurance_limit == 'absolute' ){
                        colHeaders.push('Structural insurance limit  <br>'+model.struct_cost_type+' ('+model.struct_cost_currency+')');
                        columns.push({data: 'struct_insurance_limit',
                                    type: 'numeric',
                                    format: format,
                                    language: 'en' });
                    }
                }

            }


            if ( model.non_struct_cost_type ){

                asset_chart_data.labels.push('Non structural');

                colHeaders.push('Non structural cost <br>'+model.non_struct_cost_type+' ('+model.non_struct_cost_currency+')' );
                //dataSchema.non_struct_cost = null;

                if (model.non_struct_cost_currency == 'USD'){
                    //var language = 'en';
                    var format = '$ 0,0.00';
                }
                else if (model.non_struct_cost_currency == 'EUR'){
                    //var language = 'fr';
                    var format = '€ 0,0.00';
                }

                columns.push({data: 'non_struct_cost',
                                type: 'numeric',
                                format: format,
                                language: 'en' });
                
                if ( model.deductible ){
                    //dataSchema.non_struct_deductible = null;
                    if ( model.deductible == 'relative' ){
                        colHeaders.push('Non structural deductible <br>'+model.non_struct_cost_type+' (%)');
                        columns.push({data: 'non_struct_deductible',
                                    type: 'numeric',
                                    format: '0.00 %'});
                    }
                    else if ( model.deductible == 'absolute' ){
                        colHeaders.push('Non structural deductible <br>'+model.non_struct_cost_type+' ('+model.non_struct_cost_currency+')');
                        columns.push({data: 'non_struct_deductible',
                                    type: 'numeric',
                                    format: format,
                                    language: 'en' });
                    }
                }

                if ( model.insurance_limit ){
                    //dataSchema.non_struct_insurance_limit = null;
                    if ( model.insurance_limit == 'relative' ){
                        colHeaders.push('Non structural insurance limit <br>'+model.non_struct_cost_type+' (%)');
                        columns.push({data: 'non_struct_insurance_limit',
                                    type: 'numeric',
                                    format: '0.00 %'});
                    }
                    else if ( model.insurance_limit == 'absolute' ){
                        colHeaders.push('Non structural insurance limit <br>'+model.non_struct_cost_type+' ('+model.non_struct_cost_currency+')');
                        columns.push({data: 'non_struct_insurance_limit',
                                    type: 'numeric',
                                    format: format,
                                    language: 'en' });
                    }
                }

            }

            if ( model.contents_cost_type ){

                asset_chart_data.labels.push('Contents');

                colHeaders.push('contents cost <br>'+model.contents_cost_type+' ('+model.contents_cost_currency+')' );
                //dataSchema.contents_cost = null;

                if (model.contents_cost_currency == 'USD'){
                    //var language = 'en';
                    var format = '$ 0,0.00';
                }
                else if (model.contents_cost_currency == 'EUR'){
                    //var language = 'fr';
                    var format = '€ 0,0.00';
                }

                columns.push({data: 'contents_cost',
                                type: 'numeric',
                                format: format,
                                language: 'en' });
                
                if ( model.deductible ){
                    //dataSchema.contents_deductible = null;
                    if ( model.deductible == 'relative' ){
                        colHeaders.push('Contents deductible <br>'+model.contents_cost_type+' (%)');
                        columns.push({data: 'contents_deductible',
                                    type: 'numeric',
                                    format: '0.00 %'});
                    }
                    else if ( model.deductible == 'absolute' ){
                        colHeaders.push('Contents deductible <br>'+model.contents_cost_type+' ('+model.contents_cost_currency+')');
                        columns.push({data: 'contents_deductible',
                                    type: 'numeric',
                                    format: format,
                                    language: 'en' });
                    }
                }

                if ( model.insurance_limit ){
                    //dataSchema.contents_insurance_limit = null;
                    if ( model.insurance_limit == 'relative' ){
                        colHeaders.push('Contents insurance limit <br>'+model.contents_cost_type+' (%)');
                        columns.push({data: 'contents_insurance_limit',
                                    type: 'numeric',
                                    format: '0.00 %'});
                    }
                    else if ( model.insurance_limit == 'absolute' ){
                        colHeaders.push('Contents insurance limit <br>'+model.contents_cost_type+' ('+model.contents_cost_currency+')');
                        columns.push({data: 'contents_insurance_limit',
                                    type: 'numeric',
                                    format: format,
                                    language: 'en' });
                    }
                }

            }

            if ( model.business_int_cost_type ){

                asset_chart_data.labels.push('Business Interruption');

                colHeaders.push('Business Interruption cost <br>'+model.business_int_cost_type+' ('+model.business_int_cost_currency+')' );
                //dataSchema.business_int_cost = null;

                if (model.business_int_cost_currency == 'USD'){
                    //var language = 'en';
                    var format = '$ 0,0.00';
                }
                else if (model.business_int_cost_currency == 'EUR'){
                    //var language = 'fr';
                    var format = '€ 0,0.00';
                }

                columns.push({data: 'business_int_cost',
                                type: 'numeric',
                                format: format,
                                language: 'en' });
                
                if ( model.deductible ){
                    //dataSchema.business_int_deductible = null;
                    if ( model.deductible == 'relative' ){
                        colHeaders.push('Business Interruption deductible <br>'+model.business_int_cost_type+' (%)');
                        columns.push({data: 'business_int_deductible',
                                    type: 'numeric',
                                    format: '0.00 %'});
                    }
                    else if ( model.deductible == 'absolute' ){
                        colHeaders.push('Business Interruption deductible <br>'+model.business_int_cost_type+' ('+model.business_int_cost_currency+')');
                        columns.push({data: 'business_int_deductible',
                                    type: 'numeric',
                                    format: format,
                                    language: 'en' });
                    }
                }

                if ( model.insurance_limit ){
                    //dataSchema.business_int_insurance_limit = null;
                    if ( model.insurance_limit == 'relative' ){
                        colHeaders.push('Business Interruption insurance limit <br> '+model.business_int_cost_type+' (%)');
                        columns.push({data: 'business_int_insurance_limit',
                                    type: 'numeric',
                                    format: '0.00 %'});
                    }
                    else if ( model.insurance_limit == 'absolute' ){
                        colHeaders.push('Business Interruption insurance limit <br> '+model.business_int_cost_type+' ('+model.business_int_cost_currency+')');
                        columns.push({data: 'business_int_insurance_limit',
                                    type: 'numeric',
                                    format: format,
                                    language: 'en' });
                    }
                }

            }

            colHeaders.push('Occupation <br> Day');
            //dataSchema.oc_day = null;
            columns.push({data: 'oc_day',
                            type: 'numeric',
                            format: '0.00'});

            colHeaders.push('Occupation <br> Night');
            //dataSchema.oc_night = null;
            columns.push({data: 'oc_night',
                            type: 'numeric',
                            format: '0.00'});

            colHeaders.push('Occupation <br> Transit');
            //dataSchema.oc_transit = null;
            columns.push({data: 'oc_transit',
                            type: 'numeric',
                            format: '0.00'});


            var clickedOnMap;

            if (table != undefined){
                table.destroy();
            }

    
            table = new Handsontable(container, {
                data: assets,
                dataSchema: dataSchema,
                startRows: 5,
                //startCols: 4,
                colHeaders: colHeaders,
                columns: columns,
                fixedColumnsLeft: 2,
                minSpareRows: 1,
                currentRowClassName: 'currentRow',
                manualColumnResize: true,
                //columnSorting: true,
                /*cells: function (row, col, prop) {
                    var cellProperties = {};
                    if (prop == 'selected'){
                        cellProperties.renderer = 'selectRow';
                    }
                    return cellProperties;
                },*/
                beforeOnCellMouseDown: function(cell){
                    clickedOnMap = false;
                },
                /*
                afterLoadData: function() {
                    if (assetsTags != undefined){

                        var currentTags = assetsTags.getTags();
                        console.log(currentTags);
                        //var reload = false;
                        for (var j = 0; currentTags.length; j++ ){
                            for(var i=0; i<assets.length; i++){

                                if (assets[i].name == currentTags[j]){
                                    //reload = true;
                                    assets[i].selected = true;
                                }
                            };
                        }
                        //if (reload){
                        //    table.loadData(assets);
                        //}
                    }
                },*/
                afterSelection: function(cell){

                    if (clickedOnMap == false){
                       
                        try{
                            var physicalIndex = this.sortIndex[cell][0];
                        }
                        catch(err){
                            var physicalIndex = cell;
                        }

                        try{

                            var marker = markerList[physicalIndex];
                            map.setView( marker.getLatLng(), 12 );
                            marker.openPopup();
        
                            $scope.asset_name = assets[physicalIndex].name;
                            $scope.$apply();
                            if ($scope.stack){
                                draw_stacked_charts(model, assets[physicalIndex], asset_chart_data);                                
                            }
                            else {
                                draw_charts(assets[physicalIndex], asset_chart_data);
                            }

                        }
                        catch(err){
                            console.log(err);
                            $scope.asset_name = 'Select an asset';
                            $scope.$apply();
                            asset_chart.destroy();
                            asset_occ_chart.destroy();
                            //return;
                        }
                    }


                },
                afterChange: function (change, source) {

                    if (source === 'loadData') {
                        return; //don't save this change
                    }

                    
                    if (change[0][1] == 'lat' ){
                        try{

                            var marker = markerList[change[0][0]];
                            marker.setLatLng([ change[0][3], marker.getLatLng().lng ]);

                            //markerList[change[0][0]] = marker;

                            map.setView([ change[0][3], marker.getLatLng().lng ])
                            marker.openPopup();
                        }
                        catch(err){
                            console.log('New asset');
                        }
                    }

                    if (change[0][1] == 'lon' ){
                        try{

                            var marker = markerList[change[0][0]];
                            marker.setLatLng([ marker.getLatLng().lat, change[0][3] ]);

                            //markerList[change[0][0]] = marker;

                            map.setView([ marker.getLatLng().lat, change[0][3],  ]);
                            marker.openPopup();
                        }
                        catch(err){
                            console.log('New asset');
                        }
                    }

                    if (change[0][1] == 'name' ){
                        try{
                            var marker = markerList[change[0][0]];
                            marker.bindPopup(change[0][3]);
                            marker.openPopup();
                        }
                        catch(err){
                            console.log('New asset');
                        }
                    }

                    if (change[0][1] == 'selected' ){
                        var asset = assets[change[0][0]];
                        if (change[0][3]){
                            //$scope.selectedAssets.push(asset);
                            assetsTags.addTag(asset.name)
                        }
                        else {
                            assetsTags.removeTag(asset.name)
                            //for (var i=0; i<$scope.selectedAssets.length;i++){
                            //    if ( $scope.selectedAssets[i].name == asset.name ){
                                    //$scope.selectedAssets.splice(i, 1);
                            //    }
                            //}
                        }
                        return;
                    }

                    $scope.disableSave = false; 
                    $scope.$apply();

                },
            });


            var matchMarkerTable = function(){
                    clickedOnMap = true;

                    var index = markerList.indexOf(this);

                    try{
                        var physicalIndex = table.sortIndex[index][0];
                    }
                    catch(err){
                        var physicalIndex = index;
                    }

                    table.selectCell(physicalIndex, 0);

                    $scope.asset_name = assets[index].name;
                    $scope.$apply();
                    if ($scope.stack){
                        draw_stacked_charts(model, assets[index], asset_chart_data);
                    }
                    else {
                        draw_charts(assets[index], asset_chart_data);
                    }
                }


            //MAP
            //if (markers != undefined) {
            //    map.removeLayer(markers);
            //}

            markerList = [];
            markers.clearLayers();


            map.on('draw:created', function (e) {
                var type = e.layerType,
                    marker = e.layer;
                
                markers.addLayer(marker);
                markerList.push(marker);
                marker.bindPopup(assets[assets.length-1].name);

                marker.on('click', matchMarkerTable);

                assets[assets.length-1].lat = marker.getLatLng().lat;
                assets[assets.length-1].lon = marker.getLatLng().lng;
                table.loadData(assets);
                table.selectCell(assets.length-1, 0)
                $scope.disableSave = false;
                $scope.$apply(); 
            });


            map.on('draw:edited', function (e) {
                var layers = e.layers;
                layers.eachLayer(function (layer) {
                    var index = markerList.indexOf(layer);
                    assets[index].lat = layer.getLatLng().lat;
                    assets[index].lon = layer.getLatLng().lng;
                });
                table.loadData(assets);
                $scope.disableSave = false;
                $scope.$apply(); 
            });

            map.on('draw:deleted', function (e) {
                var layers = e.layers;
                layers.eachLayer(function (layer) {
                    var index = markerList.indexOf(layer);
                    assets.splice(index, 1);
                });
                table.loadData(assets);
                $scope.disableSave = false;        
                $scope.$apply();        
            });


            var tags_sugestions = []
            for(var i=0; i<assets.length; i++){

                if (assets[i].lat != null){

                    var marker = L.marker(L.latLng(assets[i].lat, assets[i].lon));
                    marker.bindPopup(assets[i].name);
                    markerList.push(marker);

                    marker.on('click', matchMarkerTable);
                    tags_sugestions.push(assets[i].name);

                }
            };

            try {
                markers.addLayers(markerList);
                map.addLayer(markers);
                control.addOverlay(markers, 'Assets');

                map.fitBounds(markers);
            }
            catch(err) {
                console.log('Add assets');
            }


            assetsTags = $('#assets-tag-list').tags({
                suggestions:tags_sugestions,
                restrictTo: tags_sugestions,
                tagClass: 'btn-primary',
                promptText: 'Enter assets',
                afterAddingTag: function(tag){
                    for (var i=0; i<assets.length;i++){
                        if ( assets[i].name == tag ){
                            assets[i].selected = true;
                            table.loadData(assets);

                            var marker = markerList[i];
                            map.setView( marker.getLatLng(), 12 );
                            marker.openPopup();
        
                            $scope.asset_name = assets[i].name;
                            $scope.disableDelete = false;
                            $scope.$apply();
                            //draw_charts(assets[i], asset_chart_data);
                            if ($scope.stack){
                                draw_stacked_charts(model, assets[i], asset_chart_data);
                            }
                            else {
                                draw_charts(assets[i], asset_chart_data);
                            }
                        }
                    }
                },
                afterDeletingTag: function(tag){
                    for (var i=0; i<assets.length;i++){
                        if ( assets[i].name == tag ){
                            assets[i].selected = false;
                            table.loadData(assets);
                        }
                    }
                    var tags = this.getTags();
                    if (tags.length == 0){
                        $scope.disableDelete = true;
                        $scope.$apply();
                    }
                },
            });

            var existingTags = assetsTags.getTags();
            for (var i=0; i< existingTags.length; i++){
                assetsTags.removeTag(existingTags[i]);
            }


        } 



    load_assets(level, region, taxonomy);

});


            /*
            function selectRow(instance, td, row, col, prop, value, cellProperties) {
                Handsontable.renderers.TextRenderer.apply(this, arguments);

                $(td).html('<input type="checkbox">')

                if (prop == 'selected' ){
                    console.log(value);
                    if (value = false){
                        td.style.background = '#FFFFBF';
                    }
                    else {
                        td.style.background = '#FFFFFF';
                    }
                }
            }

            Handsontable.renderers.registerRenderer('selectRow', selectRow);
            */

 /*renderer: function (instance, td, row, col, prop, value, cellProperties) {
                        Handsontable.CheckboxCell.renderer.apply(this, arguments);
                        var asset = assets[row];
                        asset.text = asset.name;


                        if (value === true) {
                            $scope.selectedAssets.push(asset);
                            $scope.$apply();
                            console.log($scope.selectedAssets);
                        }
                        else {
                            var index = $scope.selectedAssets.indexOf(asset);
                            $scope.selectedAssets.splice(index, 1);
                            $scope.$apply();
                            console.log($scope.selectedAssets);
                        }


                    }*/


                    /*renderer: function (instance, td, row, col, prop, value, cellProperties) {
                        Handsontable.CheckboxCell.renderer.apply(this, arguments);
                        var asset = assets[row];

                        this.on('click', function(){
                            console.log(asset);
                        });

                        if (value === true) {
                            //charts_assets.push(asset);
                            //draw_charts_v2();
                        }
                        else {

                            //var index = charts_assets.indexOf(asset);
                            //if (index > -1) {
                            //    charts_assets.splice(index, 1);
                            //    draw_charts_v2();
                            //}

                        }

                    }*/

/*
 var draw_charts_v2 = function(){

        var asset_chart;

        for (var i=0; i < charts_assets.length; i++ ){

            var ast = {
                label: charts_assets[i].name,
                fillColor: "rgba(220,220,220,0.5)",
                strokeColor: "rgba(220,220,220,0.8)",
                highlightFill: "rgba(220,220,220,0.75)",
                highlightStroke: "rgba(220,220,220,1)",
                data: []
            }


            if (charts_assets[i].struct_cost){
                ast.data.push(charts_assets[i].struct_cost);

                if (charts_assets[i].retrofitting_cost){
                    ast.data.push(charts_assets[i].retrofitting_cost);
                }
                else {
                    ast.data.push(0);
                }
            }

            if (charts_assets[i].non_struct_cost){
                ast.data.push(charts_assets[i].struct_cost);
            }
            if (charts_assets[i].contents_cost){
                ast.data.push(charts_assets[i].contents_cost);
            }
            if (charts_assets[i].business_int_cost){
                ast.data.push(charts_assets[i].business_int_cost);
            }

        }

        asset_chart_data.datasets.push(ast);

        asset_chart = new Chart(ctx).Bar(asset_chart_data, {responsive: true,
                                                            maintainAspectRatio: false,});
    }
*/