function Todo($scope,$http,$cookies,$filter) {

    $(".icon-caret-down").hide()
    $(".icon-caret-up").hide()



    var sortingOrder = '-id';

    $('.loading').show()

    $('#alertax').hide()
     $('#report').hide() 
    

    $scope.sortingOrder = sortingOrder;
    $scope.reverse = false;
    $scope.filteredItems = [];
    $scope.groupedItems = [];
    $scope.itemsPerPage = 1000;
    $scope.pagedItems = [];
    $scope.currentPage = 0;

    queryv =0




    $scope.Query = function(){


        $('#Count').hide()
        $('.Count').hide()

        $('#alertax').hide()
        $('.loading').show()

        $('#report').hide()  

        queryv =1


    }



    $scope.search = function () {

    


        String.prototype.capitalizeFirstLetter = function() {
        return this.charAt(0).toUpperCase() + this.slice(1);
        }

 
        var output = {};

        obj = $filter('filter')($scope.clientes,$scope.tipo)

        $scope.contador = ObjectLength(obj)

        $scope.filteredItems = $filter('filter')($scope.clientes,$scope.tipo);
      
        $scope.currentPage = 0;
      
  
        $scope.groupToPages();

    };

              


    $http.get("/costumers").success(function(response) {$scope.costumers = response;
 
    });

    $http.get("/campanias").success(function(response) {$scope.campanias = response;
 
    });

     $http.get("/audiences").success(function(response) {$scope.audiences = response;
 
    });




    $scope.groupToPages = function () {

        
        $scope.pagedItems = [];
        
        for (var i = 0; i < $scope.filteredItems.length; i++) {
            if (i % $scope.itemsPerPage === 0) {
                $scope.pagedItems[Math.floor(i / $scope.itemsPerPage)] = [ $scope.filteredItems[i] ];
            } else {
                $scope.pagedItems[Math.floor(i / $scope.itemsPerPage)].push($scope.filteredItems[i]);
            }
        }

      
    };

    $scope.Change = function () {
        

       

        if ($scope.agregar.elemento == 'costumer'){

            $scope.valores = $scope.costumers

            console.log($scope.valores)
        }

        if ($scope.agregar.elemento == 'audience'){

            $scope.valores = $scope.audiences
        }

        if ($scope.agregar.elemento == 'campaign'){

            $scope.valores = $scope.campanias
        }
        

    };


        $scope.ChangeElement = function () {
        

        console.log($scope.agregar)



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


        $scope.sort_by_m = function(newSortingOrder,currentPage) {


 
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


    numi = 1;
    var est = 0





    
    Todo.$inject = ['$scope', '$filter'];




   
}

