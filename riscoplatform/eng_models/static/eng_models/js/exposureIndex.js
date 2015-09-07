"use strict";

var exposureIndexApp = angular.module('exposureIndexApp', []).config(function($interpolateProvider){
    $interpolateProvider.startSymbol('[[').endSymbol(']]');
});

exposureIndexApp.controller('exposureIndexCtrl', function($scope) {

    var map = init_map();
    map.scrollWheelZoom.disable();

    var load_countries = function() {

        $.ajax(BASE_URL+'/models/exposure/countries/')
        .done(function (data) {

            L.geoJson(data.countries, {

                style: {
                        "color": "#ff0000",
                        "weight": 1,
                        "opacity": 0.75
                },

                onEachFeature: function(feature, layer){

                    var models_str = '';

                    for (var i=0; i < feature.properties.models.length; i++){
                        models_str += '<li><a href="'+BASE_URL+'/models/exposure/'+feature.properties.models[i].id+'">'+feature.properties.models[i].name+'</a><li>'
                    }

                    var content = '<h3>'+feature.properties.name+' <img src="/static/img/flags/'+feature.properties.name+'.png" alt="country"> </h3>\
                                    <p><b>Number of models: </b>'+feature.properties.models.length+'</p>\
                                    <p><b>Number of assets: </b>'+feature.properties.n_assets+'</p>\
                                    <p><b>Models: </b><ul class="no-bullets">'+models_str+'</ul></p>'
                    layer.bindPopup(content);
                },

            }).addTo(map);



        }).fail(function() {

        });
    };

    load_countries();


});

