from flask import Flask
from app.dbManage import DB
from flask_bcrypt import Bcrypt
# from flask_login import LoginManager

db = DB('mongodb://localhost:27017')

app = Flask(__name__)

COOKIENAME = 'ac625684699ad63620dd448e4ac62568'
CREATEUSERCOOKIE = 'createSesionCookie'
#87fe164448e4ac625684699ad63620dd
app.config['SECRET_KEY'] = '87fe164448e4ac625684699ad63620dd'

bcrypt = Bcrypt(app)

# login_manager = LoginManager()
# login_manager.init_app(app)

from app import routes

def logout():
    return True
