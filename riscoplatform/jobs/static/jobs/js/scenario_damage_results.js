 "use strict";

(function($) {
$( document ).ready(function() {
    
	var map = new L.Map('map');
	var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
	var osmAttrib='Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
	var osm = new L.TileLayer(osmUrl, {minZoom: 3, maxZoom: 16, attribution: osmAttrib});

	map.setView(new L.LatLng(40, -8),5);
	map.addLayer(osm);


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
        //"color": "#00D",
        "weight": 0.1,
        "opacity": 0.3,
        "fillOpacity": 0.4
    };
    var hoverStyle = {
        "fillOpacity": 0.6
    };

    var url = document.URL.split('/');
    var job_id = url[url.length -2];

    var geoJsonURL = BASE_URL+'jobs/scenario/damage/results/'+job_id+'/tiles/{z}/{x}/{y}';
    var geoJsonTileLayer = new L.TileLayer.GeoJSON(geoJsonURL, {
            clipTiles: true,
            unique: function (feature) {
                return feature.id; 
            }
        }, {
            style: style,
            onEachFeature: function (feature, layer) {
                layer.setStyle({'color': feature.properties.color})
                //if (feature.properties) {
                //    layer.setStyle(style);
                //}
                if (!(layer instanceof L.Point)) {
                    layer.on('mouseover', function () {
                        layer.setStyle(hoverStyle);
                        //infoBox.update(layer.feature.properties);
                    });
                    layer.on('mouseout', function () {
                        layer.setStyle(style);
                        //infoBox.update();
                    });
                    layer.on('click', function () {
                        console.log(feature)
                    });
                }
            }
        }
    ).addTo(map);


});
})($); 