    var module = angular.module("App", ['ngRoute','elif','ngCookies']);

    host ='http://localhost:8000'

   


    module.config(['$routeProvider',

        function($routeProvider) {

            $routeProvider.

                when('/inicio', {
                    templateUrl: '../inicio',
                    controller: 'Todo'
                }).

                 when('/usuario', {
                    templateUrl: '../usuario',
                    controller: 'Todo'
                }).
               


                otherwise({
                    redirectTo: '/'
                });

        }]);

