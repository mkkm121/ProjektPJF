from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from Restaurant.Users.forms import RegistrationForm, LoginForm, UpdateAccountForm,\
    RequestResetForm, ResetPasswordForm
from Restaurant import db, bcrypt, mail
from Restaurant.models import User, CustomerOrder
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from Restaurant.dicts import menu

users = Blueprint('users', __name__)

@users.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    user = User.query.filter_by(email=form.email.data).first()
    if user:
        flash('Konto z podanym e-mailem już istnieje!', 'danger')
        return redirect(url_for('users.register'))
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Konto zostało utworzone. Możesz sie zalogować!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form, menu=menu)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Zalogowano. Witaj {user.username}', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Logowanie nieudane. Sprawdz login i haslo', 'danger')
    return render_template('login.html', title='Login', form=form, menu=menu)


@users.route("/logout")
def logout():
    logout_user()
    flash('Wylogowano', 'success')
    return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    orders = CustomerOrder.query.filter_by(customer_id=current_user.id).order_by(CustomerOrder.date_created.desc())
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Twoje konto zostało zaktualizowane!','success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('Account.html', title='Account', menu=menu, form=form, orders=orders)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Zmiana hasła', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''Żeby zeresetować hasło, wejdź w poniższy link:
    {url_for('users.reset_token',token=token,_external=True)}
    Jeżeli nie chciałes zmienić hasła, zignoruj tego maila.
    '''
    mail.send(msg)


@users.route("/reset_password", methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Wyslano email z instrukacją resetu hasła','success')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset', menu=menu, form=form)


@users.route("/reset_password/<token>", methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Nieprawidłowy token (lub wygasł)', 'danger')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Hasło zostało zmienione. Możesz sie zalogować!', 'success')
        return redirect(url_for('main.login'))
    return render_template('reset_token.html',title='Reset', menu=menu, form=form)