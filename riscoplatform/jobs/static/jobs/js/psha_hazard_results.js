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

    var url = document.URL.split('/');
    var job_id = url[url.length -2];

});
})($); 