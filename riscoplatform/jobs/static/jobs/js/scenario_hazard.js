 "use strict";

(function($) {
$( document ).ready(function() {

    //$('label').addClass('control-labels col-lg-2');
    $('input').addClass('form-control');
    $('select').addClass('form-control');
    $('textarea').addClass('form-control');
    //$('input').wrap('<div class="col-lg-10"></div>');
    //$('input[value="csrfmiddlewaretoken"]').next().unwrap();

    //dividers
    $('<hr>').insertAfter('#id_description');
    $('<hr>').insertAfter('#id_grid_spacing');
    $('<hr>').insertAfter('#id_z2pt5');
    $('<hr>').insertAfter('#id_rupture_mesh_spacing');
    $('<hr>').insertAfter('#id_rupture_xml');
    $('<hr>').insertAfter('#id_n_gmf');
    

    //hide-show    
    $( "label[for='id_site_model']" ).hide( "fast");
    $( "#id_site_model" ).hide( "fast");
    $('#id_sites_type').on('change', function() {
        if (this.value == 'VARIABLE_CONDITIONS'){
            $( "label[for='id_vs30']" ).hide( "fast");
            $( "#id_vs30" ).hide( "fast");
            $( "label[for='id_vs30type']" ).hide( "fast");
            $( "#id_vs30type" ).hide( "fast");
            $( "label[for='id_z1pt0']" ).hide( "fast");
            $( "#id_z1pt0" ).hide( "fast");
            $( "label[for='id_z2pt5']" ).hide( "fast");
            $( "#id_z2pt5" ).hide( "fast");

            $( "label[for='id_site_model']" ).show( "fast");
            $( "#id_site_model" ).show( "fast");
        }
        else {
            $( "label[for='id_vs30']" ).show( "fast");
            $( "#id_vs30" ).show( "fast");
            $( "label[for='id_vs30type']" ).show( "fast");
            $( "#id_vs30type" ).show( "fast");
            $( "label[for='id_z1pt0']" ).show( "fast");
            $( "#id_z1pt0" ).show( "fast");
            $( "label[for='id_z2pt5']" ).show( "fast");
            $( "#id_z2pt5" ).show( "fast");

            $( "label[for='id_site_model']" ).hide( "fast");
            $( "#id_site_model" ).hide( "fast");

        }
    });

    $( "label[for='id_rake']" ).hide( "fast");
    $( "#id_rake" ).hide( "fast");
    $( "label[for='id_upper_depth']" ).hide( "fast");
    $( "#id_upper_depth" ).hide( "fast");
    $( "label[for='id_lower_depth']" ).hide( "fast");
    $( "#id_lower_depth" ).hide( "fast");
    $( "label[for='id_dip']" ).hide( "fast");
    $( "#id_dip" ).hide( "fast");
    $( "label[for='id_rupture_xml']" ).hide( "fast");
    $( "#id_rupture_xml" ).hide( "fast");
    $('#id_rupture_type').on('change', function() {
        if (this.value == 'CLOSEST_FAULT'){
            $( "label[for='id_rake']" ).hide( "fast");
            $( "#id_rake" ).hide( "fast");
            $( "label[for='id_upper_depth']" ).hide( "fast");
            $( "#id_upper_depth" ).hide( "fast");
            $( "label[for='id_lower_depth']" ).hide( "fast");
            $( "#id_lower_depth" ).hide( "fast");
            $( "label[for='id_dip']" ).hide( "fast");
            $( "#id_dip" ).hide( "fast");
            $( "label[for='id_rupture_xml']" ).hide( "fast");
            $( "#id_rupture_xml" ).hide( "fast");

            $( "label[for='id_magnitude']" ).show( "fast");
            $( "#id_magnitude" ).show( "fast");
            $( "label[for='id_depth']" ).show( "fast");
            $( "#id_depth" ).show( "fast");
            $( "label[for='id_fault_model']" ).show( "fast");
            $( "#id_fault_model" ).show( "fast");
        }
        else if (this.value == 'CUSTOM_RUPTURE'){
            $( "label[for='id_rake']" ).show( "fast");
            $( "#id_rake" ).show( "fast");
            $( "label[for='id_upper_depth']" ).show( "fast");
            $( "#id_upper_depth" ).show( "fast");
            $( "label[for='id_lower_depth']" ).show( "fast");
            $( "#id_lower_depth" ).show( "fast");
            $( "label[for='id_dip']" ).show( "fast");
            $( "#id_dip" ).show( "fast");
            $( "label[for='id_magnitude']" ).show( "fast");
            $( "#id_magnitude" ).show( "fast");
            $( "label[for='id_depth']" ).show( "fast");
            $( "#id_depth" ).show( "fast");

            $( "label[for='id_rupture_xml']" ).hide( "fast");
            $( "#id_rupture_xml" ).hide( "fast");
            $( "label[for='id_fault_model']" ).hide( "fast");
            $( "#id_fault_model" ).hide( "fast");
        }
        else {
            $( "label[for='id_rake']" ).hide( "fast");
            $( "#id_rake" ).hide( "fast");
            $( "label[for='id_upper_depth']" ).hide( "fast");
            $( "#id_upper_depth" ).hide( "fast");
            $( "label[for='id_lower_depth']" ).hide( "fast");
            $( "#id_lower_depth" ).hide( "fast");
            $( "label[for='id_dip']" ).hide( "fast");
            $( "#id_dip" ).hide( "fast");
            $( "label[for='id_magnitude']" ).hide( "fast");
            $( "#id_magnitude" ).hide( "fast");
            $( "label[for='id_depth']" ).hide( "fast");
            $( "#id_depth" ).hide( "fast");
            $( "label[for='id_fault_model']" ).hide( "fast");
            $( "#id_fault_model" ).hide( "fast");

            $( "label[for='id_rupture_xml']" ).show( "fast");
            $( "#id_rupture_xml" ).show( "fast");
        }
    });

    $( "label[for='id_sa2_period']" ).hide( "fast");
    $( "#id_sa2_period" ).hide( "fast");
    $( "label[for='id_sa3_period']" ).hide( "fast");
    $( "#id_sa3_period" ).hide( "fast");
    $('#id_sa1_period').on('focusout', function() {
        if (this.value != ''){
            $( "label[for='id_sa2_period']" ).show( "fast");
            $( "#id_sa2_period" ).show( "fast");
        }
        else {
            $( "label[for='id_sa2_period']" ).hide( "fast");
            $( "#id_sa2_period" ).hide( "fast");
            $( "label[for='id_sa3_period']" ).hide( "fast");
            $( "#id_sa3_period" ).hide( "fast");
        }
    });
    $('#id_sa2_period').on('focusout', function() {
        if (this.value != ''){
            $( "label[for='id_sa3_period']" ).show( "fast");
            $( "#id_sa3_period" ).show( "fast");
        }
        else {
            $( "label[for='id_sa3_period']" ).hide( "fast");
            $( "#id_sa3_period" ).hide( "fast");
        }
    });

    $('#id_correlation_model').change( function() {
        if ($(this).is(":checked")){
            $( "label[for='id_vs30_clustering']" ).show( "fast");
            $( "#id_vs30_clustering" ).show( "fast");
        }
        else {
            $( "label[for='id_vs30_clustering']" ).hide( "fast");
            $( "#id_vs30_clustering" ).hide( "fast");
        }
    });



	var map = new L.Map('map');
	var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
	var osmAttrib='Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
	var osm = new L.TileLayer(osmUrl, {minZoom: 3, maxZoom: 16, attribution: osmAttrib});

	map.setView(new L.LatLng(40, -8),5);
	map.addLayer(osm);


});
})($); 