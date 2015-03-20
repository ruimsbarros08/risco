 "use strict";

(function($) {
$( document ).ready(function() {

$('#fragility-info').hide();

var poe;

var draw_chart = function(categories, container, title, units){

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
            title: {
                text: 'IML ('+units+')'
            },
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
            },
            plotLines: [{
                color: '#FF0000',
                width: 2,
                value: poe
            }],
            max: 1.0,
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

var shown = false;
$('#select').on('change', function() {
    if (!shown){
        var shown = true;
        $('#fragility-info').show('fast');
    }

    var url = document.URL.split('/');
    var model_id = url[url.length -2];

    $.ajax( BASE_URL+'models/fragility/'+model_id+'/taxonomy/'+$(this).val() )
    .done(function(data) {

        $('#imt').html(data.info[0].fields.imt);
        $('#sa_period').html(data.info[0].fields.sa_period);
        $('#unit').html(data.info[0].fields.unit);
        $('#min_iml').html(data.info[0].fields.min_iml);
        $('#max_iml').html(data.info[0].fields.max_iml);


        var str = data.functions[0].fields.cdf;
        var categories = JSON.parse("[" + str + "]")[0][0];
        
        //var prob_chart = draw_chart(categories, 'chart-container-prob', 'Probability distribution function');
        var cum_chart = draw_chart(categories, 'chart-container-cum', 'Cumulative distribution function', data.info[0].fields.unit);

        $('#values-table tbody').html('');

        for (var i=0; i<data.functions.length; i++){
            var $tr;
            $('#values-table tbody').append(
                $tr = $('<tr>').append(
                    $('<td>').text(data.functions[i].fields.limit_state),
                    $('<td>').text(data.functions[i].fields.mean),
                    $('<td>').text(data.functions[i].fields.stddev)
                )   
            )

            var str_pdf = data.functions[i].fields.pdf;
            var str_cdf = data.functions[i].fields.cdf;
            var pdf = JSON.parse("[" + str_pdf + "]")[0][1];
            var cdf = JSON.parse("[" + str_cdf + "]")[0][1];

            //prob_chart.addSeries({name: data[i].fields.limit_state, data: pdf})
            cum_chart.addSeries({name: data.functions[i].fields.limit_state, data: cdf, zIndex: data.functions.length-i})
        }

    })


});


});
})($); 