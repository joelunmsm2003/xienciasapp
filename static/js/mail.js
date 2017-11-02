
    var myApp=angular.module('myApp', ['ngCookies']);
    myApp.config(function($interpolateProvider){
    $interpolateProvider.startSymbol('{[{').endSymbol('}]}');
    });

    var sortingOrder = '-id';


function Todo($scope,$http,$cookies,$filter) {


        $(function(){

        $("#formuploadajax").on("submit", function(e){

            $('#grupo').hide();
            $('.modal-backdrop').remove();
            $('.preloader').show()

            e.preventDefault();
            var f = $(this);
            var formData = new FormData(document.getElementById("formuploadajax"));
            console.log('formdata',formData)
            formData.append("dato", "valor");
 
            $.ajax({
                url: "/upbase/",
                type: "post",
                dataType: "html",
                data: formData,
                cache: false,
                contentType: false,
                processData: false
            })
                .done(function(res){


                $http.get("/grupos").success(function(response) {

                $scope.grupos = response;

                });

                $('.preloader').hide()

                $scope.rbase = ''


                swal({   
                title: "Base agregado",      
                type: "success",     
                confirmButtonColor: "#46568B",   
                confirmButtonText: "Aceptar",  

                text: res + ' ingresado al sistema',
                closeOnConfirm: false,   
                closeOnCancel: false }, 

                function(isConfirm){ 

                     
                    if (isConfirm) {     
                        $('.sweet-alert').hide()  
                        $('.sweet-overlay').hide()  
                    } 
                   });

                    



                    //window.location.href = '/lote/'+data.database+'/'+data.nombre;
                });
        });
    });

$scope.agregar = function(data) 

    {   
         
         $('#campa').hide();
         $('.modal-backdrop').remove();
         $('.preloader').show()



        var todo={

            dato :data,
            user:$scope.user,
            done:false
        }

        $http({
        url: "/agregarcampania/",
        data: todo,
        method: 'POST',
        headers: {
        'X-CSRFToken': $cookies['csrftoken']
        }
        }).
        success(function(data) {


            $http.get("/campaniasms").success(function(response) {

            $scope.campanias = response;
            });


            $('.preloader').hide()

                 swal({   
                title: "Campaña SMS agregada",      
                type: "success",     
                confirmButtonColor: "#46568B",   
                confirmButtonText: "Aceptar",   
                text: data + ' ingresado al sistema',
                closeOnConfirm: false,   
                closeOnCancel: false }, 

                function(isConfirm){ 

                
                    if (isConfirm) {     
                        $('.sweet-alert').hide()  
                        $('.sweet-overlay').hide()    
                    } 
                   });

        })


    }





     $http.get("/serviciosapi").success(function(response) {

        console.log('servicio',response[0]['status'])

     $scope.blaster = response[0]['status'];
    $scope.cdr = response[1]['status'];
    $scope.monitor = response[2]['status'];
    $scope.sms = response[3]['status'];
    $scope.mail = response[4]['status'];

    });

     $('.preloader').show()




    $scope.a=""
    $scope.b=""

    $('#tog').change(function() {

      $scope.check = $(this).prop('checked')
      console.log($scope.check)
    
    })


     $scope.check ='false'


        $http.get("/verlotesms/").success(function(response) {

        $scope.clientes = response;

        console.log($scope.clientes)

        $scope.search()

        $('.preloader').hide()






    });



    setInterval(function(){ 

        $http.get("/verlotesms/").success(function(response) {

        $scope.clientes = response;

        console.log($scope.clientes)

        $scope.search()




    });




    }, 3000);



     $http.get("/user").success(function(response) {

        $scope.user = response[0];

    });

    $http.get("/grupos").success(function(response) {

        $scope.grupos = response;

    });



     $http.get("/campaniasms").success(function(response) {

        $scope.campanias = response;
    });



    


    $scope.sortingOrder = sortingOrder;
    $scope.reverse = false;
    $scope.filteredItems = [];
    $scope.groupedItems = [];
    $scope.itemsPerPage = 50;
    $scope.pagedItems = [];
    $scope.currentPage = 0;

    $scope.lote = $('.lote').text()

    /*

     var todo={

            lote: $scope.lote,
            username: 'beyond',
            password:123,
            done:false
        }


        $http({
        url: "/consultalote/",
        data: todo,
        method: 'POST',
        headers: {
        'X-CSRFToken': $cookies['csrftoken']
        }
        }).
        success(function(data) {

            $scope.clientes = data;
           
            $scope.fechainicio = data[0]['fh_inicio']

            $scope.search();

    
    })


    */

    $scope.verlotesms = function(data) 
    {

    console.log('ver',data)

    window.location.href = "/lotesms/"+data.user__cliente__name+"/"+data.id
    
    };



    $scope.numberOfPages = function() 
    {

    return Math.ceil($scope.clientes.length / $scope.pageSize);
    
    };

    

    $scope.agregarsms=function(data){

        
        $('.modal-backdrop').remove();
        $('.preloader').show()

        console.log('agregarlote',data)

          var todo={

            dato: data,
            done:false
        }




        $http({
        url: "/enviosms/",
        data: todo,
        method: 'POST',
        headers: {
        'X-CSRFToken': $cookies['csrftoken']
        }
        }).
        success(function(data) {

        console.log('exito',data);
        
         $('#boxContainer').hide()

                 swal({   
                title: "Lote agregado",      
                type: "success",     
                confirmButtonColor: "#46568B",   
                confirmButtonText: "Aceptar",   
                text: data + ' ingresado al sistema',
                closeOnConfirm: false,   
                closeOnCancel: false }, 

                function(isConfirm){ 

                  
                    if (isConfirm) {     
                        $('.sweet-alert').hide()  
                        $('.sweet-overlay').hide()
                        $('.preloader').hide()   
                    } 
                   });

        })


    };

    $scope.saveContact = function (idx,currentPage) {


        $scope.pagedItems[currentPage][idx] = angular.copy($scope.model);
       

        var todo={

            add: "Edit",
            dato: $scope.model,
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

     
        $scope.model.costumer__short_name = data['cliente'];
        
        console.log($scope.model)
      

        })


        $('#Edit').modal('hide')
        $('.modal-backdrop').remove();
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

    $scope.editContact = function (contact,index,currentPage) {


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
        $scope.currentPage = this.n;
    };

    
    Todo.$inject = ['$scope', '$filter'];

    
    

}

