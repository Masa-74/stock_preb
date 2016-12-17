// js/controllers/main.js
angular.module('stockDataController', ['nvd3'])

    // inject the Todo service factory into our controller
    .controller('mainController', function($scope, $http, mainService) {
        // $scope.formData = {};

        /* Chart options */
        $scope.options = {
            chart: {
                type: 'candlestickBarChart',
                height: 450,
                margin : {
                    top: 20,
                    right: 20,
                    bottom: 40,
                    left: 60
                },
                x: function(d){ 

                    singleDate = d['date']
                    var format = d3.time.format("%Y-%m-%d"); // Input date format
                    singleDate_ms = new Date(format.parse(singleDate)).getTime();
                    return (20000 * 86400000 - new Date() + singleDate_ms) / 86400000;
                    // Returning adjasted value based on xAxis calculation

                },
                y: function(d){ return d['close']; },
                duration: 100,

                xAxis: {
                    axisLabel: 'Dates',
                    tickFormat: function(d) {
                        return d3.time.format('%x')(new Date(new Date() - (20000 * 86400000) + (d * 86400000)));
                        // Showing 20000 days from today. According to this, date input from DB has to be adjusted.
                    },
                    showMaxMin: false
                },

                yAxis: {
                    axisLabel: 'Stock Price',
                    tickFormat: function(d){
                        return 'JPY ' + d3.format(',.1f')(d);
                    },
                    showMaxMin: false
                },
                zoom: {
                    enabled: true,
                    scaleExtent: [1, 100],
                    useFixedDomain: false,
                    useNiceScale: false,
                    horizontalOff: false,
                    verticalOff: true,
                    unzoomEventType: 'dblclick.zoom'
                }
            }
        };


        mainService.getStockIds()
            .success(function(data) {
                $scope.stockIds = data
                console.log(data)
            })
            .error(function(data) {
                console.log('Error: ' + data);
            });

        mainService.getYears()
            .success(function(data) {
                $scope.years = data
                console.log(data)
            })
            .error(function(data) {
                console.log('Error: ' + data);
            });


        mainService.get()
            .success(function(data) {

                $scope.data = [{values: data}];
                console.log(data)
            })
            .error(function(data) {
                console.log('Error: ' + data);
            });


        $scope.updateGraph = function() {

            if (!$.isEmptyObject($scope.selectedStockId)) {
                if (!$.isEmptyObject($scope.selectedYear)) {

                    mainService.getBy($scope.selectedStockId, $scope.selectedYear)

                        .success(function(data) {
                            console.log(data)
                            $scope.data = [{values: data}];
                        })
                        .error(function(data) {
                                console.log('Error: ' + data);
                        });
                }
            }
        };

        // // DELETE ==================================================================
        // // delete a todo after checking it
        // $scope.deleteTodo = function(id) {
        //     Todos.delete(id)
        //         // if successful creation, call our get function to get all the new todos
        //         .success(function(data) {
        //             $scope.todos = data; // assign our new list of todos
        //         })
        //         .error(function(data) {
        //                 console.log('Error: ' + data);
        //         });
        // };
    });