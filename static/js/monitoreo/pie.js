 
    var myApp=angular.module('App', []);
    myApp.config(function($interpolateProvider){
    $interpolateProvider.startSymbol('{[{').endSymbol('}]}');
    });



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
            
        $.getJSON("/llamadas", function (result) {


            console.log('grafica',result[0])


            
            series.data[0].update(result[0]['num_est']);
            series.data[1].update(result[1]['num_est']);
            series.data[2].update(result[2]['num_est']);
            series.data[3].update(result[3]['num_est']);
            series.data[4].update(result[4]['num_est']);
       

        });   


        }      
              
        setInterval(function(){updateChart()},1000);



                    }
                }



        },
        title: {
            text: 'Trafico LLamadas Interfono'
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
                name: "No Contestada",
                y: 0,

            }, {
                name: "Contestada",
                y: 0
            }, {
                name: "Ocupado",
                y: 0
            }, {
                name: "Busy/Congested",
                y: 0
            }, {
                name: "Cancelada",
                y: 0
            }

            ]
        }]

    });
});


 $(function () {
    $('#bar').highcharts({
        chart: {
            type: 'column'
        },
        title: {
            text: 'Estado vs Tipo Llamada'
        },
        subtitle: {
            text: 'Source: Xiencias'
        },
        xAxis: {
            categories: [
                'No Contestada',
                'Contestada',
                'Ocupado',
                'Busy/Congested',
                'Cancelada'
                
            ],
            crosshair: true
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Rainfall '
            }
        },
        tooltip: {
            headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                '<td style="padding:0"><b>{point.y:.1f} </b></td></tr>',
            footerFormat: '</table>',
            shared: true,
            useHTML: true
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
        series: [{
            name: 'Entrante',
            data: [49, 71, 106, 129, 144]

        }, {
            name: 'Saliente',
            data: [83, 78, 98, 93, 106]

        }]
    });
});




function Controller($scope,$http) {

   $http.get("/anexos").success(function(response) {$scope.anexo = response;

      
              console.log($scope.anexo)
        
    });

    $http.get("/user").success(function(response) {

        $scope.user = response[0];

    });

        $http.get("/serviciosapi").success(function(response) {

        console.log('servicio',response[0]['status'])

        $scope.blaster = response[0]['status'];
        $scope.cdr = response[1]['status'];
        $scope.monitor = response[2]['status'];

    });




}

