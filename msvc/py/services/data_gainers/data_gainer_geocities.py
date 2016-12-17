##############################################################
# Gaining data from the link below.
#  http://www.geocities.co.jp/WallStreet-Stock/9256/data.html
#
##############################################################

# -- Load libraries
from io import BytesIO
from zipfile import ZipFile
import requests
import os, shutil, sys, traceback
import os.path as osp
import ntpath
from datetime import datetime, timedelta, date

# -- Load custome modules
from __init__ import app
import file_manager_util as file_mu
import date_manager_util as date_mu


# -- Data dirs (Path should come after app.config['DATA_DIR'] without initial '/'.)
DB_SAVED_DAILY  = 'geocities/db_saved/stock_daily'
DB_SAVED_DATE_LIST = osp.join(DB_SAVED_DAILY, 'date_list')
RAW_STOCK_DAILY = 'geocities/raw/stock_daily'

# -- Params
url_stock_daily_byYear = {
	'url'		  : 'http://www.geocities.co.jp/WallStreet-Stock/9256/%s.zip', 
	'inputFormat' : '%Y', #date(yyyy)
	'storeDir'	  :	osp.join(RAW_STOCK_DAILY, 'byYear')
	}
url_stock_daily_byDate = {
	'url'		  : 'http://www.geocities.co.jp/WallStreet-Stock/9256/y%s.zip', 
	'inputFormat' : '%y%m%d', #date(yymmdd)
	'storeDir'	  : osp.join(RAW_STOCK_DAILY, 'byDate')
	}




########################################################
# Retrieve stock data list from raw csv file
# Input:
#   - csvFile <Type: file>		   : Target csv file 						  
#	- date    <Type: datetime.date>: Date of the stock data in the csvFile  
########################################################
def retrieve_stock_list_fromRawCSV(csvFile, date):
	try:
		raw_data = csvFile.read()
		# raw_data = csvFile
		# print(raw_data)
		raw_data_list = raw_data.split("\r\n")
		raw_data_list.pop(0)  #1st row is not stok data
		stock_data = []
		for item in raw_data_list:
			data = item.split("\t")
			if len(data) > 1:
				data.pop(1) #ASCII data is in item#1, so remove it.
				data.insert(1, date.strftime(app.config['DB_DATE_FORMAT'])) #Insert date in item#1
				stock_data.append(data)
		return stock_data
	except Exception:
		# raise Exception('<Error in "retrieve_stock_list_fromRawCSV()":> ' + sys.exc_info())
		print(traceback.print_exc())
		raise Exception(sys.exc_info())


########################################################
# Get a raw daily stock data csv by date from online
# Input: 
#	- date <Type: datetime.date>: Target date 
########################################################
def get_stock_daily_rawCSV_byDate(date):
# Output data format: 
#		  - stock_id 	<Type: str>
#		  - date 		<Type: str> *Date format is app.config['DB_DATE_FORMAT'].
#		  - open_rate 	<Type: str>
#		  - high_price 	<Type: str> 
#		  - low_price 	<Type: str> 
#		  - close_rate 	<Type: str> 
#		  - volume 		<Type: str>
	try:
		# Set params
		params 		= url_stock_daily_byDate
		inputFormat = date.strftime(params['inputFormat'])
		url 		= params['url'] % (inputFormat)
		storeDir	= params['storeDir']

		print(url)

		# Download zipFile
		zipfile_path = file_mu.download_zipFile(url, storeDir)

		# Open zipFile
		files, file_paths = file_mu.extract_zipFile(zipfile_path) # file should be only 1

		# Raise error if zipfile has more than 1 file.
		if len(files) > 1:
			raise Exception('Downloaded zipfile contains multiple files: ' + str(file_paths))

		# Retrieve file in list
		file 	  = files[0]
		file_path = file_paths[0]

		# Retrieve stock data from file
		stock_data = retrieve_stock_list_fromRawCSV(file, date)

		# #Remove extracted file
		# os.remove(file_path) 

		return stock_data
	except Exception:
		# raise Exception('<Error in "get_stock_daily_rawCSV_byDate()":> ' + sys.exc_info())
		print(traceback.print_exc())
		raise Exception(sys.exc_info())


########################################################
# Get a raw daily stock data csv by year from online
# Input: 
#	- date <Type: datetime.date>: Target year 
########################################################
def get_stock_daily_rawCSV_byYear(date):
# Output data format: 
#		  - stock_id 	<Type: str>
#		  - date 		<Type: str> *Date format is app.config['DB_DATE_FORMAT'].
#		  - open_rate 	<Type: str>
#		  - high_price 	<Type: str> 
#		  - low_price 	<Type: str> 
#		  - close_rate 	<Type: str> 
#		  - volume 		<Type: str>
	try:
		# Set params
		params 		= url_stock_daily_byYear
		inputFormat = date.strftime(params['inputFormat'])
		url 		= params['url'] % (inputFormat)
		storeDir	= params['storeDir']

		print(url)

		# Download zipFile for year
		zipfile_path_y = file_mu.download_zipFile(url, storeDir)

		# Open zipFile for year and store stock data in a list which will be returned
		stock_data_list = []  #Returned list
		files_y, file_paths_y = file_mu.extract_zipFile(zipfile_path_y) # files_y should be a list of daily files
		for zipfile_path_d in file_paths_y:
			files_d, file_paths_d = file_mu.extract_zipFile(zipfile_path_d) # file should be only 1

			# Raise error if zipfile has more than 1 file.
			if len(files_d) > 1:
				raise Exception('Downloaded zipfile contains multiple files: ' + str(file_paths))

			# Retrieve file in list
			file_d 	 	= files_d[0]
			file_path_d = file_paths_d[0]

			# Get file name from path
			file_name_d = ntpath.basename(file_path_d)

			# Get date
			date_str = file_name_d[1:7] #Retrieve date from file name
			single_date = datetime.strptime(date_str, '%y%m%d')

			# Retrieve stock data from file
			stock_data = retrieve_stock_list_fromRawCSV(file_d, single_date)
			# print('#### stock_data: ' + str(stock_data))
			stock_data_list.append(stock_data)
			os.remove(file_path_d) #Remove extracted file

		return stock_data_list

	except Exception:
		# raise Exception('<Error in "get_stock_daily_rawCS_byYear()":> ' + sys.exc_info())
		print(traceback.print_exc())
		raise Exception(sys.exc_info())


########################################################
# Get a raw daily stock data csv for dates from online
#  ***[Causion] Including both of from_d & to_d data too. ***
# Input: 
#	- from_d <Type: datetime.date>: First date
#	- to_d   <Type: datetime.date>: Last date
########################################################
def get_stock_daily_rawCSV_forDate(from_d, to_d):
# Output data format: 
#	- stock_data_list (Returned list contains stock data):
#		  - stock_id 	<Type: str>
#		  - date 		<Type: str> *Date format is app.config['DB_DATE_FORMAT'].
#		  - open_rate 	<Type: str>
#		  - high_price 	<Type: str> 
#		  - low_price 	<Type: str> 
#		  - close_rate 	<Type: str> 
#		  - volume 		<Type: str>
#	- err_date_list (Returned list contains err date):
#		  - date        <Type: datetime.date>
	try:
		stock_data_list = []  #Returned list contains stock data
		err_date_list = []	  #Returned list contains err date
		for d in date_mu.date_range(from_d, to_d):
			try:
				stock_data_d = get_stock_daily_rawCSV_byDate(d)
				stock_data_list.append(stock_data_d)
			except Exception:
				err_date_list.append(d)
				continue
		return stock_data_list, err_date_list
	except Exception:
		# raise Exception('<Error in "get_stock_daily_rawCSV_forDate()":> ' + sys.exc_info())
		print(traceback.print_exc())
		raise Exception(sys.exc_info())


########################################################
# Get a raw daily stock data csv for years from online
#  ***[Causion] Including both of from_y & to_y data too. ***
# Input: 
#	- from_y <Type: datetime.date>: First date
#	- to_y   <Type: datetime.date>: Last date
########################################################
def get_stock_daily_rawCSV_forYear(from_y, to_y):
# Output data format: 
#	- stock_data_list (Returned list contains stock data):
#		  - stock_id 	<Type: str>
#		  - date 		<Type: str> *Date format is app.config['DB_DATE_FORMAT'].
#		  - open_rate 	<Type: str>
#		  - high_price 	<Type: str> 
#		  - low_price 	<Type: str> 
#		  - close_rate 	<Type: str> 
#		  - volume 		<Type: str>
#	- err_year_list (Returned list contains err year):
#		  - year        <Type: int>
	try:
		stock_data_list = []  #Returned list contains stock data
		err_year_list = []	  #Returned list contains err year
		for y in date_mu.year_range(from_y, to_y):
			try:
				y = date(y, 01, 01)  #Convert integer y into datetime.date y
				stock_data_y = get_stock_daily_rawCSV_byYear(y)
				stock_data_list.append(stock_data_y)
			except Exception:
				err_year_list.append(y)
				continue
		return stock_data_list, err_year_list #Return stock data separated in year year (e.x. [[year1], [year2], ...])
	except Exception:
		# raise Exception('<Error in "get_stock_daily_rawCSV_forYear()":> ' + sys.exc_info())
		print(traceback.print_exc())
		raise Exception(sys.exc_info())








