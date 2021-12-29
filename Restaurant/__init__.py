from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__,static_url_path='/static')
app.config['SECRET_KEY']= 'c255e55a9f701bbdd7fbe16d88972d50'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

from Restaurant import routes