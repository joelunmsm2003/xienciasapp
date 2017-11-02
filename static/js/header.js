
var myApp=angular.module('myApp', ['ngCookies']);
myApp.config(function($interpolateProvider){
$interpolateProvider.startSymbol('{[{').endSymbol('}]}');
});

var sortingOrder = '-id';




function Todo($scope,$http,$cookies,$filter) {

     $http.get("/appexternas").success(function(response) {


        $scope.sup = response[0]
        $scope.age = response[1]

        console.log('SUP',$scope.sup)


    });

        $http.get("/serviciosapi").success(function(response) {

        console.log('servicio',response[0]['status'],response[1]['status'])

    $scope.age=response[0]['status']
    $scope.blaster = response[1]['status'];
    $scope.cdr = response[2]['status'];
    $scope.mail = response[3]['status'];
    $scope.monitoreo = response[4]['status'];
    $scope.sms = response[5]['status'];
    $scope.sup = response[6]['status'];
    $scope.tasky = response[7]['status']


         $('header').fadeToggle("slow")
      $('.table').fadeToggle("slow")


        });

        
    
    Todo.$inject = ['$scope', '$filter'];

    
    

}

