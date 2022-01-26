from flask_wtf import FlaskForm
from wtforms import StringField,  SubmitField,  TextAreaField
from wtforms.validators import DataRequired, Length, Email
from wtforms.fields.html5 import TelField

class MessageForm(FlaskForm):
    name = StringField('Nazwa*', validators=[DataRequired()])
    email = StringField('E-mail*', validators=[DataRequired(), Email()])
    phone = TelField('Telefon')
    address = StringField('Adres')
    topic = TextAreaField('Temat*', validators=[DataRequired(), Length(min=0, max=50)])
    body = TextAreaField('Wiadomość*', validators=[DataRequired(), Length(min=1, max=500)])
    submit = SubmitField('Wyślij!')

