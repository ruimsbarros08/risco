 "use strict";

(function($) {
$( document ).ready(function() {

var draw_chart = function(categories, container, title){

    return new Highcharts.Chart({
        chart: {
            type: 'areaspline',
            renderTo: container,
        },
        title: {
            text: title
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
            categories: categories,
            //plotBands: [{ // visualize the weekend
            //    from: 4.5,
            //    to: 6.5,
            //    color: 'rgba(68, 170, 213, .2)'
            //}]
        },
        yAxis: {
            title: {
                text: 'Probability of exceedance'
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
        series: []
    });
    }

$('#select').on('change', function() {

    var url = document.URL.split('/');
    var model_id = url[url.length -2];

    $.ajax( BASE_URL+'models/fragility/'+model_id+'/taxonomy/'+$(this).val() )
    .done(function(data) {

        var str = data[0].fields.cdf;
        var categories = JSON.parse("[" + str + "]")[0][0];
        
        var prob_chart = draw_chart(categories, 'chart-container-prob', 'Probability distribution function');
        var cum_chart = draw_chart(categories, 'chart-container-cum', 'Cumulative distribution function');

        for (var i=0; i<data.length; i++){

            var str_pdf = data[i].fields.pdf;
            var str_cdf = data[i].fields.cdf;
            var pdf = JSON.parse("[" + str_pdf + "]")[0][1];
            var cdf = JSON.parse("[" + str_cdf + "]")[0][1];

            prob_chart.addSeries({name: data[i].fields.limit_state, data: pdf})
            cum_chart.addSeries({name: data[i].fields.limit_state, data: cdf})
        }

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