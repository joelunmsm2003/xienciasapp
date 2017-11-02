
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



        });

        $('#boxContainer').show()

        $scope.items = [{
        id: 1,
        label: 'Manager',
       
        }, {
        id: 2,
        label: 'User',
        
        }];

        $scope.selected = $scope.items[0];




    $scope.a=""
    $scope.b=""

    //$('.usuarios').hide()

    $http.get("/user").success(function(response) {

        $scope.user = response[0];

        console.log($scope.user)

    });

     $http.get("/appexternas").success(function(response) {

        $scope.clientes = response

        $scope.search()

     

   
    });


     $scope.agregarusuario = function(data) 
    {   
           $('#user').modal('hide')
         $('.modal-backdrop').remove();
         $('#boxContainer').show()

        console.log('$scope.clienteact',$scope.clienteact)

        var todo={

            cliente :$scope.clienteact,
            user:data,
            done:false
        }

        $http({
        url: "/usuarios/",
        data: todo,
        method: 'POST',
        headers: {
        'X-CSRFToken': $cookies['csrftoken']
        }
        }).
        success(function(data) {

            $('#boxContainer').hide()

                 swal({   
                title: "Usuario agregado",      
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




     $scope.getusuarios = function(data) 
    {

        $('.data').hide()

        $scope.clienteact = data

        console.log('----',data)

        $scope.usuariosclientes = ""
        //$('.clientes').hide()

        $scope.usercliente = data.name

        console.log(data)

         $http.get("/usercliente/"+data.id).success(function(response) {

            $scope.usuarios = response

            $('.data').show()

        });

        $http.get("/clientecliente/"+data.id+'/'+data.database).success(function(response) {

            $scope.clientecliente = response

            console.log($scope.clientecliente)

            $('.data').show()



        });

    }
    
     $scope.getusuariosclientes = function(data) 
    {

        
        //$('.clientes').hide()

        $scope.userclientecliente = data.name

        console.log(data)

         $http.get("/userclientecliente/"+data.id).success(function(response) {

            $scope.usuariosclientes = response

            console.log('lll',$scope.usuariosclientes)

            $('.data').show()

        });

    

    }




    $scope.apagar = function() 
    {

        $http.get("/apaga").success(function(response) {

        swal("Xiencias", response)

        });
    };

     $scope.prender = function() 
    {

        $http.get("/lanza").success(function(response) {

        swal("Xiencias", response)

        });
    };



    $scope.prevpag = function() 
    {

        $('.preloader').show()

        $scope.pag = $scope.pag -1

        if ($scope.pag <= -1){

            $scope.pag = 0
        }

        $http.get("/querylote/"+lote+"/"+$scope.pag).success(function(response) {

        $scope.clientes = response;

        $scope.search();

         $('.preloader').hide()

        });
    };


    $scope.nextpag = function() 
    {

         $('.preloader').show()

        $scope.pag = $scope.pag +1

        $http.get("/querylote/"+lote+"/"+$scope.pag).success(function(response) {

        $scope.clientes = response;

        $scope.search();

        $('.preloader').hide()

    });
    
    };


    $http.get("/serviciosapi").success(function(response) {

     

        $scope.blaster = response[0]['status'];
        $scope.cdr = response[1]['status'];
        $scope.monitor = response[2]['status'];

    });

    $('.lote').hide()




    $scope.sortingOrder = sortingOrder;
    $scope.reverse = false;
    $scope.filteredItems = [];
    $scope.groupedItems = [];
    $scope.itemsPerPage = 100;
    $scope.pagedItems = [];
    $scope.currentPage = 0;

    $scope.lote = $('.lote').text()


    $scope.numberOfPages = function() 
    {

    return Math.ceil($scope.clientes.length / $scope.pageSize);
    
    };

    
    $scope.addNew=function(currentPage){

         $('#Agregar').modal('hide')
         $('.modal-backdrop').remove();


        console.log($scope.agregar)
        
        var todo={

            add: "New",
            dato: $scope.agregar,
            done:false
        }


        $http({
        url: "/audiences/",
        data: todo,
        method: 'POST',
        headers: {
        'X-CSRFToken': $cookies['csrftoken']
        }
        }).
        success(function(data) {
        console.log(data);

        window.location.href = "/audience"
        $scope.agregar=""
        })


    };

    $scope.agregar = function (data) {

        $('#external').modal('hide')
        $('.modal-backdrop').remove();

        $('#boxContainer').show()


        console.log(data)

        $http({
        url: "/externaladd/",
        data: data,
        method: 'POST',
        headers: {
        'X-CSRFToken': $cookies['csrftoken']
        }
        }).
        success(function(data) {

    
        console.log(data)

              swal({   
                title: "App agregado",      
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

    $scope.save = function (todo) {

        $('#edit').modal('hide')
        $('.modal-backdrop').remove();


        $http({
        url: "/externalappedit/",
        data: todo,
        method: 'POST',
        headers: {
        'X-CSRFToken': $cookies['csrftoken']
        }
        }).
        success(function(data) {


                swal({   
                title: "External App editado",      
                type: "success",     
                confirmButtonColor: "#46568B",   
                confirmButtonText: "Aceptar",   
                text: data + ' editado',
                closeOnConfirm: false,   
                closeOnCancel: false }, 

                function(isConfirm){ 

         
                    if (isConfirm) {     
                        location.reload(true);   
                    } 
                   });
        
    

        })


   
    };


    $scope.eliminarContact = function (idx,currentPage) {


        $('#Eliminar').modal('hide')
        $('.modal-backdrop').remove();

        console.log($scope.pagedItems[currentPage])

        $scope.pagedItems[currentPage].splice(idx,1);

        var todo={

            dato: $scope.model,

            add: "Eliminar",

            done:false
        }


        $http({
        url: "/audiences/",
        data: todo,
        method: 'POST',
        headers: {
        'X-CSRFToken': $cookies['csrftoken']
        }
        }).
        success(function(data) {

        $scope.contador =$scope.contador -1
        


        })
    };

    $scope.edit = function (contact,index,currentPage) {


        console.log('edit')        
        $scope.index = index;
        $scope.numberPage =currentPage;
        $scope.model = angular.copy(contact);   
        console.log($scope.model);

    };


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


     $scope.search = function () {
    
 
        var output = {};

        console.log($filter('filter')($scope.clientes,$scope.tipo))

        obj = $filter('filter')($scope.clientes,$scope.tipo)

        $scope.contador = ObjectLength(obj)


        $scope.filteredItems = $filter('filter')($scope.clientes,$scope.tipo);
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


        var input =[]

            for (var i = 1; i <= $scope.pagedItems.length; i++) input.push(i);

            $scope.toto = input
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

    
    

}

