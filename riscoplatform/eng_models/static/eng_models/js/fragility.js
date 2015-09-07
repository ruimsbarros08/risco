 "use strict";

(function($) {
$( document ).ready(function() {

// $('#fragility-info').hide();

var poe;
var categories;
var cum = [];
var frag_functions = [];

var draw_fragility = function(categories, container, title, units){

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


var url = document.URL.split('/');
var model_id = url[url.length -2];

var get_taxonomy = function(tax){

    $.ajax(BASE_URL+'/models/fragility/'+model_id+'/taxonomy/'+tax )
    .done(function(data) {

        $('#imt').html(data.info[0].fields.imt);
        $('#sa_period').html(data.info[0].fields.sa_period);
        $('#unit').html(data.info[0].fields.unit);
        $('#min_iml').html(data.info[0].fields.min_iml);
        $('#max_iml').html(data.info[0].fields.max_iml);


        var str = data.functions[0].fields.cdf;
        categories = JSON.parse("[" + str + "]")[0][0];
        
        var cum_chart = draw_fragility(categories, 'chart-container-cum', 'Cumulative distribution function', data.info[0].fields.unit);

        $('#values-table tbody').html('');

        cum = [];
        for (var i=0; i<data.functions.length; i++){
            var $tr;
            $('#values-table tbody').append(
                $tr = $('<tr>').append(
                    $('<td>').text(data.functions[i].fields.limit_state),
                    $('<td>').text(Humanize.formatNumber(data.functions[i].fields.mean, 4)),
                    $('<td>').text(Humanize.formatNumber(data.functions[i].fields.stddev, 4))
                )   
            )

            var str_pdf = data.functions[i].fields.pdf;
            var str_cdf = data.functions[i].fields.cdf;
            var pdf = JSON.parse("[" + str_pdf + "]")[0][1];
            var cdf = JSON.parse("[" + str_cdf + "]")[0][1];
            
            cum.push({name: data.functions[i].fields.limit_state, cdf: cdf})

            cum_chart.addSeries({name: data.functions[i].fields.limit_state, data: cdf, zIndex: data.functions.length-i})
            
        }
        frag_functions = [];
        for (var i=0; i<data.limit_states.length; i++){
            for (var j=0; j<cum.length; j++){
                if (data.limit_states[i] == cum[j].name){
                    frag_functions.push(cum[j]);
                }
            }
        }

        if (cons_shown){
            update_vulnerability();
        }


    });

}




var shown = false;
$('#select').on('change', function() {
    // if (!shown){
    //     shown = true;
    //     $('#fragility-info').show('fast');
    // }

    get_taxonomy($(this).val());

});

get_taxonomy($('#select').val());


var cons_categories;
var cons_values;
var cons_shown = false;

$('#id_consequence_model').on('change', function(){
    update_consequence($(this).val());
});

var update_consequence = function(model_id){
    cons_shown = true;
    $.ajax(BASE_URL+'/models/consequence/'+model_id+'/ajax/')
    .done(function(data) {
        if (data.limit_states == null){
            cons_categories = [];
        }
        else {
            cons_categories = data.limit_states;
        }

        
        for (var i = 0; i < cons_categories.length; i++){
            $('#limit-state-dropdown').append(
                    "<option>"+cons_categories[i]+"</option>"
            );
        }

        if (data.values == null){
            cons_values = [];
        }
        else {
            cons_values = data.values;
        }


        var chart = new Highcharts.Chart({
            chart: {
                type: 'column',
                renderTo: 'chart-container',
            },
            title: {
                text: 'Consequence model'
            },
            subtitle: {
                text: ''
            },
            xAxis: {
                categories: cons_categories,
                title: {
                    text: null
                }
            },
            yAxis: {
                min: 0,
                //max: 1.0,
                title: {
                    text: '% Repair cost / Total cost',
                },
                labels: {
                    overflow: 'justify'
                }
            },
            tooltip: {
                valueSuffix: ''
            },
            plotOptions: {
                bar: {
                    dataLabels: {
                        enabled: true
                    }
                }
            },
            credits: {
                enabled: false
            },
            series: [{
                id: 'cons',
                name: '% Repair cost / Total cost',
                data: cons_values
            },
            ]
        });

        // if (shown && cons_shown){
            update_vulnerability();
        // }
    });
}



var update_vulnerability = function(){

        var values = [];
        for (var i = 0; i<categories.length; i++){

            var sum = 0;
            for (var j =0; j<cons_values.length; j++){

                if (j < cons_values.length-1){
                    sum += (frag_functions[j].cdf[i] - frag_functions[j+1].cdf[i])*cons_values[j];
                }
                else {
                    sum += frag_functions[j].cdf[i]*cons_values[j];
                }
            }

            values.push(sum);
            sum = 0;
        }

        var chart = new Highcharts.Chart({
            chart: {
                renderTo: 'vulnerability-container',
            },
            title: {
                text: 'Vulnerability preview - '+$("#select option:selected").text()
            },
            subtitle: {
                text: ''
            },
            xAxis: {
                categories: categories,
                title: {
                    text: null
                }
            },
            yAxis: {
                min: 0,
                //max: 1.0,
                title: {
                    text: 'Loss ratio',
                },
                labels: {
                    overflow: 'justify'
                }
            },
            tooltip: {
                valueSuffix: ''
            },
            plotOptions: {
                bar: {
                    dataLabels: {
                        enabled: true
                    }
                }
            },
            credits: {
                enabled: false
            },
            series: [{
                id: 'cons',
                name: 'Loss ratio',
                data: values
            },
            ]
        });
    }



});
})($); 