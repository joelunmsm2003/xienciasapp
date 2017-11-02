var myApp=angular.module('myApp', []);

   myApp.config(function($interpolateProvider){
    $interpolateProvider.startSymbol('{[{').endSymbol('}]}');
    });


 
function Todo($scope,$http,$filter) {

    $http.get("/appexternas").success(function(response) {


        $scope.sup = response[0]
        $scope.age = response[1]

        console.log('SUP',$scope.sup)


    });

     $http.get("/serviciosapi").success(function(response) {

        console.log('servicio',response[0]['status'])

        
    $scope.age=response[0]['status']
    $scope.blaster = response[1]['status'];
    $scope.cdr = response[2]['status'];
    $scope.mail = response[3]['status'];
    $scope.monitoreo = response[4]['status'];
    $scope.sms = response[5]['status'];
    $scope.sup = response[6]['status'];
    $scope.tasky = response[7]['status']




    });


    $('#tog').change(function() {

      $scope.check = $(this).prop('checked')
      console.log($scope.check)
    
    })







   
    $http.get("/clientes").success(function(response) {

    	$scope.clientes = response;
         $('header').fadeToggle("slow")
      $('.table').fadeToggle("slow")

    });

    $scope.check ='false'

    $scope.data = 'false';


    $http.get("/user").success(function(response) {

    	$scope.user = response[0];

    });

    $scope.editContact = function(contact) 
    {

    $http.get("/servicios/"+contact.id).success(function(response) {

    	$scope.servicios = response;


    });
    
    };


    $scope.audio = function(data) 
    {

        console.log('check',data)

        if( data.toString()=='false'){

            $scope.data='true'
        }

        if( data.toString()=='true'){

            $scope.data='false'
        }

        console.log($scope.data)
    
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



