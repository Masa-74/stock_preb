// app/models/stockData.js

    // load mongoose since we need it to define a model
    var mongoose = require('mongoose');
    var Schema   = mongoose.Schema;
	var stockData = new Schema(
		{
		  stock_id: String,
		  date: String,
		  open_rate: Number,
		  high_price: Number,
		  low_price: Number,
		  close_rate: Number,
		  other: Number
		},
		{ collection : 'stock_data' }
		);

    module.exports = mongoose.model('Stock_data', stockData);