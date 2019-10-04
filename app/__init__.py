from flask import Flask
from app import dbManage
from flask_bcrypt import Bcrypt

db = dbManage.DB('mongodb://localhost:27017')

app = Flask(__name__)

#87fe164448e4ac625684699ad63620dd
app.config['SECRET_KEY'] = '87fe164448e4ac625684699ad63620dd'

Bcrypt(app)

from app import routes

def logout():
    return True