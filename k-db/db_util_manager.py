from pymongo import MongoClient
import datetime
import os

class MongoDb:

	def __init__(self, db_id='kdb-client', collection_id='kdb-collection'):
		
		self.client = MongoClient('mongodb://localhost:27017/')

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

	def find_data(self, json = {}):
		db = self.client[self.db_id]
		collection = db[self.collection_id]
		for item in collection.find(json):
			print(item)

	def delete_data(self, json = {}):
		db = self.client[self.db_id]
		collection = db[self.collection_id]
		post_id = collection.delete_many(json)

	def drop_collection(self):
		db = self.client[self.db_id]
		collection = db[self.collection_id]
		collection.drop()

	def save_collection(self, save_file):
		save_command = 'mongoexport -d %s -c %s -o %s'
		os.system(save_command % (self.db_id, self.collection_id, save_file))

	def load_collection(self, load_file):
		load_command = 'mongoimport -d %s -c %s --drop --file %s'
		os.system(load_command % (self.db_id, self.collection_id, load_file))


if __name__ == '__main__':

	mdb = MongoDb()

	post1 = {"author": "Mike",
			"text": "My first blog post!",
			"tags": ["mongodb", "python", "pymongo"],
			"date": datetime.datetime.utcnow()}

	post2 = {"author": "Jone",
			"text": "My first blog post!",
			"tags": ["python", "pymongo"],
			"date": datetime.datetime.utcnow()}

	posts = []
	posts.append(post1)
	posts.append(post2)
	print(posts)
	mdb.insert_multiple_data(posts)
	mdb.find_data()
	mdb.save_collection('./output')
	mdb.drop_collection()
	mdb.find_data()
	mdb.load_collection('./output')
	mdb.find_data()
	mdb.drop_collection()
	mdb.find_data()



