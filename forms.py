from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Nazwa użytkownika', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Haslo', validators=[DataRequired()])
    confirm_password = PasswordField('Powtorz haslo', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Zarejestruj!')

class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Haslo', validators=[DataRequired()])
    remember = BooleanField('Zapamietaj mnie')
    submit = SubmitField('Zaloguj!')