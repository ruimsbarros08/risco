 "use strict";

(function($) {
$( document ).ready(function() {

    $('label').addClass('control-labels col-lg-2');
    $('input').addClass('form-control');
    $('select').addClass('form-control');
    $('textarea').addClass('form-control');
    $('input').wrap('<div class="col-lg-10"></div>');
    $('select').wrap('<div class="col-lg-10"></div>');
    $('textarea').wrap('<div class="col-lg-10"></div>');
    $('<div class="form-group">').insertBefore('label');
    $('</div>').insertAfter('</input>');
    $('</div>').insertAfter('</textarea>');
    $('</div>').insertAfter('</select>');
    
    $('input[name="csrfmiddlewaretoken"]').unwrap();
    //$('#id_location').unwrap();
    //$('#id_rupture_geom').unwrap();

    //dividers
    //$('<hr>').insertAfter('#id_xml');
    
    $( "label[for='id_tax_source_name']" ).hide( "fast");
    $( "#id_tax_source_name" ).hide( "fast");
    $( "label[for='id_tax_source_desc']" ).hide( "fast");
    $( "#id_tax_source_desc" ).hide( "fast");
    $('#id_add_tax_source').change( function() {
        if ($(this).is(":checked")){
            $( "label[for='id_tax_source_name']" ).show( "fast");
            $( "#id_tax_source_name" ).show( "fast");
            $( "label[for='id_tax_source_desc']" ).show( "fast");
            $( "#id_tax_source_desc" ).show( "fast");
        }
        else {
            $( "label[for='id_tax_source_name']" ).hide( "fast");
            $( "#id_tax_source_name" ).hide( "fast");
            $( "label[for='id_tax_source_desc']" ).hide( "fast");
            $( "#id_tax_source_desc" ).hide( "fast");
        }
    });


});
})($); 