 "use strict";

(function($) {
$( document ).ready(function() {

    //TO DO 

    // * click on hazard cell and get markers
    
    var map = new L.Map('map');
    map.setView(new L.LatLng(0, 0),2);
    bw.addTo(map);

    var control = L.control.layers(baseLayers).addTo(map);

    var url = document.URL.split('/');
    var job_id = url[url.length -2];
    
    var legendControl;
    legendControl = new L.Control.Legend();
    legendControl.addTo(map);


////////////////
//   HAZARD   //
////////////////

    var cells;
    var hazard_data;
    var hazardLayer;
    var hazard_options;

    var epicenter;
    var rupture;
    var rupture_info;

    var job;

    $.ajax( BASE_URL+'/jobs/scenario/hazard/results_ajax/'+job_id )
    .done(function(data) {

        job = data.job[0].fields;

        cells = data.geojson;
        hazard_data = data.hazard;
        
        hazard_options = get_hazard_options(cells);
        rupture_info = data.rupture.info[0].fields;

        epicenter = L.geoJson(data.rupture.epicenter, {
            pointToLayer: function (feature, latlng) {
                var marker = L.marker(latlng, {icon: epicenterIcon});
                marker.bindPopup('<b><h4>Epicenter</h4></b>'+
                                ' <br> <b> Magnitude: </b>'+Humanize.formatNumber(rupture_info.magnitude, 2)+
                                ' <br> <b> Latitude: </b>'+Humanize.formatNumber(latlng.lat, 2)+' º'+
                                ' <br> <b> Longitude: </b>'+Humanize.formatNumber(latlng.lng, 2)+' º'+
                                ' <br> <b> Depth: </b>'+Humanize.formatNumber(rupture_info.depth, 2)+' km'+
                                ' <br> <b> Rake: </b>'+Humanize.formatNumber(rupture_info.rake, 2)+' º');
                return marker;
            }
        }).addTo(map);
        control.addOverlay(epicenter, 'Epicenter');

        if ( data.rupture.rupture ){
            rupture = L.geoJson(data.rupture.rupture, {}).addTo(map);
            rupture.bindPopup('<b><h4>Simple fault rupture</h4></b>'+
                                    ' <br> <b> Dip: </b>'+Humanize.formatNumber(rupture_info.dip, 2)+' º'+
                                    ' <br> <b> Upper seismo depth: </b>'+Humanize.formatNumber(rupture_info.upper_depth, 2)+' km'+
                                    ' <br> <b> Lower seismo depth: </b>'+Humanize.formatNumber(rupture_info.lower_depth, 2)+' km');
            control.addOverlay(rupture, 'Rupture');
        }

        if ( job.status == 'FINISHED' ){

            for (var i = 0; i<hazard_data.length; i++){

                hazard_options.onEachRecord = function(layer, record){
                    layer.on('click', function () {
                        console.log(record);
                    });
                }

                hazardLayer = new L.ChoroplethDataLayer(hazard_data[i], hazard_options);

                if ( i == 0){
                    hazardLayer.addTo(map);
                }

                control.addOverlay(hazardLayer ,hazard_data[i].name);
                map.fitBounds(hazardLayer.getBounds());

            }
        }

    });


});
})($); 