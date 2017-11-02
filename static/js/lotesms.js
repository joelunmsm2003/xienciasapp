
    var myApp=angular.module('myApp', ['ngCookies']);
    myApp.config(function($interpolateProvider){
    $interpolateProvider.startSymbol('{[{').endSymbol('}]}');
    });

    var sortingOrder = '-id';


function Todo($scope,$http,$cookies,$filter) {

    $scope.a=""
    $scope.b=""

    $http.get("/user").success(function(response) {

        $scope.user = response[0];
 

    });

    lote = window.location.href.split("/")[5]

    $scope.lotename = lote



    $scope.database = window.location.href.split("/")[4]

    console.log('database',$scope.database,lote)

    $http.get("/infolote/"+lote).success(function(response) {

        $scope.name = response[0].name
    

    })


    $scope.pag  = 0

    $http.get("/querylotesms/"+$scope.database+"/"+lote+"/"+$scope.pag).success(function(response) {

        $scope.clientes = response;

        $scope.search();

        $('.preloader').hide()

         $('header').fadeToggle("slow")
      $('.table').fadeToggle("slow")

    });

    var updateChart = function() {

        $http.get("/querylotesms/"+$scope.database+"/"+lote+"/"+$scope.pag).success(function(response) {

        $scope.clientes = response;


        $scope.search();

        $('.preloader').hide()

    });


    }

    setInterval(function(){updateChart()},1000);



    $scope.prevpag = function() 
    {

        $('.preloader').show()

        $scope.pag = $scope.pag -1

        if ($scope.pag <= -1){

            $scope.pag = 0
        }

        $http.get("/querylotesms/"+lote+"/"+$scope.pag).success(function(response) {

        $scope.clientes = response;

        $scope.search();

         $('.preloader').hide()

        });
    };


    $scope.nextpag = function() 
    {

         $('.preloader').show()

        $scope.pag = $scope.pag +1

        $http.get("/querylotesms/"+lote+"/"+$scope.pag).success(function(response) {

        $scope.clientes = response;

        $scope.search();

        $('.preloader').hide()

    });
    
    };


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

    $('.lote').hide()

    $scope.sortingOrder = sortingOrder;
    $scope.reverse = false;
    $scope.filteredItems = [];
    $scope.groupedItems = [];
    $scope.itemsPerPage = 30;
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

      $scope.enviarlote=function(){

        $('#enviarlote').modal('hide')
        $('.modal-backdrop').remove();

    $http.get("/enviarlotesms/"+lote).success(function(response) {


swal({     title: "Lote enviado",   type: "success",   confirmButtonColor: "#324994",   confirmButtonText: "Cerrar",   }, function(){   });



        
    });



        


    };


    $scope.cancelarlote=function(currentPage){

                $('#cancelarlote').modal('hide')
        $('.modal-backdrop').remove();

         $http.get("/cancelarlotesms/"+lote).success(function(response) {

        swal({     title: "Lote cancelado",   type: "success",   confirmButtonColor: "#324994",   confirmButtonText: "Cerrar",   }, function(){   });




    });

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

    $scope.descarga = function () {

        console.log('jsjsjsjsj')
        window.location.href = "/descargacsvlote/"+lote



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

