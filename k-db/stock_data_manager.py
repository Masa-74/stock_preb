import get_stock_data as getSD
from db_util_manager import MongoDb as mongoDb

def save_whole_stock_data_1d():
	whole_stock_info_1d = getSD.get_whole_stock_info_1d()
	insert_jsons = []
	for stock_info_1d in whole_stock_info_1d:
		stock_info_1d_json = {}
		#'date(yyyy-mm-dd)', 'open_rate', 'high_price', 'low_price', 'close_rate', 'volume', 'turnover'
		stock_info_1d_json['stock_id'] = stock_info_1d[0]
		stock_info_1d_json['date'] = stock_info_1d[1]
		stock_info_1d_json['open_rate'] = stock_info_1d[2]
		stock_info_1d_json['high_price'] = stock_info_1d[3]
		stock_info_1d_json['low_price'] = stock_info_1d[4]
		stock_info_1d_json['close_rate'] = stock_info_1d[5]
		stock_info_1d_json['volume'] = stock_info_1d[6]
		stock_info_1d_json['turnover'] = stock_info_1d[7]
		insert_jsons.append(stock_info_1d_json)

	db = mongoDb('kdb_db', 'stock_data_1d')
	db.insert_multiple_data(insert_jsons)
	db.save_collection('./data/kdb_stock_data_1d')
	db.drop_collection()


if __name__ == '__main__':
	save_whole_stock_data_1d()