 "use strict";

(function($) {
$( document ).ready(function() {
    
	var map = new L.Map('map');
	var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
	var osmAttrib='Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
	var osm = new L.TileLayer(osmUrl, {minZoom: 3, maxZoom: 16, attribution: osmAttrib});

	map.setView(new L.LatLng(40, -8),5);
	map.addLayer(osm);
    L.control.layers(baseMaps).addTo(map);


    var info = L.control({position: 'bottomleft'});
    info.onAdd = function (map) {
        this._div = L.DomUtil.create('div', 'info');
        return this._div;
    };
    info.update = function (props) {
        this._div.innerHTML = '<h4>INFO</h4>' +  (props ?
            '<b>a: </b>' + props.a + ' m/s<sup>2</sup> <br>'
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
    var job_id = url[url.length -2];

    
    var control = L.control.layers().addTo(map);
    
    $.ajax( '/jobs/scenario/hazard/results_ajax/'+job_id )
    .done(function(data) {
        for (var i = 0; i<data.hazard.length;i++) {

            var geoJsonTileLayer = L.geoJson(data.hazard[i], {
                style: style,
                onEachFeature: function (feature, layer) {
                    layer.setStyle({"fillColor": feature.properties.color});
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

            control.addBaseLayer(geoJsonTileLayer, data.hazard[i].name);

        }

        var ruptureLayer = L.geoJson(data.rupture, {
        //style: style,
        onEachFeature: function (feature, layer) {
            //layer.setStyle({"fillColor": feature.properties.color});
            layer.on('click', function () {
                //info.update(layer.feature.properties);
                //layer.setStyle(hoverStyle);
            });
        }
    }).addTo(map);

    control.addOverlay(ruptureLayer, 'Rupture')

    })
    .fail(function() {
        alert( "ERROR: The results are not in the database" );
    })
    .always(function() {
        //alert( "complete" );
    });


});
})($); 