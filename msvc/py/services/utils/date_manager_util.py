# -- Load libraries
from datetime import timedelta, date
import os, sys, traceback


########################################################
# Get a daily range from start_date to end_date.
#  The range includes start_date and end_date too.
# Input: 
#	- start_date <Type: datetime.date>:
#	- end_date   <Type: datetime.date>:
# Output:
#	- <Type: list of datetime.date>:
########################################################
def date_range(start_date, end_date):
	try:
		end_date = end_date + timedelta(days=1)
		for n in range(int ((end_date - start_date).days)):
			yield start_date + timedelta(n)
	except Exception:
		# raise Exception('<Error in "date_range()":> ' + sys.exc_info())
		print(sys.exc_info())
		raise Exception(sys.exc_info())


########################################################
# Get a yearly range from start_date to end_date.
#  The range includes start_year and end_year too.
#  Only year info is retrieved from input.
#   (Ex1. start_date='2010.01.01', 
#	 	  end_date  ='2010.03.01'    => Output[2010])
#   (Ex2. start_date='2010.12.31', 
#		  end_date  ='2012.01.01'    => Output[2010, 2011, 2012])
# Input: 
#	- start_year <Type: datetime.date>:
#	- end_year   <Type: datetime.date>:
# Output:
#	- <Type: list of datetime.date>:
########################################################
def year_range(start_date, end_date):
	try:
		start_year_int = int(start_date.strftime('%Y'))
		end_year_int = int(end_date.strftime('%Y')) + 1
		for n in range(start_year_int, end_year_int):
			yield n
	except Exception:
		# raise Exception('<Error in "year_range()":> ' + sys.exc_info())
		print(sys.exc_info())
		raise Exception(sys.exc_info())





		