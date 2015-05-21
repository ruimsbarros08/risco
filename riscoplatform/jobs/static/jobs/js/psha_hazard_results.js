 "use strict";

(function($) {
$( document ).ready(function() {
    
    var map = new L.Map('map', {
        fullscreenControl: true,
        fullscreenControlOptions: {
            position: 'topleft'
        }
    });
    map.setView(new L.LatLng(0, 0),2);
    bw.addTo(map);

    var control = L.control.layers(baseLayers).addTo(map);

    var url = document.URL.split('/');
    var job_id = url[url.length -2];

});
})($); 