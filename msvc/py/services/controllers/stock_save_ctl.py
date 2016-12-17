# -- Load libraries
from db_manager_util import MongoDb as mongoDb
from datetime import datetime, timedelta, date
import sys, traceback
from os import listdir
from os.path import isfile, join
import os.path as osp
import time

# -- Load custome modules
from __init__ import app
from exception_manager_util import EmptyData

class SS_Clt:

	def __init__(self, gainer_id):

		try:
			self.gainer_id 		  = gainer_id
			self.params 		  = app.config['GAINER_PARAMS'][gainer_id]
			self.data_gainers 	  = self.params['data_gainers']
			self.db_id 		  	  = self.params['db_id']
			self.db_columns	  	  = self.params['db_columns']
			# Load target gainer file
			self.gainer = __import__(self.data_gainers)
		except Exception:
			print(traceback.print_exc())
			raise Exception('Invalid <gainer_id>')



	########################################################
	# Check if daily stock data exists
	# Input: 
	#	- stock_id <Type: str>: 
	#	- date     <Type: datetime.date>: 
	########################################################
	def isExistDailyStock(self, stock_id, date):
		try:
			db = mongoDb(self.db_id, app.config['DB_COL_DAILY_STOCK'])
			stock_id_key = self.db_columns['dayily_stock']['stock_id']['field_name']
			date_key 	 = self.db_columns['dayily_stock']['date']['field_name']
			items = db.count_data(
				{
					stock_id_key: stock_id, 
					date_key	: date.strftime(app.config['DB_DATE_FORMAT'])
				})
			if items > 0:
				return True
			else:
				return False
		except Exception:
			# raise Exception('<Error in "isExistDailyStock()":> ' + sys.exc_info())
			print(traceback.print_exc())
			raise Exception(sys.exc_info())


	########################################################
	# Check if daily stock data exists
	# Input: 
	#	- stock_id <Type: str>: 
	#	- date     <Type: datetime.date>: 
	########################################################
	def getLatestDate(self):
		try:
			db = mongoDb(self.db_id, app.config['DB_COL_DAILY_STOCK'])
			field_date = self.db_columns['dayily_stock']['date']['field_name']
			count_data = db.count_data()

			# Raise error if data doesn't exist.
			if count_data == 0:
				raise EmptyData('No data in DB')

			dates_strs = db.distinct(field_date)
			dates = [datetime.strptime(d, app.config['DB_DATE_FORMAT']) for d in dates_strs]

			return max(dates)

		except EmptyData:
			raise EmptyData('No data in DB')
		except Exception:
			# raise Exception('<Error in "getLatestDate()":> ' + sys.exc_info())
			print(traceback.print_exc())
			raise Exception(sys.exc_info())



	########################################################
	# Save data into DB
	# *** [Causion] All fields in each line have to be str. ***
	# Input: 
	#	- input_data <Type: list>: 
	########################################################
	def saveDailyStock(self, input_data):
		try:
			db = mongoDb(self.db_id, app.config['DB_COL_DAILY_STOCK'])
			insert_datas = []
			err_datas = []
			keys = self.db_columns['dayily_stock']
			print('###len_key: ' + str(len(keys)))
			for data_y in input_data: #Each year
				for data_d in data_y: #Each day
					for data_i in data_d: #Each stock_id
						insert_data = {}
						for k in keys: #Each field
							# All fields has to be str, and beable to be decoded by 'utf-8'.
							try:
								insert_data[keys[k]['field_name']] = data_i[keys[k]['order']].decode('utf-8')
							except UnicodeError:
								err_datas.append(data_i)
								continue #Ignore lines which contains invalid field values.
							except Exception:
								data_i.append(str(sys.exc_info()))
								err_datas.append(data_i)

						insert_datas.append(insert_data)
			# Insert data
			db.insert_multiple_data(insert_datas)
			return err_datas
		except Exception:
			# raise Exception('<Error in "saveDailyStock()":> ' + sys.exc_info())
			print(traceback.print_exc())
			raise Exception(sys.exc_info())


	########################################################
	# Load daily stock data btw from_y & to_y from online into DB
	# Input: 
	#	- from_y <Type: datetime.date>: First date
	#	- to_y   <Type: datetime.date>: Last date
	########################################################
	def loadDailyStock_forYear_fromOnline(self, from_y, to_y):
		try:
			data, err_date_list = self.gainer.get_stock_daily_rawCSV_forYear(from_y, to_y)
			print("err_date_list" + str(err_date_list)) #Print error years
			err_datas = self.saveDailyStock(data)
			print("err_datas" + str(err_datas)) #Print error years
		except Exception:
			# raise Exception('<Error in "loadDailyStock_forYear_fromOnline()":> ' + sys.exc_info())
			print(traceback.print_exc())
			raise Exception(sys.exc_info())


	########################################################
	# Load daily stock data btw the date after last update & 
	#  today from online into DB
	# Input: 
	#	- from_y <Type: datetime.date>: First date
	#	- to_y   <Type: datetime.date>: Last date
	########################################################
	def updateDailyStock_fromOnline(self):
		try:
			try:
				latest_date = self.getLatestDate() + timedelta(days=1)
			except EmptyData:
				latest_date = datetime.today() #If no data in DB, get only today's data.
			today = datetime.today()
			data, err_date_list = self.gainer.get_stock_daily_rawCSV_forDate(latest_date, today)
			print("err_date_list" + str(err_date_list)) #Print error years
			err_datas = self.saveDailyStock([data]) #Each line is separated in data, so they have to be gathered in one list.
			print("err_datas" + str(err_datas)) #Print error years

		except Exception:
			print(traceback.print_exc())
			raise Exception(sys.exc_info())


	########################################################
	# Save DB data into file
	# *** [Causion] This function could be failed in specific os.
	# Input: 
	########################################################
	def save_stock_daily_DB(self):
		try:
			#Get date list saved in file
			saved_date_list_path = osp.join(app.config['DATA_DIR'], self.gainer.DB_SAVED_DATE_LIST)
			# If not exist, create file.
			if not osp.exists(saved_date_list_path):
				f = open(saved_date_list_path, 'w+')
				f.close()

			f = open(saved_date_list_path, 'r')
			saved_date_list_raw = f.read()
			f.close()
			saved_date_list = saved_date_list_raw.split('\n')

			#Get dir to save file
			save_dir = osp.join(app.config['DATA_DIR'], self.gainer.DB_SAVED_DAILY)
			save_file = osp.join(save_dir, 'saved_' + datetime.today().strftime('%Y%m%d')) #File name would be 'saved_date' (date is the date of the data)

			#Get date list stored in DB
			db = mongoDb(self.db_id, app.config['DB_COL_DAILY_STOCK'])
			stored_date_list = db.distinct(self.db_columns['dayily_stock']['date']['field_name'])

			#Create saving date list
			saving_date_list = []
			for i in stored_date_list:
				if not i in saved_date_list:
					if saved_date_list != '':
						saving_date_list.append(i)
						saved_date_list.append(i)

			#Create query for saving
			q = [{self.db_columns['dayily_stock']['date']['field_name']: date} for date in saving_date_list]
			q = { '$or': q}

			#Save data and rewrite saved date
			db.save_collection(save_file, q)
			with open(saved_date_list_path, 'w+') as f: #Rewrite saved date
				for i in saved_date_list:
					f.write(str(i) + '\n')

		except Exception:
			print(traceback.print_exc())
			raise Exception(sys.exc_info())












