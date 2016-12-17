import urllib2
from datetime import datetime, timedelta, date

url_Kobetsu_Megara = 'http://k-db.com/stocks/?download=csv'
url_stock_data_1d = 'http://k-db.com/stocks/%s/1d/%s?download=csv' # $0:id, $1:year(2016-2013)
url_stock_data_1h = 'http://k-db.com/stocks/%s/1h/%s?download=csv'    # $0:id (201611-201608)


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


def get_stock_info_1h(stock_id, yyyymm=''):
	# Output: 'date(yyyy-mm-dd)', 'time', 'open_rate', 'high_price', 'low_price', 'close_rate', 'volume', 'turnover'
	url = url_stock_data_1h % (stock_id, yyyymm)
	response = urllib2.urlopen(url)
	stock_data_raw = response.read()
	stock_data_csv = stock_data_raw.split("\r\n")
	stock_data_csv.pop(0)
	stock_data = map(lambda x: x.split(','), stock_data_csv)
	return stock_data

def get_stock_info_1d(stock_id, yyyy=''):
	# Output: 'date(yyyy-mm-dd)', 'open_rate', 'high_price', 'low_price', 'close_rate', 'volume', 'turnover'
	url = url_stock_data_1d % (stock_id, yyyy)
	response = urllib2.urlopen(url)
	stock_data_raw = response.read()
	stock_data_csv = stock_data_raw.split("\r\n")
	stock_data_csv.pop(0)
	stock_data = map(lambda x: x.split(','), stock_data_csv)
	return stock_data

# Don't use it at the very first day of the month, otherwise, you cannot get any info.
def get_whole_stock_info_1h():
	whole_stock_info = []
	stock_id_list = get_stock_id()
	for stock_id in stock_id_list:
		print("Retrieve data: " + stock_id)
		hasValidData = 1
		today_date = datetime.today()
		target_date = date(day=1, month=today_date.month, year=today_date.year)
		while (hasValidData):
			yyyymm = target_date.strftime('%Y%m')
			stock_info_list = get_stock_info_1h(stock_id, yyyymm)
			retrieved_date = stock_info_list[0][0].split('-')
			retrieved_yyyymm = str(retrieved_date[0]) + str(retrieved_date[1])
			if retrieved_yyyymm != str(yyyymm):
				hasValidData = 0
			else:
				for stock_info in stock_info_list:
					if len(stock_info) == 8: #The number of items is 8
						stock_info.insert(0, stock_id)
						whole_stock_info.append(stock_info)
					else:
						continue
				print("Retrieve date: " + str(yyyymm))
				previous_date = target_date - timedelta(days=1)
				target_date = date(day=1, month=previous_date.month, year=previous_date.year)
	return whole_stock_info

# Don't use it at the very first day of the year, otherwise, you cannot get any info.
def get_whole_stock_info_1d():
	whole_stock_info = []
	stock_id_list = get_stock_id()
	for stock_id in stock_id_list:
		print("Retrieve data: " + stock_id)
		hasValidData = 1
		y = datetime.now().year #Retrieve current date's year
		while (hasValidData):
			stock_info_list = get_stock_info_1d(stock_id, y)
			retrieved_date = stock_info_list[0][0].split('-')
			if retrieved_date[0] != str(y):
				hasValidData = 0
			else:
				for stock_info in stock_info_list:
					if len(stock_info) == 7: #The number of items is 7
						stock_info.insert(0, stock_id)
						whole_stock_info.append(stock_info)
					else:
						continue
				print("Retrieve date: " + str(y))
				y = y - 1
	return whole_stock_info





if __name__ == '__main__':
	# stock_id_list = get_stock_id()
	# print(stock_id_list[0])
	# stock_info_1h = get_stock_info_1h(stock_id_list[0], '201609')
	# stock_info_1d = get_stock_info_1d(stock_id_list[0], '2011')

	# print(stock_info_1h[0])
	# print(stock_info_1d[0][0])
	result = get_whole_stock_info_1d()
	print(len(result))
	print(result[0])
	# result = get_whole_stock_info_1h()
	# print(len(result))
	# print(result[0])








