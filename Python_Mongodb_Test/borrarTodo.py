from pymongo import MongoClient
import datetime
import pymongo

client = MongoClient()

client = MongoClient('mongodb://localhost:27017')

db = client['test']

posts = db.posts
result = posts.delete_many({})