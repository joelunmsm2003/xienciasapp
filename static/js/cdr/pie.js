
$(function () {
    $('#pie').highcharts({
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie',
            events: {
                    load: function () {

                        // set up the updating of the chart each second
                        var series = this.series[0];


        var updateChart = function() {
            
        $.getJSON("/cant", function (result) {


            console.log('grafica',result[0])


            
            series.data[0].update(result[0]['answer']);
            series.data[1].update(result[0]['noanswer']);
       

        });   


        }      
              
        setInterval(function(){updateChart()},1000);



                    }
                }



        },
        title: {
            text: 'Trafico LLamadas Unitlab'
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                showInLegend: true,
                dataLabels: {
                    enabled: true,
                    format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                    style: {
                        color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                    }
                }
            }
        },

         
        series: [{

            name: "Total SMS",
            colorByPoint: true,
            data: [
            {
                name: "Answered",
                y: 0,

            }, {
                name: "No Answer",
                y: 0
            }

            ]
        }]

    });
});


