 "use strict";

(function($) {
$( document ).ready(function() {

var draw_chart = function(values){
    $('#chart-container').highcharts({
        chart: {
            type: 'areaspline'
        },
        title: {
            text: 'Cumulative distribution function'
        },
        //legend: {
        //    layout: 'vertical',
        //    align: 'left',
        //    verticalAlign: 'top',
        //    x: 150,
        //    y: 100,
        //    floating: true,
        //    borderWidth: 1,
        //    backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'
        //},
        xAxis: {
            categories: values[0],
            //plotBands: [{ // visualize the weekend
            //    from: 4.5,
            //    to: 6.5,
            //    color: 'rgba(68, 170, 213, .2)'
            //}]
        },
        yAxis: {
            title: {
                text: ''
            }
        },
        tooltip: {
            shared: true,
            valueSuffix: ''
        },
        credits: {
            enabled: false
        },
        plotOptions: {
            areaspline: {
                fillOpacity: 0.5
            }
        },
        series: [{
            name: '',
            data: values[1]
        },]
    });
    }

$('#select').on('change', function() {

    var url = document.URL.split('/');
    var model_id = url[url.length -2];

    $.ajax( BASE_URL+'models/fragility/'+model_id+'/taxonomy/'+$(this).val() )
    .done(function(data) {
        var str = data[0].fields.cdf;
        var cdf = JSON.parse("[" + str + "]");

        console.log(cdf[0]);

        draw_chart(cdf[0]);
    })
    .fail(function() {
        alert( "error" );
    })
    .always(function() {
        //alert( "complete" );
    });

});


});
})($); 