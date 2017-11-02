
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


    $scope.sortingOrder = sortingOrder;
    $scope.reverse = false;
    $scope.filteredItems = [];
    $scope.groupedItems = [];
    $scope.itemsPerPage = 10;
    $scope.pagedItems = [];
    $scope.currentPage = 0;



    

    $(function(){
        $("#formuploadajax").on("submit", function(e){

          $('#upload').modal('hide')
         $('.modal-backdrop').remove();
      
          $('#boxContainer').show()

            e.preventDefault();
            var f = $(this);
            var formData = new FormData(document.getElementById("formuploadajax"));
            console.log('formdata',$scope.id_grupo)


            formData.append("grupo", $scope.id_grupo);
            //formData.append(f.attr("name"), $(this)[0].files[0]);
            $.ajax({
                url: "/uploadcontacto/",
                type: "post",
                dataType: "html",
                data: formData,
                cache: false,
                contentType: false,
                processData: false
            })
                .done(function(res){

                    $('#boxContainer').hide() 

                  

                    location.reload(true); 

                   

        

                });
        });
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

  
    


     $http.get("/grupos").success(function(response) {

        $scope.grupos = response;

        console.log($scope.grupo)
        $('#boxContainer').hide()

    });

        $http.get("/clientes").success(function(response) {

        $scope.clientes = response;

        
         $('header').fadeToggle("slow")
      $('.table').fadeToggle("slow")


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

      $scope.getcontactos = function(contact) 
    {   

        console.log(contact)
        $('#boxContainer').show()

        $scope.name = contact.name
        $scope.id_grupo = contact.id



        $http.get("/grupo/"+contact.id).success(function(response) {

        $scope.clientes = response;
        $scope.search()

        $('#boxContainer').hide()

        console.log($scope.grupo)

    });

    }

    $scope.agregarcontacto = function(contact) 

    {   

        console.log(contact)

        var todo={

            add: "New",
            dato: contact,
            grupo: $scope.id_grupo,
            done:false
        }


        $http({
        url: "/grupos/",
        data: todo,
        method: 'POST',
        headers: {
        'X-CSRFToken': $cookies['csrftoken']
        }
        }).
        success(function(data) {

              swal({   
                title: "Contacto agregado",      
                type: "success",     
                confirmButtonColor: "#46568B",   
                confirmButtonText: "Aceptar",   
                text: data + ' ingresado al sistema',
                closeOnConfirm: false,   
                closeOnCancel: false }, 

                function(isConfirm){ 

                    $('#boxContainer').hide()  
                    if (isConfirm) {     
                        location.reload(true);   
                    } 
                   });

 
        })



    }

        $scope.agregargrupo = function(todo) 

    {   


        $http({
        url: "/addgrupo/",
        data: todo,
        method: 'POST',
        headers: {
        'X-CSRFToken': $cookies['csrftoken']
        }
        }).
        success(function(data) {

              swal({   
                title: "Grupo agregado",      
                type: "success",     
                confirmButtonColor: "#46568B",   
                confirmButtonText: "Aceptar",   
                text: data + ' ingresado al sistema',
                closeOnConfirm: false,   
                closeOnCancel: false }, 

                function(isConfirm){ 

                    $('#boxContainer').hide()  
                    if (isConfirm) {     
                        location.reload(true);   
                    } 
                   });

 
        })



    }

     $scope.sort_by = function(newSortingOrder,currentPage) {

        function sortByKey(array, key) {
            return array.sort(function(a, b) {
            var x = a[key]; var y = b[key];
            return ((x < y) ? -1 : ((x > y) ? 1 : 0));
            });
        }

    
        if ($scope.sortingOrder == newSortingOrder)
            $scope.reverse = !$scope.reverse;

        $scope.sortingOrder = newSortingOrder;

        people = sortByKey($scope.clientes, newSortingOrder);

        if ($scope.reverse){

            console.log($scope.reverse);
            people = sortByKey(people, newSortingOrder).reverse();
            
        }
  
        $scope.clientes = people

        $scope.search()

        // icon setup

        $('th i').each(function(){
            // icon reset
            $(this).removeClass().addClass('icon-sort');
        });
        if ($scope.reverse)
            $('th.'+newSortingOrder+' i').removeClass().addClass('icon-chevron-up');
        else
            $('th.'+newSortingOrder+' i').removeClass().addClass('icon-chevron-down');
    
    };


     $scope.search = function (data) {
    
        var output = {};

        console.log('tipo',data)

        console.log($filter('filter')($scope.clientes,data))

        obj = $filter('filter')($scope.clientes,data)

        $scope.contador = ObjectLength(obj)

        console.log('contador',$scope.contador)

        $scope.filteredItems = $filter('filter')($scope.clientes,data);

        $scope.currentPage = 0;

        $scope.groupToPages();

    };

    function ObjectLength( object ) {
    var length = 0;
    for( var key in object ) {
        if( object.hasOwnProperty(key) ) {
            ++length;
        }
    }
    return length;
    };


    $scope.groupToPages = function () {

        console.log('Grupo')
        $scope.pagedItems = [];
        
        for (var i = 0; i < $scope.filteredItems.length; i++) {
            if (i % $scope.itemsPerPage === 0) {
                $scope.pagedItems[Math.floor(i / $scope.itemsPerPage)] = [ $scope.filteredItems[i] ];
            } else {
                $scope.pagedItems[Math.floor(i / $scope.itemsPerPage)].push($scope.filteredItems[i]);
            }
        }


    };


    $scope.prevPage = function () {
        if ($scope.currentPage > 0) {
            $scope.currentPage--;
        }
    };
    
    $scope.nextPage = function () {
        if ($scope.currentPage < $scope.pagedItems.length - 1) {
            $scope.currentPage++;
        }
    };
    
    $scope.setPage = function () {
        $scope.currentPage = this.n-1;
    };

    
    Todo.$inject = ['$scope', '$filter'];





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

