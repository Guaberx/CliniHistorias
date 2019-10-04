from pymongo import MongoClient
import datetime
import pymongo
import pprint

client = MongoClient()

client = MongoClient('mongodb://localhost:27017')

db = client['test']

posts = db.posts

# pprint.pprint(posts.find_one())

# print()

# pprint.pprint(posts.find_one({"author": "Scott"}))

# pprint.pprint(posts.find_one({"Nombre": "Juan"}))

nombreConsulta = "Camilo"
test = posts.find_one({"Nombre": nombreConsulta})
if posts.count_documents({"Nombre": nombreConsulta}) == 0:
    print("Usuario no existe")
else:
    for consulta in posts.find({"Nombre": nombreConsulta}):
        pprint.pprint(consulta)
