var myApp=angular.module('myApp', ['ngCookies']);

   myApp.config(function($interpolateProvider){
    $interpolateProvider.startSymbol('{[{').endSymbol('}]}');
    });


 
function Todo($scope,$http,$cookies,$filter) {

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



 


   
    $http.get("/usuarios").success(function(response) {

      $scope.clientes = response;
      $scope.useract = response[0]['first_name']
      $scope.userid = response[0]['id']

       $http.get("/servicios/"+response[0]['id']).success(function(response) {

      $scope.servicios = response;
      $scope.items = response
      console.log('data',$scope.servicios)

      $('#boxContainer').hide()


         });


    });




    $http.get("/user").success(function(response) {

      $scope.user = response[0];

    });

    $scope.editContact = function(contact) 
    {

    $scope.useract = contact.first_name
    $scope.userid = contact.id
    $http.get("/servicios/"+contact.id).success(function(response) {

      $scope.servicios = response;
      
      console.log('data',$scope.servicios)


    });
    
    };

    $scope.agregarservicio = function(contact) 
    {

         $('#servicio').modal('hide')
         $('.modal-backdrop').remove();
         $('#boxContainer').show()


    console.log('serv',contact.selected)

        var todo={

            servicio :contact.selected,
            user:$scope.userid,
            done:false
        }

        $http({
        url: "/servicios/"+$scope.userid+"/",
        data: todo,
        method: 'POST',
        headers: {
        'X-CSRFToken': $cookies['csrftoken']
        }
        }).
        success(function(data) {

                 swal({   
                title: "Servicio agregado",      
                type: "success",     
                confirmButtonColor: "#46568B",   
                confirmButtonText: "Aceptar",   
                text: data ,
                closeOnConfirm: false,   
                closeOnCancel: false }, 

                function(isConfirm){ 

                    $('#boxContainer').hide()  
               
                    if (isConfirm) {     
                        location.reload(true);   
                    } 
                   });
        

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



