 "use strict";

(function($) {
$( document ).ready(function() {

    //map.on('map:loadfield', function (e) {
        // Customize map for field
    //    console.log(e.field, e.fieldid);
    //});
    /*
	var map = new L.Map('id_geom_map');
	var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
	var osmAttrib='Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
	var osm = new L.TileLayer(osmUrl, {minZoom: 3, maxZoom: 16, attribution: osmAttrib});

	map.setView(new L.LatLng(40, -8),5);
	map.addLayer(osm);

    // Initialise the FeatureGroup to store editable layers
    var drawnItems = new L.FeatureGroup();
    map.addLayer(drawnItems);

    var polylineOptions = {
                allowIntersection: false,
                shapeOptions: {
                    color: '#f00',
                    weight: 3
                }
            };

    // Initialise the draw control and pass it the FeatureGroup of editable layers
    var drawControl = new L.Control.Draw({
        edit: {
            featureGroup: drawnItems,
            //edit: false,
            //remove: false
        },
        draw: {
            polyline: polylineOptions,
            polygon: false,
            rectangle: false,
            circle: false,
            marker: false
        }
    });
    map.addControl(drawControl);


    map.on('draw:created', function (e) {
        var type = e.layerType,
            layer = e.layer;

        // Do whatever else you need to. (save to db, add to map etc)
        drawnItems.addLayer(layer);
    });


    map.on('draw:edited', function (e) {
        var layers = e.layers;
        layers.eachLayer(function (layer) {
            //do whatever you want, most likely save back to db
        });
    });

    map.on('draw:deleted', function (e) {
        var layers = e.layers;
        layers.eachLayer(function (layer) {
            //do whatever you want, most likely save back to db
        });
    });



    /*
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


    */

});
})($);