"use strict";

var sitesApp = angular.module('sitesApp', []).config(function($interpolateProvider){
    $interpolateProvider.startSymbol('[[').endSymbol(']]');
});

sitesApp.controller('sitesCtrl', function($scope) {

    var map = new L.Map('map', {
        fullscreenControl: true,
        fullscreenControlOptions: {
            position: 'topleft'
        }
    });
    map.setView(new L.LatLng(0, 0),2);
    osm.addTo(map);

    var control = L.control.layers(baseLayers).addTo(map);

    var info = L.control({position: 'bottomleft'});
    info.onAdd = function (map) {
        this._div = L.DomUtil.create('div', 'info');
        return this._div;
    };
    info.update = function (props) {
        this._div.innerHTML = '<h4>INFO</h4>' +  (props ?
            '<b>vs30: </b>' + props.vs30 + ' m/s <br>'
            : 'Hover the map');
    };
    info.addTo(map);

    var style = {
        "color": "#00D",
        "weight": 0.1,
        "opacity": 0.3,
        "fillOpacity": 0.4
    };
    var hoverStyle = {
        "fillOpacity": 0.6
    };

    var url = document.URL.split('/');
    var model_id = url[url.length -2];


    $.ajax('/models/site/'+model_id+'/map_grid' )
    .done(function(data) {
        var geoJsonTileLayer = L.geoJson(data, {
        style: style,
        onEachFeature: function (feature, layer) {
            //layer.setStyle({"fillColor": feature.properties.color});
            layer.on('mouseover', function () {
                info.update(layer.feature.properties);
                layer.setStyle(hoverStyle);
            });
            layer.on('mouseout', function () {
                info.update();
                layer.setStyle(style);
            });
        }
    }).addTo(map);

    map.fitBounds( geoJsonTileLayer.getBounds() );


    })
    .fail(function() {
        alert( "error" );
    })
    .always(function() {
        //alert( "complete" );
    });



});

// (function($) {
// $( document ).ready(function() {

//     var map = new L.Map('map', {
//         fullscreenControl: true,
//         fullscreenControlOptions: {
//             position: 'topleft'
//         }
//     });
//     map.setView(new L.LatLng(0, 0),2);
//     osm.addTo(map);

//     var control = L.control.layers(baseLayers).addTo(map);

// 	var info = L.control({position: 'bottomleft'});
//     info.onAdd = function (map) {
//         this._div = L.DomUtil.create('div', 'info');
//         return this._div;
//     };
//     info.update = function (props) {
//         this._div.innerHTML = '<h4>INFO</h4>' +  (props ?
//             '<b>vs30: </b>' + props.vs30 + ' m/s <br>'
//             : 'Hover the map');
//     };
//     info.addTo(map);

//     var style = {
//         "color": "#00D",
//         "weight": 0.1,
//         "opacity": 0.3,
//         "fillOpacity": 0.4
//     };
//     var hoverStyle = {
//         "fillOpacity": 0.6
//     };

//     var url = document.URL.split('/');
//     var model_id = url[url.length -2];


// 	$.ajax('/models/site/'+model_id+'/map_grid' )
// 	.done(function(data) {
//     	var geoJsonTileLayer = L.geoJson(data, {
//         style: style,
//         onEachFeature: function (feature, layer) {
//             //layer.setStyle({"fillColor": feature.properties.color});
//             layer.on('mouseover', function () {
//                 info.update(layer.feature.properties);
//                 layer.setStyle(hoverStyle);
//             });
//             layer.on('mouseout', function () {
//                 info.update();
//                 layer.setStyle(style);
//             });
//         }
//     }).addTo(map);

//     map.fitBounds( geoJsonTileLayer.getBounds() );


// 	})
// 	.fail(function() {
// 	    alert( "error" );
// 	})
// 	.always(function() {
// 	    //alert( "complete" );
// 	});




// });
// })($); 