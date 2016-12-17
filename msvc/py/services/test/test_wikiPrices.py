# -- Load libraries
from io import BytesIO
from zipfile import ZipFile
import requests
import os, shutil, sys, traceback
import os.path as osp
import ntpath
from datetime import datetime, timedelta, date

# -- Load custome modules --
from __init__ import app
from exception_manager_util import EmptyData
import stock_save_ctl as ss_module

# -- Gainer id for test--
gainer_id = 'wikiPrices'

def test(step):

	gainer_module_name = app.config['GAINER_PARAMS'][gainer_id]['data_gainers']
	gainer_module = __import__(gainer_module_name)
	ss_ctl = ss_module.SS_Clt(gainer_id)


	if step == '1':
		try:
			date1 = date(2014, 01, 06)
			date2 = date(2014, 01, 8)
			date3 = date(2016, 06, 24)

			# retrieved_data = gainer_module.retrieve_stock_list_fromRawCSVLocal()
			# for i in range(0,3):
			# 	print(retrieved_data[i])
			# print('*** Pass: retrieve_stock_list_fromRawCSVLocal ')

			return_list, err_list = gainer_module.get_stock_daily_rawCSV_forYear(date1, date3)


			print(len(return_list))
			print(len(err_list))

			for i in range(0, 3):
				print(return_list[i])

			print('*** Pass: get_stock_daily_rawCSV_forYear')
			# stock_data_list, err_date_list = target.get_stock_daily_rawCSV_forDate(date1, date2)
			# print('*** Pass: get_stock_daily_rawCSV_forDate')
			# stock_data_list, err_date_list = target.get_stock_daily_rawCSV_forYear(date1, date3)
			# print('*** Pass: get_stock_daily_rawCSV_forYear')
		except Exception:
			print(traceback.print_exc())
			# raise Exception('<Error in "test_for_dg_geocities()":> ' + sys.exc_info())
			raise Exception(sys.exc_info())



	elif step == '2':
		try:
			print('test 2 start')
			# stock_id = '3013'

			for i in range(1999, 2016):
				date1    = date(i, 01, 01)
				date2    = date(i, 01, 31)
				ss_ctl.loadDailyStock_forYear_fromOnline(date1, date2)
				print('*** Pass: loadDailyStock_forYear_fromOnline: ' + str(i))

		except Exception:
			print(traceback.print_exc())
			# raise Exception('<Error in "test_for_dg_geocities()":> ' + sys.exc_info())
			raise Exception(sys.exc_info())

