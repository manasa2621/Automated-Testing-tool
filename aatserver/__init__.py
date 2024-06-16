import os
import secrets
from flask import Flask
#from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder='static')
# main app for flask
# app = Flask(__name__,
#             template_folder='../templates',
#             static_folder='../static',
#             static_url_path='/static'
#             )
app.secret_key = secrets.token_urlsafe(16)

DATABASE = 'database.db'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE}'
db = SQLAlchemy(app)
# login_manager = LoginManager(app)

# this needs to be imported after the app has been be initialised otherwise this will go into loop and fail for not finding the modules. 
from aatserver.routes import mcq_route
from aatserver.routes import formattive_route


