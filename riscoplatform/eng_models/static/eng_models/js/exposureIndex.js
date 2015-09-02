"use strict";

var exposureIndexApp = angular.module('exposureIndexApp', []).config(function($interpolateProvider){
    $interpolateProvider.startSymbol('[[').endSymbol(']]');
});

exposureIndexApp.controller('exposureIndexCtrl', function($scope) {


    $( "label[for='tax_source_name']" ).hide();
    $( "#id_tax_source_name" ).hide();
    $( "label[for='tax_source_desc']" ).hide();
    $( "#id_tax_source_desc" ).hide();
    $('#id_add_tax_source').change( function() {
        if ($(this).is(":checked")){
            $( "label[for='tax_source_name']" ).show( "fast");
            $( "#id_tax_source_name" ).show( "fast");
            $( "label[for='tax_source_desc']" ).show( "fast");
            $( "#id_tax_source_desc" ).show( "fast");
        }
        else {
            $( "label[for='tax_source_name']" ).hide( "fast");
            $( "#id_tax_source_name" ).hide( "fast");
            $( "label[for='tax_source_desc']" ).hide( "fast");
            $( "#id_tax_source_desc" ).hide( "fast");
        }
    });


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
                        models_str += '<li><a href="/models/exposure/'+feature.properties.models[i].id+'">'+feature.properties.models[i].name+'</a><li>'
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

