from Restaurant import db, login_manager, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), unique=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}','{self.email}')"

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    cost = db.Column(db.NUMERIC(2, 2), nullable=False)
    description = db.Column(db.String(200))
    category = db.Column(db.String(40))
    image = db.Column(db.String(50), nullable=False, default='static/food.jpg')

    def __repr__(self):
        return f"User('{self.name}', '{self.cost}', '{self.description}')"

class MyModelView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated:
            if current_user.username == 'admin':
                return True
