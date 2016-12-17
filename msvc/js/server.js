var express = require('express')
var db = require('./services/db_manager_util')
var graph_manager = require('./services/graph_manager')
var app = express()
var path = require('path')

app.get('/showGraph', function (req, res) {
  res.send("hello")
  query = {"date":"150106"}
  db.testConnect(query)
})


app.get('/', function (req, res) {
	graph_manager.testChart() 
})


app.listen(3000, function () {
  console.log('Example app listening on port 3000!')
})

