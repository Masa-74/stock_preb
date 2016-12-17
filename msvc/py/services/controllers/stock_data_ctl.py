# # -- Load libraries
# from db_manager_util import MongoDb as mongoDb
# from datetime import datetime, timedelta, date
# import sys, traceback
# from os import listdir
# from os.path import isfile, join
# import os.path as osp
# import time

# # -- Load custome modules
# from __init__ import app
# from exception_manager_util import EmptyData


# class SD_Clt:


# 	def __init__(self, gainer_id, data_type):

# 		try:
# 			self.gainer_id 		  = gainer_id
# 			self.datatype 		  = data_type
# 			self.params 		  = app.config['GAINER_PARAMS'][gainer_id]
# 			self.data_gainers 	  = self.params['data_gainers']
# 			self.db_id 		  	  = self.params['db_id']
# 			self.db_columns	  	  = self.params['db_columns']
# 			self.db_columns 	  = self.db_columns[self.datatype]
# 			# Load target gainer file
# 			self.gainer = __import__(self.data_gainers)
# 		except Exception:
# 			print(traceback.print_exc())
# 			raise Exception('Invalid <gainer_id>')

# 	def getData(query1={}, qurery2={}):
		


