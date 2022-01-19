import secrets
from flask import render_template, flash, redirect, url_for, request, session, make_response
from Restaurant.forms import RegistrationForm, LoginForm, UpdateAccountForm,\
    RequestResetForm, ResetPasswordForm, MessageForm
from Restaurant import app, db, bcrypt, mail
from Restaurant.models import User, Product, CustomerOrder
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from Restaurant.dicts import menu, images, menu_elements, menu_elements2, about_content
import pdfkit
import stripe

publishable_key = 'pk_test_51KJOqPEYj7vDaQKMeUXoae6KDiwR4ZzdYMuL253SpbAaXVPkTuFe2HJmzKhJy5CZsDN8e2UDs3O31mBooP4KUeAm00quIG2yWO'
stripe.api_key ='sk_test_51KJOqPEYj7vDaQKMyvJ1mEnuYCicRV52A2edrB1gV3zeQysFf100zn8cxQzdYpkiBQg7oZGQ6Ux1ux25L6iGyvl600dpXiuAab'


@app.route('/payment', methods=['POST'])
def payment():
    invoice = request.form.get('invoice')
    amount = request.form.get('amount')
    customer = stripe.Customer.create(
      email=request.form['stripeEmail'],
      source=request.form['stripeToken'],
    )
    charge = stripe.Charge.create(
      customer=customer.id,
      description='Snackzen Order',
      amount=amount,
      currency='PLN',
    )
    order = CustomerOrder.query.filter_by(invoice=invoice).first()
    order.status = 'Zapłacone'
    db.session.commit()
    return redirect(url_for('thanks'))


@app.route('/payment_delivery', methods=['POST'])
def payment_delivery():
    invoice = request.form.get('invoice')
    order = CustomerOrder.query.filter_by(invoice=invoice).first()
    order.status = 'Płatność przy odbiorze'
    db.session.commit()
    return redirect(url_for('thanks'))


@app.route('/thanks')
def thanks():
    return render_template('thank.html', menu=menu)


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
    products = Product.query.all()
    return render_template('order.html', menu=menu, title='Order', products=products)


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
    orders = CustomerOrder.query.filter_by(customer_id=current_user.id).order_by(CustomerOrder.date_created.desc())
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Twoje konto zostało zaktualizowane!','success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('Account.html', title='Account', menu=menu, form=form, orders=orders)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Zmiana hasła', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''Żeby zeresetować hasło, wejdź w poniższy link:
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


def MagerDicts(dict1, dict2):
    if isinstance(dict1,list) and isinstance(dict2,list):
        return dict1+dict2
    elif isinstance(dict1,dict) and isinstance(dict2,dict):
        return dict(list(dict1.items())+list(dict2.items()))
    return False


@app.route("/addcart", methods=['POST'])
def AddCart():
    try:
        quantity = 1
        product_id = request.form.get('id')
        product = Product.query.filter_by(id=product_id).first()
        if product_id and product and request.method == 'POST':
            DictItems = {product_id: {'name': product.name, 'price': product.cost, 'image': product.image, 'quantity': quantity}}
            if 'cart' in session:
                if product_id in session['cart']:
                    for key, item in session['cart'].items():
                        if int(key) == int(product_id):
                            session.modified = True
                            item['quantity'] += 1
                else:
                    session['cart'] = MagerDicts(session['cart'], DictItems)
            else:
                session['cart'] = DictItems
                return redirect(request.referrer)
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)


@app.route("/cart")
def getcart():
    form = MessageForm()
    if 'cart' not in session or len(session['cart']) <= 0:
        return redirect(request.referrer)
    total = 0
    for key, product in session['cart'].items():
        total += (product['price']) * int(product['quantity'])

    total = str(total)
    return render_template('cart.html', menu=menu, title='Cart', form=form, total=total)


@app.route('/updatecart/<int:code>', methods=['POST'])
def updatecart(code):
    if 'cart' not in session and len(session['cart']) <= 0:
        return redirect(url_for('home'))
    if request.method == "POST":
        quantity = request.form.get("quantity")
        try:
            session.modified = True
            for key, item in session['cart'].items():
                if int(key) == code:
                    item['quantity'] = quantity
                    flash("Koszyk został zaktualizowany",'success')
                    return redirect(url_for('getcart'))
        except Exception as e:
            print(e)
            return redirect(url_for('getcart'))


@app.route('/deletecart/<int:id>')
def deletecart(id):
    if 'cart' not in session and len(session['cart']) <= 0:
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key, item in session['cart'].items():
            if int(key) == id:
                flash("Koszyk został zaktualizowany", 'success')
                session['cart'].pop(key,None)
                if len(session['cart'])==0:
                    return redirect(url_for('order'))
                else:
                    return redirect(url_for('getcart'))
    except Exception as e:
        print(e)
        return redirect(url_for('getcart'))


@app.route('/clearcart')
def clearcart():
    try:
        session.pop('cart',None)
        return redirect(url_for('order'))
    except Exception as e:
        print(e)


def updateshoppingcart():
    for key, shopping in session['Shoppingcart'].items():
        session.modified = True
        del shopping['image']
        del shopping['colors']
    return updateshoppingcart


@app.route('/getorder')
@login_required
def getorder():
    if current_user.is_authenticated:
        customer_id = current_user.id
        invoice = secrets.token_hex(5)
        try:
            order = CustomerOrder(invoice=invoice,customer_id=customer_id,orders=session['cart'])
            db.session.add(order)
            db.session.commit()
            session.pop('cart')
            flash('Zamówienie zostało złożone','success')
            return redirect(url_for('orders', invoice=invoice))
        except Exception as e:
            print(e)
            flash("Coś poszło nie tak",'danger')
            return redirect(url_for('getcart'))


@app.route('/orders/<invoice>')
@login_required
def orders(invoice):
    if current_user.is_authenticated:
       total = 0
       customer_id = current_user.id
       customer = User.query.filter_by(id=customer_id).first()
       orders = CustomerOrder.query.filter_by(invoice=invoice).first()
       for _key, product in orders.orders.items():
           total += float(product['price']) * int(product['quantity'])
    else:
        return redirect(url_for('login'))
    return render_template('user-order.html', menu=menu, invoice=invoice, total=str(total), customer=customer, orders=orders)


@app.route('/get_pdf/<invoice>', methods=['POST'])
@login_required
def get_pdf(invoice):
    if current_user.is_authenticated:
        total = 0
        customer_id = current_user.id
        if request.method == 'POST':
            customer = User.query.filter_by(id=customer_id).first()
            orders = CustomerOrder.query.filter_by(invoice=invoice).order_by(CustomerOrder.id.desc()).first()
            for _key, product in orders.orders.items():
                total += float(product['price']) * int(product['quantity'])

            rendered = render_template('pdf.html', menu=menu, invoice=invoice, total=total, customer=customer,
                                       orders=orders)
            config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
            pdf = pdfkit.from_string(rendered, False, configuration=config)
            response = make_response(pdf)
            response.headers['content-Type'] = 'application/pdf'
            response.headers['content-Disposition'] = 'inline: filename=' + invoice + '.pdf'
            return response
        return request(url_for('orders'))


@app.route("/<invoice>", methods=['POST'])
@login_required
def order_again(invoice):
    form = MessageForm()
    orders = CustomerOrder.query.filter_by(invoice=invoice).first()
    session['cart'] = orders.orders
    total = 0
    for key, product in session['cart'].items():
        total += float(product['price']) * int(product['quantity'])
    return render_template('cart.html', menu=menu, title='Cart', form=form, total=total)

