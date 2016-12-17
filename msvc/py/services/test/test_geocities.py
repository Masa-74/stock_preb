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
gainer_id = 'geocities'

def test(step):

	gainer_module_name = app.config['GAINER_PARAMS'][gainer_id]['data_gainers']
	gainer_module = __import__(gainer_module_name)
	ss_ctl = ss_module.SS_Clt(gainer_id)

	if step == '1':
		try:
			date1 = date(2014, 01, 06)
			date2 = date(2014, 01, 8)
			date3 = date(2016, 06, 24)
			# stock_data_d = gainer_module.get_stock_daily_rawCSV_byDate(date1)
			# print('*** Pass: get_stock_daily_rawCSV_byDate ')
			# stock_data_y = gainer_module.get_stock_daily_rawCS_byYear(date1)
			# print('*** Pass: get_stock_daily_rawCS_byYear')
			# stock_data_list, err_date_list = gainer_module.get_stock_daily_rawCSV_forDate(date1, date2)
			# print('*** Pass: get_stock_daily_rawCSV_forDate')
			# stock_data_list, err_date_list = gainer_module.get_stock_daily_rawCSV_forYear(date1, date3)
			# print('*** Pass: get_stock_daily_rawCSV_forYear')
		except Exception:
			print(traceback.print_exc())
			# raise Exception('<Error in "test_for_dg_geocities()":> ' + sys.exc_info())
			raise Exception(sys.exc_info())

	elif step == '2':
		try:
			# stock_id = '3013'
			date1    = date(2000, 01, 06)
			date2    = date(2015, 01, 07)
			# ss_ctl.isExistDailyStock(stock_id, date1)
			# ss_ctl.isExistDailyStock(stock_id, date1)
			# print('*** Pass: isExistDailyStock ')
			# try:
			# 	ss_ctl.getLatestDate()
			# 	print('*** Pass: getLatestDate ')
			# except EmptyData:
			# 	print('*** Pass: getLatestDate ')

			ss_ctl.loadDailyStock_forYear_fromOnline(date1, date2)
			# print('*** Pass: loadDailyStock_forYear_fromOnline ')
			# ss_ctl.updateDailyStock_fromOnline()
			# print('*** Pass: updateDailyStock_fromOnline ')
		except Exception:
			print(traceback.print_exc())
			# raise Exception('<Error in "test_for_dg_geocities()":> ' + sys.exc_info())
			raise Exception(sys.exc_info())

	elif step == '3':
		try:
			ss_ctl.save_stock_daily_DB()

		except Exception:
			print(traceback.print_exc())
			# raise Exception('<Error in "test_for_dg_geocities()":> ' + sys.exc_info())
			raise Exception(sys.exc_info())

