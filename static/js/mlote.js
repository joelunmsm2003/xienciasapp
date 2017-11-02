
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

       
  $scope.age=response[0]['status']
    $scope.blaster = response[1]['status'];
    $scope.cdr = response[2]['status'];
    $scope.mail = response[3]['status'];
    $scope.monitoreo = response[4]['status'];
    $scope.sms = response[5]['status'];
    $scope.sup = response[6]['status'];
    $scope.tasky = response[7]['status']



    });



    $scope.a=""
    $scope.b=""

    $('#tog').change(function() {

      $scope.check = $(this).prop('checked')
      console.log($scope.check)
    
    })


     $scope.check ='false'


    var updateChart = function() {

     $http.get("/verlote/").success(function(response) {

        $scope.clientes = response;
        
        $scope.search()

     
    });

    }

    setInterval(function(){updateChart()},1000);


    $http.get("/verlote/").success(function(response) {

        $scope.clientes = response;

        console.log('cli',$scope.clientes)

        $scope.search()

        $('#boxContainer').hide()

         $('header').fadeToggle("slow")
      $('.table').fadeToggle("slow")


    });

    /*

    setInterval(function(){ 

        $http.get("/verlote/").success(function(response) {

        $scope.clientes = response;

        console.log($scope.clientes)

        $scope.search()

        $('.preloader').hide()


    });




    }, 3000);

*/



     $http.get("/user").success(function(response) {

        $scope.user = response[0];

    });

    $http.get("/grupos").success(function(response) {

        $scope.grupos = response;

    });

    $http.get("/audios").success(function(response) {

        $scope.audios = response;

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

    $scope.verlote = function(data) 
    {

    console.log(data)

    window.location.href = "/lote/"+data.cliente__name+"/"+data.lote
    
    };

      $scope.verloteblaster = function(data) 
    {

    console.log(data)

    window.location.href = "/lote/"+4+"/"+data.id
    
    };


    $scope.numberOfPages = function() 
    {

    return Math.ceil($scope.clientes.length / $scope.pageSize);
    
    };

    $scope.blasterindividual=function(data){

        $('#boxContainer').show() 

        $('.modal-backdrop').remove();

        $http({
        url: "/blasterindividual/",
        data: data,
        method: 'POST',
        headers: {
        'X-CSRFToken': $cookies['csrftoken']
        }
        }).
        success(function(data) {

        console.log('exito',data);
        
         $('#boxContainer').hide()

                 swal({   
                title: "Blaster Enviado",      
                type: "success",     
                confirmButtonColor: "#46568B",   
                confirmButtonText: "Aceptar",   
                text: data ,
                closeOnConfirm: false,   
                closeOnCancel: false }, 

                function(isConfirm){ 

            
                    if (isConfirm) {     
                        location.reload(true);   
                    } 
                   });

        })


    };

    

    $scope.agregarlote=function(data){

        $('#boxContainer').show() 

        $('.modal-backdrop').remove();

        var todo={

            add: "Buscar",
            dato: data,
            encuesta:$scope.check,

            done:false
        }

        $http({
        url: "/agregarlote/",
        data: todo,
        method: 'POST',
        headers: {
        'X-CSRFToken': $cookies['csrftoken']
        }
        }).
        success(function(data) {

        console.log('exito',data);
        
        $('#boxContainer').hide()

        swal({   title: 'Lote agregado',   type: "success",  timer: 2000,   showConfirmButton: false });


        $http.get("/verlote/").success(function(response) {

        $scope.clientes = response;

        console.log($scope.clientes)

        $scope.search()

   
        $scope.model =''


        });

     

        })


    };

        $(function(){
        $("#formuploadajax").on("submit", function(e){

            $('#upload').hide();
            $('.modal-backdrop').remove();
            $('#boxContainer').show()

 
  
        

            e.preventDefault();
            var f = $(this);
            var formData = new FormData(document.getElementById("formuploadajax"));
            console.log('formdata',formData)
            formData.append("dato", "valor");
            //formData.append(f.attr("name"), $(this)[0].files[0]);
            $.ajax({
                url: "/uploadaudio/",
                type: "post",
                dataType: "html",
                data: formData,
                cache: false,
                contentType: false,
                processData: false
            })
                .done(function(res){

                    console.log(res)
                    $('#boxContainer').hide()



                 swal({   
                title: "Audio agregado",      
                type: "success",     
                confirmButtonColor: "#46568B",   
                confirmButtonText: "Aceptar",   
                text: res + ' ingresado al sistema',
                closeOnConfirm: false,   
                closeOnCancel: false }, 

                function(isConfirm){ 

                 
                    if (isConfirm) {     
                        //location.reload(true);

                            $http.get("/audios").success(function(response) {

                            $scope.audios = response;

                            });

                         $('.sweet-alert').hide()  
                        $('.sweet-overlay').hide()    
                    } 
                   });
              //location.reload(true); 

                });
        });
    });

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

