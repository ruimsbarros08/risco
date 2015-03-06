 "use strict";

(function($) {
$( document ).ready(function() {


    var map = new L.Map('map');
    var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
    var osmAttrib='Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
    var osm = new L.TileLayer(osmUrl, {minZoom: 3, maxZoom: 16, attribution: osmAttrib});

    map.setView(new L.LatLng(40, -8),5);
    map.addLayer(osm);


    var style = {
        //"color": "#00D",
        "weight": 0.1,
        "opacity": 1.0,
        "fillOpacity": 0.0
    };
    var hoverStyle = {
        "fillOpacity": 0.3
    };

    var url = document.URL.split('/');
    var model_id = url[url.length -2];

    var geoJsonURL = BASE_URL+'models/exposure/'+model_id+'/tiles/{z}/{x}/{y}';
    var geoJsonTileLayer = new L.TileLayer.GeoJSON(geoJsonURL, {
            clipTiles: true,
            unique: function (feature) {
                return feature.id; 
            }
        }, {
            style: style,
            onEachFeature: function (feature, layer) {
                //layer.setStyle({'color': feature.properties.color})
                //if (feature.properties) {
                //    layer.setStyle(style);
                //}
                layer.on('mouseover', function () {
                    layer.setStyle(hoverStyle);
                    //infoBox.update(layer.feature.properties);
                });
                layer.on('mouseout', function () {
                    layer.setStyle(style);
                    //infoBox.update();
                });
                layer.on('click', function () {
                    layer.bindPopup("<b>Number of assets: </b><br>"+feature.properties.n_assets).openPopup();
                });
            }
        }
    ).addTo(map);



});
})($);