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
                    var format = d3.time.format("%y%m%d"); // Input date format
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
                        return '$' + d3.format(',.1f')(d);
                    },
                    showMaxMin: false
                },
                zoom: {
                    enabled: true,
                    scaleExtent: [1, 10],
                    useFixedDomain: false,
                    useNiceScale: false,
                    horizontalOff: false,
                    verticalOff: true,
                    unzoomEventType: 'dblclick.zoom'
                }
            }
        };


        // // $scope.data = [{values: []}]
        // $scope.data = [{values: [
        //     {"date": 0, "open": 165.42, "high": 165.8, "low": 164.34, "close": 165.22, "volume": 160363400, "adjusted": 164.35},
        //     {"date": 1, "open": 165.42, "high": 165.8, "low": 164.34, "close": 165.22, "volume": 160363400, "adjusted": 164.35}]}]
 


        // GET =====================================================================
        // when landing on the page, get all todos and show them
        // use the service to get all the todos
        mainService.get()
            .success(function(data) {

                $scope.data = [{values: data}];
                console.log(data)
            })
            .error(function(data) {
                    console.log('Error: ' + data);
            });

        // // CREATE ==================================================================
        // // when submitting the add form, send the text to the node API
        // $scope.createTodo = function() {

        //     // validate the formData to make sure that something is there
        //     // if form is empty, nothing will happen
        //     // people can't just hold enter to keep adding the same to-do anymore
        //     if (!$.isEmptyObject($scope.formData)) {

        //         // call the create function from our service (returns a promise object)
        //         Todos.create($scope.formData)

        //             // if successful creation, call our get function to get all the new todos
        //             .success(function(data) {
        //                 $scope.formData = {}; // clear the form so our user is ready to enter another
        //                 $scope.todos = data; // assign our new list of todos
        //             })
	       //          .error(function(data) {
	       //                  console.log('Error: ' + data);
	       //          });
        //     }
        // };

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