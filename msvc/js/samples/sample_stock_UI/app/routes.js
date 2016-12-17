// app/routes.js

// load the todo model
var stockData = require('./models/stockData');


// expose the routes to our app with module.exports
module.exports = function(app) {


// routes ======================================================================

    // api ---------------------------------------------------------------------
    // get all todos
    app.get('/getStockData', function(req, res) {

        // stockId = req.query.color;
        // stockId = '1301';
        // stockId = '6176';
        stockId = '3453';
        query = { 
            "stock_id": stockId
        }
        fields = {
            "_id": 0,
            "stock_id": 0
        }
        console.log("Requet stock ID: " + stockId)

        stockData.find(query, fields, function(err, data) {
            
            if (err)
                res.send(err)

            res.json(data);

            // for (var i=0, size=docs.length; i<size; ++i) {
            //     console.log(data[i])
            // }

        });

    });

    app.get('/getStockIds', function(req, res) {

        stockData.aggregate(
            [
                {"$unwind": "$stock_id" } ,
                { "$group": { _id: '$stock_id' }},
                { "$sort": { "stock_id": -1 }}
            ])
            // .limit(200)
            .exec(function(err, data) {
            
                if (err)
                    res.send(err)

                // console.log(data)
                res.json(data);

        });

        // stockData
        //     .find()
        //     .distinct('stock_id')
        //     .limit(20)
        //     .exec(function(err, data) {
            
        //         if (err)
        //             res.send(err)

        //         console.log(data)
        //         res.json(data);

        // })

    });


    app.get('/getYears', function(req, res) {

        // stockData.aggregate(
        //     [
        //         { "$group": { _id: '$stock_id' }},
        //         { "$sort": { "stock_id": -1 }}
        //     ],
        //     function(err, data) {
            
        //         if (err)
        //             res.send(err)

        //         // console.log(data)
        //         res.json(data);

        // });
        stockData.find().distinct('date', function(err, data) {
            
                if (err)
                    res.send(err)

                output = []
                for (var i=0; i<data.length; i++){
                    data_y = data[i].substring(0,4) // Be careful for data structure.
                    if(output.indexOf(data_y) < 0){
                        output.push(data_y)  // Be careful for data structure.
                    }
                }
                res.json(output);

        })

    });


    app.get('/getStockDataBy/:id/:year', function(req, res) {

        stockId = req.param('id');
        year = req.param('year');
        // stockId = '1301';
        query = { 
            "stock_id": stockId
            // "date": new RegExp('^'+year+'.*', 'i')
        }
        fields = {
            "_id": 0,
            "stock_id": 0
        }
        console.log("Requet stock ID: " + stockId)
        console.log("Requet year: " + '^'+year+'.*')

        stockData.find(query, fields, function(err, data) {
            
            if (err)
                res.send(err)

            console.log(data)
            res.json(data);

            // for (var i=0, size=docs.length; i<size; ++i) {
            //     console.log(data[i])
            // }

        });

    });


    // // create todo and send back all todos after creation
    // app.post('/api/todos', function(req, res) {

    //     // Do something

    // });

    // // delete a todo
    // app.delete('/api/todos/:todo_id', function(req, res) {
        
    //     // Do something

    // });

    // application -------------------------------------------------------------
    app.get('/', function(req, res) {
        res.sendfile('./public/index.html'); // load the single view file (angular will handle the page changes on the front-end)
    });

}