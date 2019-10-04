from pymongo import MongoClient


class DB:
    
    def __init__(self, dbUrl):#'mongodb://localhost:27017'
        # self.client = MongoClient()
        self.client = MongoClient(dbUrl)
        self.db = self.client['test']
        self.posts = self.db.posts
    
    #GETS
    def getAllUsers(self):
        users = []
        for user in self.posts.find({}):
            users.append(user)
        return users

    def getUserInfoById(self,userId):
        user = self.posts.find_one(userId)
        return user
    
    def getUserInfoByName(self,name):
        usuarios = []
        for user in self.posts.find(name): 
            usuarios.append(user)
        return usuarios

    def getUserInfoByLastName(self,name):
        usuarios = []
        for user in self.posts.find(name): 
            usuarios.append(user)
        return usuarios

    def getUserInfoByDocument(self,name):
        usuarios = []
        for user in self.posts.find(name): 
            usuarios.append(user)
        return usuarios

    def getUserInfoByEmail(self,name):
        usuarios = []
        for user in self.posts.find(name): 
            usuarios.append(user)
        return usuarios

    #SETS
    def setUserName(self,userId,name):
        pass

    def setUserLastName(self,userId,name):
        pass

    def setUserDocument(self,userId,name):
        pass

    def setUserEmail(self,userId,name):
        pass

    #ADDS

    def addUser(self,userId,name):
        pass

    #DELETE