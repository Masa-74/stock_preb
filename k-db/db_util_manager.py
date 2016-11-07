from pymongo import MongoClient
import datetime

client = MongoClient('mongodb://localhost:27017/')

db_id = 'kdb-client'
collection_id = 'kdb-collection'


def insert_data(json, db=db_id, collection=collection_id):
	db = client[db_id]
	collection = db[collection_id]
	post_id = collection.insert_one(json)

def insert_multiple_data(json_list, db=db_id, collection=collection_id):
	db = client[db_id]
	collection = db[collection_id]
	post_id = collection.insert_many(json)

def find_data(json = {}, db=db_id, collection=collection_id):
	db = client[db_id]
	collection = db[collection_id]
	for item in collection.find(json):
		print(item)

def delete_data(json = {}, db=db_id, collection=collection_id):
	db = client[db_id]
	collection = db[collection_id]
	post_id = collection.delete_many(json)

def drop_collection(db=db_id, collection=collection_id):
	db = client[db_id]
	collection = db[collection_id]
	collection.drop()





if __name__ == '__main__':

	post = {"author": "Mike",
			"text": "My first blog post!",
			"tags": ["mongodb", "python", "pymongo"],
			"date": datetime.datetime.utcnow()}
	insert_data(post)
	find_data()
	drop_collection()
	find_data()

