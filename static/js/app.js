var myApp=angular.module('myApp', ['ngCookies']);

   myApp.config(function($interpolateProvider){
    $interpolateProvider.startSymbol('{[{').endSymbol('}]}');
    });


 
function Todo($scope,$http,$filter,$location,$cookies) {



	console.log($location.url())

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



    });


   
    $http.get("/clientes").success(function(response) {

    	$scope.clientes = response;

    });

    $http.get("/user").success(function(response) {

    	$scope.user = response[0];

    });

    $scope.editContact = function(contact) 
    {

    $http.get("/servicios/"+contact.id).success(function(response) {

    	$scope.servicios = response;


    });
    
    };

     $scope.logear = function(contact) 
    {


        $http({
        url: "/logear/",
        data: contact,
        method: 'POST',
        headers: {
        'X-CSRFToken': $cookies['csrftoken']
        }
        }).
        success(function(data) {

        	console.log(data)

        })

    };




    $scope.activar = function(contact,index) 
    {

    $http.get("/activar/"+contact.id).success(function(response) {



    $scope.servicios[index].status = 1

    console.log($scope.servicios[index])


    });
    
    };

    $scope.desactivar = function(contact,index) 
    {

    $http.get("/desactivar/"+contact.id).success(function(response) {


    $scope.servicios[index].status = 0


    });
    
    };






}



