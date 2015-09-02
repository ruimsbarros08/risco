 "use strict";

(function($) {
$( document ).ready(function() {

    var url = document.URL.split('/');
    var model_id = url[url.length -2];

    var chart;
    var categories = [];
    var values = [];

    var addLimitState = function(cat_name){
        categories.push(cat_name);
        chart.xAxis[0].setCategories(categories);
        chart.get("cons").addPoint(0);
        chart.redraw();
        //updateLimitStates(cat_name);

        $("#id_limit_states").attr('value', categories.toString());
        $('#limit-state-dropdown').append(
                "<option>"+cat_name+"</option>"
        );
    }

    var updateValue = function(category, value){
        for (var i = 0; i < categories.length; i++){
            if (categories[i] == category){
                values[i] = value;
                categories[i] = category;
                chart.series[0].setData(values,true);
            }
        }

        var val_str = [];
        for (var i = 0; i < values.length; i++){
            val_str.push(values[i].y);
        }
        $("#id_values").attr('value', val_str.toString());
    }


    $.ajax(BASE_URL+'/models/consequence/'+model_id+'/ajax/')
    .done(function(data) {
        if (data.limit_states == null){
            categories = [];
        }
        else {
            categories = data.limit_states;
        }

        $("#id_limit_states").attr('value', categories.toString());
        
        for (var i = 0; i < categories.length; i++){
            $('#limit-state-dropdown').append(
                    "<option>"+categories[i]+"</option>"
            );
        }

        if (data.values == null){
            for (var i = 0; i < categories.length; i++){
                values.push(0);
            }
        }
        else {
            values = data.values;
        }

        $("#id_values").attr('value', values.toString());


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

    
    $('#limit-state-dropdown').on('change', function(){
        $("#limit-state-name").val($(this).val());
        for (var i = 0; i < categories.length; i++){
            if (categories[i] == $(this).val()){
                $("#limit-state-value").val(values[i]);
            }
        }
    });
    

    $("#add-limit-state").on( "click", function(){
        var cat_name = $('#limit-state').val();
        addLimitState(cat_name);
    });

    $('#update-value').on('click', function(){
        var category = $("#limit-state-dropdown").val();
        var value = parseFloat($("#limit-state-value").val());

        if (value < 0 || value > 1){
            alert('The ratios must be between 0 and 1')
        }
        else {
            updateValue(category, value);
        }
    });


});
})($); 