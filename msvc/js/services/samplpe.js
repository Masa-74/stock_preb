var express = require('express')
var db = require('./db_manager_util')
var app = express()

app.get('/', function (req, res) {
  name = db.testConnect()
  res.send('Hello World! ' + name)
})



app.listen(3000, function () {
  console.log('Example app listening on port 3000!')
})