import os
from flask import render_template, flash, redirect, url_for, request
from Restaurant.forms import RegistrationForm, LoginForm, UpdateAccountForm,\
    RequestResetForm, ResetPasswordForm, MessageForm
from Restaurant import app, db, bcrypt, mail
from Restaurant.models import User
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
menu = [
    {
        'name':'HOME',
        'url':'home'
    },
    {
        'name':'O nas',
        'url': 'about'
    },
{
        'name':'Oferta',
        'url':'menu'
    },
{
        'name':'Zamów',
        'url':'order'
    },
{
        'name':'Kontakt',
        'url':'contact'
    }
]
about_content = [
    {
        'name':'item-1',
        'description':"Pierwszy slajd",
        'val': 'Burgir burgirowy \n Drugi burgir tez sie znajdzie',
        'prev':'item-3',
        'next':'item-2'
    },
    {
        'name':'item-2',
        'description':"Drugi slajd",
        'val': 'Kebaby z minsem \n Ide po kebaby jakie baby',
        'prev':'item-1',
        'next':'item-3'
    },
    {
        'name':'item-3',
        'description':"Trzeci slajd",
        'val': 'Pizzka z ananasem.\n Zamow juz dzisiaj, swiezutka cieplutka',
        'prev':'item-2',
        'next':'item-1'
    },
]
menu_elements = [
    {
        'image':'background-image: url(/static/food.jpg)',
    },
{
        'image':'Śniadanie'

    },
{
        'image':'background-image: url(/static/food2.jfif)'
    },
{
        'image':'Obiad'
    },
]
menu_elements2 = [
{
    'image':'Kolacja'
    },
{
    'image':'background-image: url(/static/food3.jpg)'
    },
{
    'image':'Przystawki'

    },
{
    'image': 'background-image: url(/static/food.jpg)'
    },
]

images = [
    {
        'img':'static/food.jpg',
        'name':'img-1',
        'prev':'img-3',
        'next':'img-2',
    },
    {
        'img': 'static/food2.jfif',
        'name':'img-2',
        'prev':'img-1',
        'next':'img-3',
    },
    {
        'img': 'static/food3.jpg',
        'name':'img-3',
        'prev':'img-2',
        'next':'img-1',
    }
]
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', menu=menu)

@app.route('/about')
def about():
    return render_template('About.html', about=about_content, menu=menu, images=images, title='About')

@app.route('/menu')
def menu_rend():
    return render_template('menu.html', menu=menu, menu_elements=menu_elements, menu_elements2=menu_elements2, title='Menu')

@app.route('/order')
def order():
    return render_template('order.html', menu=menu, title='Order')

def send_message(name, text, email, address, topic):
    msg = Message(topic, sender='noreply@demo.com', recipients=['snackzen0@gmail.com'])
    msg.body = f'''
    Od: {name}
    Mail: {email}
    Adres: {address}
    Treść: 
    {text}
    '''
    mail.send(msg)

@app.route('/contact', methods=['GET','POST'])
def contact():
    form = MessageForm()
    if current_user.is_authenticated:
        form.name.data = current_user.username
        form.email.data = current_user.email
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        address = form.address.data
        topic = form.topic.data
        text = form.body.data
        send_message(name, text, email, address, topic)
        flash("E-mail został wysłany!", 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html', menu=menu, title='Contact', form=form)

@app.route('/kebab')
def kebab():
    return '<h2>KIEBAB NA CIENKIM Z OSTRYM SOSEM</h2>'

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Konto zostało utworzone. Możesz sie zalogować!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form, menu=menu)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Zalogowano. Witaj {user.username}', 'success')
            return redirect(url_for('home'))
        else:
            flash('Logowanie nieudane. Sprawdz login i haslo', 'danger')
    return render_template('login.html', title='Login', form=form, menu=menu)

@app.route("/logout")
def logout():
    logout_user()
    flash('Wylogowano', 'success')
    return redirect(url_for('home'))

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Twoje konto zostało zaktualizowane!','success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('Account.html', title='Account', menu=menu, form=form)

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Zmiana hasła', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''Żeby zeresetować hasło, wejdź w poniższy:
    {url_for('reset_token',token=token,_external=True)}
    Jeżeli nie chciałes zmienić hasła, zignoruj tego maila.
    '''
    mail.send(msg)

@app.route("/reset_password", methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Wyslano email z instrukacją resetu hasła','success')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset', menu=menu, form=form)

@app.route("/reset_password/<token>", methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Nieprawidłowy token (lub wygasł)', 'danger')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Hasło zostało zmienione. Możesz sie zalogować!', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html',title='Reset', menu=menu, form=form)