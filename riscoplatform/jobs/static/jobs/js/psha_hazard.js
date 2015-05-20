 "use strict";

(function($) {
$( document ).ready(function() {

    //hide-show    
    $( "label[for='region']" ).hide( "fast");

    $( "label[for='site_model']" ).hide( "fast");
    $( "#id_site_model" ).hide( "fast");
    $('#id_sites_type').on('change', function() {
        if (this.value == 'VARIABLE_CONDITIONS'){
            $( "label[for='vs30']" ).hide( "fast", 'swing');
            $( "#id_vs30" ).hide( "fast", 'swing');
            $( "label[for='vs30type']" ).hide( "fast", 'swing');
            $( "#id_vs30type" ).hide( "fast", 'swing');
            $( "label[for='z1pt0']" ).hide( "fast", 'swing');
            $( "#id_z1pt0" ).hide( "fast", 'swing');
            $( "label[for='z2pt5']" ).hide( "fast", 'swing');
            $( "#id_z2pt5" ).hide( "fast", 'swing');

            $( "label[for='site_model']" ).show( "fast", 'swing');
            $( "#id_site_model" ).show( "fast", 'swing');
        }
        else {
            $( "label[for='vs30']" ).show( "fast", 'swing');
            $( "#id_vs30" ).show( "fast", 'swing');
            $( "label[for='vs30type']" ).show( "fast", 'swing');
            $( "#id_vs30type" ).show( "fast", 'swing');
            $( "label[for='z1pt0']" ).show( "fast", 'swing');
            $( "#id_z1pt0" ).show( "fast", 'swing');
            $( "label[for='z2pt5']" ).show( "fast", 'swing');
            $( "#id_z2pt5" ).show( "fast", 'swing');

            $( "label[for='site_model']" ).hide( "fast", 'swing');
            $( "#id_site_model" ).hide( "fast", 'swing');

        }
    });


    $('fieldset').append('<div class="form-group" id="imt-l-selection"> \
                            <label for="im" class="col-lg-2 control-label"> Intensity Measures </label> \
                            <div class="col-lg-8"> \
                                <select id="im" name="im" class="form-control"> \
                                    <option value="pga">PGA</option> \
                                    <option value="sa">SA</option> \
                                    <option value="pgv">PGV</option> \
                                    <option value="mmi">MMI</option> \
                                </select> \
                                <div id=sa_period_wraper> \
                                    <input id="sa_period" class="form-control" placeholder="Sa period" type="number"> \
                                </div> \
                                <div id=il_wraper> \
                                    <input id="il" class="form-control" placeholder="Intensity levels. Ex: 0.1, 0.2, 0.45..." type="number"> \
                                </div> \
                            </div> \
                            <div class="col-lg-2"> \
                                <button id="add-imt-btn" class="btn btn-sm btn-primary" type="button">Add IMT</button> \
                            </div> \
                        </div>');

    $('#sa_period_wraper').hide();
    $('#im').on('change', function(){
        var imt = $('#im').val();
        if ( imt == 'sa' ){
            $('#sa_period_wraper').show();
        }
        else {
            $('#sa_period_wraper').hide();
        }
    });


    var map = new L.Map('map', {
        fullscreenControl: true,
        fullscreenControlOptions: {
            position: 'topleft'
        }
    });
    map.setView(new L.LatLng(0, 0),2);
    bw.addTo(map);

    var control = L.control.layers(baseLayers).addTo(map);

    // Initialize the FeatureGroup to store editable layers
    var drawnItems = new L.FeatureGroup();
    map.addLayer(drawnItems);


    var polygonOptions = {
                showArea: true,
            };

    // Initialise the draw control and pass it the FeatureGroup of editable layers
    var drawControl = new L.Control.Draw({
        edit: {
            featureGroup: drawnItems,
            //edit: false,
            //remove: false
        },
        draw: {
            polyline: false,
            polygon: polygonOptions,
            rectangle: false,
            circle: false,
            marker: false
        }
    });
    map.addControl(drawControl);


    map.on('draw:created', function (e) {
        var type = e.layerType,
            layer = e.layer;

        if (type == 'polygon'){
            $('.leaflet-draw-draw-polygon').hide();
            $("#id_region").attr('value', toWKT(layer));
        }

        drawnItems.addLayer(layer);
    });


    map.on('draw:edited', function (e) {
        var layers = e.layers;
        layers.eachLayer(function (layer) {

            if (layer instanceof L.Polygon){
                $("#id_region").attr('value', toWKT(layer));
            }
        });
    });

    map.on('draw:deleted', function (e) {
        var layers = e.layers;
        layers.eachLayer(function (layer) {

            if (layer instanceof L.Polygon){
                $('.leaflet-draw-draw-polygon').show();
                $("#id_region").attr('value', '');
            }
        });
    });







});
})($); 