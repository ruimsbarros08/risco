 "use strict";

(function($) {
$( document ).ready(function() {

    var map = new L.Map('map');
    map.setView(new L.LatLng(40, -8),5);
    osm.addTo(map);
    L.control.layers(baseMaps).addTo(map);

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


	$.ajax( BASE_URL+'models/site/'+model_id+'/map_grid' )
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
	})
	.fail(function() {
	    alert( "error" );
	})
	.always(function() {
	    //alert( "complete" );
	});




});
})($); 