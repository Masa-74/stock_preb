import urllib2

url_Kobetsu_Megara = 'http://k-db.com/stocks/?download=csv'
url_stock_data_1d = 'http://k-db.com/stocks/%s/1d/%s?download=csv' # $0:id, $1:year(2016-2013)
url_stock_data_1h = 'http://k-db.com/stocks/%s/1h?download=csv'    # $0:id (201611-201608)


def get_stock_id():
	response = urllib2.urlopen(url_Kobetsu_Megara)
	raw_data = response.read()
	csv_data = raw_data.split("\r\n")
	csv_data.pop(0)
	stock_id_list = []
	for row in csv_data:
		current_stock_id = row.split(',')
		stock_id_list.append(current_stock_id[0])
	return stock_id_list

def get_stock_info_1h(stock_id):
	url = url_stock_data_1h % stock_id
	print(url)
	response = urllib2.urlopen(url)
	stock_data_raw = response.read()
	stock_data_csv = stock_data_raw.split("\r\n")
	return stock_data_csv

def get_stock_info_1d(stock_id, year):
	url = url_stock_data_1d % (stock_id, year)
	print(url)
	response = urllib2.urlopen(url)
	stock_data_raw = response.read()
	stock_data_csv = stock_data_raw.split("\r\n")
	return stock_data_csv









