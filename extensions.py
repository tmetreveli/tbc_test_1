from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager



app = Flask(__name__)

app.config["SECRET_KEY"] = "sdfqcr@#w$twv45T23CQ4TQ"
UPLOAD_FOLDER = 'C:\\Users\\Mifort\\Desktop\\tbc techschool\\group3\\static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"
db = SQLAlchemy(app)

login_manager = LoginManager(app)