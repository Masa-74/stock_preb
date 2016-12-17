// js/services/todos.js
angular.module('stockDataService', [])

    // super simple service
    // each function returns a promise object 
    .factory('mainService', function($http) {
        return {
            get : function() {
                return $http.get('/getStockData');
            }
        }
    });