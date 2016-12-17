# -- Load libraries
from pymongo import MongoClient
import datetime
import os
import json
# -- Load custome modules
from __init__ import app


class MongoDb:

	def __init__(self, db_id, collection_id):
		self.client = MongoClient(app.config['DB_PATH'])
		self.db_id = db_id
		self.collection_id = collection_id

	def insert_data(self, json):
		db = self.client[self.db_id]
		collection = db[self.collection_id]
		post_id = collection.insert_one(json)

	def insert_multiple_data(self, json_list):
		db = self.client[self.db_id]
		collection = db[self.collection_id]
		post_id = collection.insert_many(json_list)

	def count_data(self, json = {}):
		db = self.client[self.db_id]
		collection = db[self.collection_id]
		return collection.count(json)

	def find_data(self, json1 = {}, json2 = {}):
		db = self.client[self.db_id]
		collection = db[self.collection_id]
		return collection.find(json1, json2)

	def distinct(self, key):
		db = self.client[self.db_id]
		collection = db[self.collection_id]
		return collection.distinct(key)

	def delete_data(self, json = {}):
		db = self.client[self.db_id]
		collection = db[self.collection_id]
		post_id = collection.delete_many(json)

	def drop_collection(self):
		db = self.client[self.db_id]
		collection = db[self.collection_id]
		collection.drop()

	def save_collection(self, save_file, query={}):
		db = self.client[self.db_id]
		collection = db[self.collection_id]
		data = collection.find(query, {'_id':0})
		with open(save_file, 'w+') as outfile:
			for doc_json in data:
				doc = json.dumps(doc_json)
				outfile.write(doc + '\n')
				# json.dump(doc, outfile)


	def load_collection(self, load_file):
		load_command = 'mongoimport -d %s -c %s --drop --file %s'
		os.system(load_command % (self.db_id, self.collection_id, load_file))


if __name__ == '__main__':

	db = MongoDb('kdb_db', 'stock_data')
	db.find_data()



