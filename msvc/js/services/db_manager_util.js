var mongoose = require('mongoose');

// Connection URL
db_name = 'kdb_db'
var url = 'mongodb://localhost:27017/' + db_name + '/';
mongoose.connect(url);

var Schema   = mongoose.Schema;
var stockData = new Schema(
	{
	  stock_id: String,
	  date: String,
	  open_rate: String,
	  high_price: String,
	  low_price: String,
	  close_rate: String,
	  other: String
	},
	{ collection : 'stock_data' }
	);
mongoose.model('Stock_data', stockData);



module.exports = { 
	testConnect: function (query) {
		var stockData = mongoose.model('Stock_data');
		stockData.find(query, function(err, docs) {
		  for (var i=0, size=docs.length; i<size; ++i) {
		    console.log(docs[i])
		  }
		});
		// mongoose.connection.db.collection('stock_data', function (err, collection) {
		//     list = collection.find({});
		//     console.log(list[0])
	 //    });
	}
}



