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
        stockId = '1301';
        query = { 
            "stock_id": '1301'
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