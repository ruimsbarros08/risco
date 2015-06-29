
$.ajaxSetup({ 
     beforeSend: function(xhr, settings) {
         function getCookie(name) {
             var cookieValue = null;
             if (document.cookie && document.cookie != '') {
                 var cookies = document.cookie.split(';');
                 for (var i = 0; i < cookies.length; i++) {
                     var cookie = jQuery.trim(cookies[i]);
                     // Does this cookie string begin with the name we want?
                 if (cookie.substring(0, name.length + 1) == (name + '=')) {
                     cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                     break;
                 }
             }
         }
         return cookieValue;
         }
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     } 
});


//SPINNER

var spinner_opts = {
    lines: 11,
    length: 0,
    width: 7,
    radius: 15,
    rotate: 0,
    speed: 1.4,
    trail: 60, 
    shadow: false,
    className: 'spinner',
};
var spinner = new Spinner(spinner_opts);
var ajax_cnt = 0;


 
$(document).ajaxStart(function() {

    var modal = $('#modal').modal({
        backdrop: 'static',
        keyboard: false
    });
    modal.modal('show');
    spinner.spin($('#spinner_center')[0]);
    ajax_cnt++;
});
 
$(document).ajaxStop(function() {
    ajax_cnt--;
    if (ajax_cnt >= 0) {
        spinner.stop();
        var modal = $('#modal').modal({
            backdrop: 'static',
            keyboard: false
        });
        modal.modal('hide');
        ajax_cnt = 0;
   }
});



//functions
function toWKT(layer) {
    var lng, lat, coords = [];
    if (layer instanceof L.Polygon || layer instanceof L.Polyline) {
        var latlngs = layer.getLatLngs();
        for (var i = 0; i < latlngs.length; i++) {
            latlngs[i]
            coords.push(latlngs[i].lng + " " + latlngs[i].lat);
            if (i === 0) {
                lng = latlngs[i].lng;
                lat = latlngs[i].lat;
            }
    };
        if (layer instanceof L.Polygon) {
            return "POLYGON((" + coords.join(",") + "," + lng + " " + lat + "))";
        } else if (layer instanceof L.Polyline) {
            return "LINESTRING(" + coords.join(",") + ")";
        }
    } else if (layer instanceof L.Marker) {
        return "POINT(" + layer.getLatLng().lng + " " + layer.getLatLng().lat + ")";
    }
}


function wktToLatLng(wkt) {
    var lon = parseFloat(wkt.split('(')[1].split(' ')[0])
    var lat = parseFloat(wkt.split('(')[1].split(' ')[1].split(')')[0])
    return [lat, lon]
}

/*
function get_world(){
    $.ajax('/countries')
    .done(function(data){
        for (var i = 0; i<data.length; i++){
            $("#country").append('<option value='+data[i][0]+'>'+data[i][1]+'</option>');
        }
    });
    
    $("#level1").remoteChained({
        parents : "#country",
        url : "/level1"
    });

    $("#level2").remoteChained({
        parents : "#level1",
        url : "/level2"
    });

    $("#level3").remoteChained({
        parents : "#level2",
        url : "/level3"
    });
}
*/


var epicenterIcon = L.icon({
        iconUrl: '/static/img/star.png',
        iconSize: [30, 30],
    });


function get_hazard_options(geojson){
    return  {
            recordsField: 'values',
            locationMode: L.LocationModes.LOOKUP,
            locationLookup: geojson,
            codeField: 'id',
            includeBoundary: false,

            displayOptions: {
                'value': {
                    displayName: 'Acceleration g (m/s2)',
                    fillColor: new L.HSLHueFunction(new L.Point(0,90), new L.Point(1,0)),
                    color: new L.HSLHueFunction(new L.Point(0,90), new L.Point(1,0), {outputSaturation: '100%', outputLuminosity: '30%'})
                }
            },
            layerOptions: {
                fillOpacity: 0.5,
                opacity: 0.7,
                weight: 0.5,
            },
            tooltipOptions: {
                iconSize: new L.Point(100,65),
                iconAnchor: new L.Point(-5,65)
            },
            legendOptions: {
                //title: 'Hazard g (m/s2)'
            }
        };
}



function get_losses_options(geojson, total){
    return  {
            recordsField: 'values',
            locationMode: L.LocationModes.LOOKUP,
            locationLookup: geojson,
            codeField: 'id',
            includeBoundary: false,
            displayOptions: {
                'value': {
                    displayName: 'Losses',
                    fillColor: new L.HSLHueFunction(new L.Point(0,90), new L.Point(total,0)),
                    color: new L.HSLHueFunction(new L.Point(0,90), new L.Point(total,0), {outputSaturation: '100%', outputLuminosity: '30%'})
                }
            },
            layerOptions: {
                fillOpacity: 0.5,
                opacity: 0.7,
                weight: 0.5,
            },
            tooltipOptions: {
                iconSize: new L.Point(100,65),
                iconAnchor: new L.Point(-5,65)
            },
            legendOptions: {
                //title: 'Losses'
            }
        };
}

    var redIcon = L.AwesomeMarkers.icon({
                        icon: 'stats',
                        markerColor: 'red'
                    });

    var blueIcon = L.AwesomeMarkers.icon({
                        icon: 'stats',
                        markerColor: 'blue'
                    });



//Maps base layers

var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
var osmAttrib='Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
var osm = new L.TileLayer(osmUrl, {attribution: osmAttrib});

var bwUrl='http://{s}.tiles.wmflabs.org/bw-mapnik/{z}/{x}/{y}.png';
var bwAttrib='&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>';
var bw = new L.TileLayer(bwUrl, {attribution: bwAttrib});

var ocmUrl='http://{s}.tile.opencyclemap.org/cycle/{z}/{x}/{y}.png';
var ocmAttrib='Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
var ocm = new L.TileLayer(ocmUrl, {attribution: ocmAttrib});

var hikingUrl='http://toolserver.org/tiles/hikebike/{z}/{x}/{y}.png';
var hikingAttrib='Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
var hiking = new L.TileLayer(hikingUrl, {attribution: hikingAttrib});

var transportUrl='http://{s}.tile2.opencyclemap.org/transport/{z}/{x}/{y}.png';
var transportAttrib='Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
var transport = new L.TileLayer(transportUrl, {attribution: transportAttrib});

var Esri_WorldImagery = 'http://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}';
var Esri_WorldImagery_attribution = 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community';
var Esri_WorldImageryLayer = new L.tileLayer(Esri_WorldImagery, {attribution: Esri_WorldImagery_attribution});


var baseLayers = {
    "Black and White": bw,
    "OpenStreetMap": osm,
    "OpenCycleMap": ocm,
    "Hiking": hiking,
    "Transport": transport,
    "ESRI World": Esri_WorldImageryLayer
};



//Forms 
$( document ).ready(function() {
    $('form input').addClass('form-control');
    $('form select').addClass('form-control');
    $('form textarea').addClass('form-control');
});


function getRandomColor() {
    var letters = '0123456789ABCDEF'.split('');
    var color = '#';
    for (var i = 0; i < 6; i++ ) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

function hexToRgb(hex) {
    var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
    } : null;
}


function isFloat(n){
        return   n===Number(n)  && n%1!==0
}



var RegionSelectControl = L.Control.extend({
    options: {
        position: 'topright'
    },

    onAdd: function (map) {
        var container = L.DomUtil.get('region-selector');
        return container;
    }
});




