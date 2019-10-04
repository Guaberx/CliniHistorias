from pymongo import MongoClient
import datetime
import pymongo

client = MongoClient()

client = MongoClient('mongodb://localhost:27017')

db = client['test']

posts = db.posts
# post_data = {
#     'title': 'Python and MongoDB',
#     'content': 'PyMongo is fun, you guys',
#     'author': 'Scott'
# }
# result = posts.insert_one(post_data)
# print('One post: {0}'.format(result.inserted_id))


# post_2 = {
#     'title': 'Virtual Environments',
#     'content': 'Use virtual environments, you guys',
#     'author': 'Scott'
# }
# post_3 = {
#     'title': 'Learning Python',
#     'content': 'Learn Python, it is easy',
#     'author': 'Bill'
# }
# new_result = posts.insert_many([post_2, post_3])
# print('Multiple posts: {0}'.format(new_result.inserted_ids))

# bills_post = posts.find_one({'author': 'Bill'})
# print(bills_post)


# print("View all documents: ")
# cursor = posts.find()
# for document in cursor:
#     print(document)
usuario = {
    'Nombre' : 'Bananin',
    'Apellido' : 'Elmo Cosquillas',
    'DI' : '17478865',
    'Consultas':
    [
        {
            'id': 1,
            'Descripcion' : 'Sida. Es un moluzco contagioso',
            'Estado' : 'Atendida. Sin CURA',
            'Dependencias': []
        }
    ]
}
result = posts.insert_one(usuario)
# result = posts.insert_many(usuario)