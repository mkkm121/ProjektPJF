from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_admin import Admin

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'c255e55a9f701bbdd7fbe16d88972d50'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'snackzen0@gmail.com'
app.config['MAIL_PASSWORD'] = 'okobblbotyneyokr'
mail = Mail(app)

from .models import User, Product, MyModelView, CustomerOrder

admin = Admin(app, name='Restaurant', template_mode='bootstrap4')
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Product, db.session))
admin.add_view(MyModelView(CustomerOrder, db.session))

from Restaurant.Users import routes
from Restaurant.cart import routes
from Restaurant.orders import routes
from Restaurant.main import routes

from Restaurant.main.routes import main
from Restaurant.Users.routes import users
from Restaurant.cart.routes import cart
from Restaurant.orders.routes import order

app.register_blueprint(main)
app.register_blueprint(users)
app.register_blueprint(cart)
app.register_blueprint(order)
