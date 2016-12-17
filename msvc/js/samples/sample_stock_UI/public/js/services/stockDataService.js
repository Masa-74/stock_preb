// js/services/todos.js
angular.module('stockDataService', [])

    // super simple service
    // each function returns a promise object 
    .factory('mainService', function($http) {
        return {
            get : function() {
                return $http.get('/getStockData');
            },
            getStockIds : function() {
            	return $http.get('/getStockIds');
            },
            getYears : function() {
                return $http.get('/getYears');
            },
            getBy : function(stockId, year) {
                return $http.get('/getStockDataBy/' + stockId + "/" + year);
            }
        }
    });