# -- Load libraries
from io import BytesIO
from zipfile import ZipFile
import requests
import os, sys, traceback
import os.path as osp

# -- Load custome modules
from __init__ import app

# Download zipFile 
#  from url into path(osp.join(app.config['DATA_DIR'], path_fromDataDir))
#  and return the zipFile path
def download_zipFile(url, path_fromDataDir):
	try:
		data_dir = osp.join(app.config['DATA_DIR'], path_fromDataDir)
		# Create dir if not exist.
		if not os.path.exists(data_dir):
			os.makedirs(data_dir)
		os.chdir(data_dir)
		response = requests.get(url)
		zipfile_path = BytesIO(response.content)
		return zipfile_path
	except Exception:
		# raise Exception('<Error in "download_zipFile()":> ' + sys.exc_info())
		raise Exception(sys.exc_info())


# Extract all files in input zipFile,
#  return all file obj and path
def extract_zipFile(zipfile_path):
	try:
		zipfile = ZipFile(zipfile_path)
		file_name_list = zipfile.namelist()
		files = []
		file_paths = []
		for f in file_name_list:
			file_path = zipfile.extract(f)
			file = open(file_path, 'r')
			files.append(file)
			file_paths.append(file_path)
		return files, file_paths
	except Exception:
		# raise Exception('<Error in "extract_zipFile()":> ' + sys.exc_info())
		raise Exception(sys.exc_info())
