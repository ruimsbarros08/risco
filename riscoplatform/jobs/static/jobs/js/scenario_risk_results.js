 "use strict";

(function($) {
$( document ).ready(function() {

    get_world();

    $( "#vulnerability-selector li:first-child" ).addClass( "active" );
    $( "#myTabContent div:first-child" ).addClass( "tab-pane fade active in" );

    //hide-show    
    $( "label[for='region']" ).hide( "fast");

    var map = new L.Map('map');
    map.setView(new L.LatLng(40, -8),5);
    osm.addTo(map);

    //L.control.layers(baseMaps).addTo(map);

	map.setView(new L.LatLng(40, -8),5);
	map.addLayer(osm);

    var hazard_url = $('#hazard_id').attr("href").split('/');
    var hazard_job_id = hazard_url[hazard_url.length -2];

    
    var control = L.control.layers().addTo(map);
    

    var info = L.control({position: 'bottomleft'});
    info.onAdd = function (map) {
        this._div = L.DomUtil.create('div', 'info');
        return this._div;
    };
    info.update = function (props) {
        this._div.innerHTML = '<h4>INFO</h4>' +  (props ?
            '<b>a: </b>' + props.a + ' g m/s<sup>2</sup> <br>'
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
            }).addTo(map);

            control.addBaseLayer(geoJsonTileLayer, data.hazard[i].name);
            map.fitBounds(geoJsonTileLayer.getBounds());
        }
    });


    var url = document.URL.split('/');
    var job_id = url[url.length -2];

    var get_losses = function(country, adm1){
        $.ajax( '/jobs/scenario/risk/results_per_region/'+job_id+'?'+'&country='+country+'&adm1='+adm1 )
        .done(function(data) {
            for (var i = 0; i<data.results.length;i++) {
                $('#'+data.results[i].type+'_region_total').text(data.results[i].total);
            }

            /*
            if (data.region != null){
                geoJsonTileLayer_losses = L.geoJson(data.region).addTo(map);
            }

            if (geoJsonTileLayer_losses == undefined){
                control.addBaseLayer(geoJsonTileLayer_losses, 'Region selected');
                map.fitBounds(geoJsonTileLayer_losses.getBounds());
            }
*/
        });
    }

    var country = undefined;
    var adm1 = undefined;
    //var geoJsonTileLayer_losses= undefined;
    get_losses(country, adm1);

    $('#country').on('change', function(){
        country = $(this).val();
        get_losses(country, adm1);
        //load_assets(page, country, adm1);
    });

    $('#level1').on('change', function(){
        adm1 = $(this).val();
        get_losses(country, adm1);
        //load_assets(page, country, adm1);
    });

        /*
    var losses_style = {
        //"color": "#00D",
        "weight": 0.1,
        "opacity": 0.3,
        "fillOpacity": 0.4
    };
    var hover_losses_style = {
        "fillOpacity": 0.6
    };
    
    var geoJsonURL = 'http://localhost:8080/world/{z}/{x}/{y}.json';
    var losses_geoJsonTileLayer = new L.TileLayer.GeoJSON(geoJsonURL, {
        clipTiles: true,
        unique: function (feature) {
            return feature.id; 
        }
    }, {
        style: style,
        onEachFeature: function (feature, layer) {
            layer.setStyle({'color': feature.properties.color})
            layer.on('mouseover', function () {
                layer.setStyle(hover_losses_style);
                //infoBox.update(layer.feature.properties);
            });
            layer.on('mouseout', function () {
                layer.setStyle(losses_style);
                //infoBox.update();
            });
            layer.on('click', function () {
                updateChart(feature.properties.limit_states)
            });
        }
    }).addTo(map);

    control.addBaseLayer(losses_geoJsonTileLayer, 'Losses');
    */

});
})($); 