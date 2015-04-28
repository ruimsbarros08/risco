    

var get_hazard = function(hazard_job_id){

    $.ajax( '/jobs/scenario/hazard/results_ajax/'+hazard_job_id )
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
            });

            return geoJsonTileLayer
        }
    });
}