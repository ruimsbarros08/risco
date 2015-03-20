 "use strict";

(function($) {
$( document ).ready(function() {


    var url = document.URL.split('/');
    var model_id = url[url.length -2];

    var chart;
    var categories = [];
    var values = [];

    var updateLimitStates = function(name){
        //for (var i = 0; i < categories.length; i++){
            $('#limit-state-dropdown').append(
                "<option>"+name+"</option>"
                );
        //}
    }


    $.ajax( BASE_URL+'models/consequence/'+model_id+'/ajax/')
    .done(function(data) {
        if (data.limit_states == null){
            categories = [];
        }
        else {
            categories = data.limit_states;
        }
        for (var i = 0; i < categories.length; i++){
            updateLimitStates(categories[i]);
        }

        if (data.values == null){
            values = [];
        }
        else {
            values = data.values;
        }

        chart = new Highcharts.Chart({
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
                categories: categories,
                title: {
                    text: null
                }
            },
            yAxis: {
                min: 0,
                max: 1.0,
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
                data: values
            },
            ]
        });
    });


    $("#add-limit-state").on( "click", function(){
        var cat_name = $('#limit-state').val();
        categories.push(cat_name);
        chart.xAxis[0].setCategories(categories);
        chart.get("cons").addPoint(0);
        chart.redraw();
        updateLimitStates(cat_name);
    });

    $('#update-value').on('click', function(){
        var category = $("#limit-state-dropdown").val();
        var value = $("#limit-state-value").val();


        for (var i = 0; i < categories.length; i++){
            if (categories[i] == category){
                values[i] = value;
                chart.series[0].setData(values);
            }
        }
        chart.redraw();

    })


});
})($); 