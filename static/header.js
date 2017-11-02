
var myApp=angular.module('Header', ['ngCookies']);
myApp.config(function($interpolateProvider){
$interpolateProvider.startSymbol('{[{').endSymbol('}]}');
});

var sortingOrder = '-id';



function Todo($scope,$http,$cookies,$filter) {


    $scope.sortingOrder = sortingOrder;
    $scope.reverse = false;
    $scope.filteredItems = [];
    $scope.groupedItems = [];
    $scope.itemsPerPage = 10;
    $scope.pagedItems = [];
    $scope.currentPage = 0;


    $http.get("/serviciosapi").success(function(response) {

    console.log('servicio',response[0]['status'])

    $scope.blaster = response[0]['status'];
    $scope.cdr = response[1]['status'];
    $scope.monitor = response[2]['status'];
    $scope.sms = response[3]['status'];
    $scope.mail = response[4]['status'];

    });

    $http.get("/appexternas").success(function(response) {


        $scope.appexternas = response


    });

    

  
    


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

