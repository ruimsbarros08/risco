//vars

if (location.host == 'localhost:8000'){   
    var BASE_URL = 'http://'+location.host+'/';
}
else {
    var BASE_URL = 'http://'+location.host+'/risco/';
}

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


//Maps base layers
var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
var osmAttrib='Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
var osm = new L.TileLayer(osmUrl, {attribution: osmAttrib});

var ocmUrl='http://{s}.tile.opencyclemap.org/cycle/{z}/{x}/{y}.png';
var ocmAttrib='Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
var ocm = new L.TileLayer(ocmUrl, {attribution: ocmAttrib});

var baseMaps = {
    "OpenStreetMap": osm,
    "OpenCycleMap": ocm,
};

//Forms 
$( document ).ready(function() {
    $('form input').addClass('form-control');
    $('form select').addClass('form-control');
    $('form textarea').addClass('form-control');
});

