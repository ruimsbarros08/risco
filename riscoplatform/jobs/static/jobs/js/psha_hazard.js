 "use strict";

(function($) {
$( document ).ready(function() {

    //hide-show    
    $( "label[for='region']" ).hide( "fast");
    $( "label[for='imt_l']" ).hide( "fast");

    //$( "label[for='site_model']" ).hide( "fast");
    //$( "#id_site_model" ).hide( "fast");
    $( "#id_site_model" ).attr('disabled', true);
    
    $('#id_sites_type').on('change', function() {
        if (this.value == 'VARIABLE_CONDITIONS'){
            $( "#id_vs30" ).attr('disabled', false);
            $( "#id_vs30type" ).attr('disabled', false);
            $( "#id_z1pt0" ).attr('disabled', false);
            $( "#id_z2pt5" ).attr('disabled', false);

            $( "#id_site_model" ).attr('disabled', true);
        }
        else {
            $( "#id_vs30" ).attr('disabled', true);
            $( "#id_vs30type" ).attr('disabled', true);
            $( "#id_z1pt0" ).attr('disabled', true);
            $( "#id_z2pt5" ).attr('disabled', true);

            $( "#id_site_model" ).attr('disabled', false);

        }
    });


    var tags = $('#imt-tags').tags({
        bootstrapVersion: 3,
        tagSize: 'md',
        readOnly: false,
        popovers: true,
        popoverTrigger: 'click',
        tagClass: 'btn-success',
        //tagData: ["a", "prepopulated", "list", "of"],
        //beforeAddingTag: function(tag){ console.log(tag); },
        //afterAddingTag: function(tag){ console.log(tag); },
        beforeDeletingTag: function(tag){ remove_imt(tag); },
        afterDeletingTag: function(tag){ $('#imt-tags input').attr('disabled', true); },
        definePopover: function(tag){
            return imt_l[tag].join(", ");
        },
        //excludes: function(tag){ return true; },
    });

    $('#imt-tags input').attr('disabled', true);

    var imt_l = {};

    //$('#sa_period_wraper').hide();
    $('#sa_period').attr("disabled", true);
    
    $('#im').on('change', function(){
        var imt = $('#im').val();
        if ( imt == 'SA' ){
            $('#sa_period').attr("disabled", false);
            //$('#sa_period_wraper').show();
        }
        else {
            $('#sa_period').attr("disabled", true);
            //$('#sa_period_wraper').hide();
        }
    });

    $('#add-imt-btn').on('click', function(){
        var imt = $('#im').val();
        if ( imt == 'SA' ){
            var sa_period = $('#sa_period').val();

            if ( isNaN(sa_period) == true ){
                $('#sa_period').val('');
                alert('Sa period must be a float value');
                return;
            }

            imt = 'SA('+sa_period+')'
        }

        var il = $("#il").val().split(',');

        for (var i = 0; i < il.length; i++){

            il[i] = parseFloat(il[i]);

            if ( isNaN(il[i]) == true ){
                alert('The internsity measure levels must be floats');
                return;
            }

        }

        imt_l[imt] = $.unique( il.sort(function(a, b){return a-b}) );

        $('#id_imt_l').val( JSON.stringify(imt_l) );
        tags.addTag(imt);
        $('#imt-tags input').attr('disabled', true);

    });

    var remove_imt = function(imt){
        delete imt_l[imt];
        $('#id_imt_l').val( JSON.stringify(imt_l) );
        $('#imt-tags input').attr('disabled', true);
    }


    $('#structural_vulnerability_add_imt_l, \
        #non_structural_vulnerability_add_imt_l, \
        #contents_vulnerability_add_imt_l, \
        #business_int_vulnerability_add_imt_l, \
        #occupants_vulnerability_add_imt_l').on('click', function(){

        var type = $(this).attr('id').split('_add')[0];
        var vul_id = $( '#id_'+type ).val();

        if (vul_id){
            $.ajax( '/models/vulnerability/'+vul_id+'/imt/' )
                .done(function(data) {

                $('#id_imt_l').val( JSON.stringify(data) );

                for (var i = 0; i<Object.keys( data ).length; i++){
                    var tag = Object.keys( data )[i];
                    imt_l[tag] = data[tag];
                    tags.addTag(tag);
                }

                $('#imt-tags input').attr('disabled', true);
            });
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