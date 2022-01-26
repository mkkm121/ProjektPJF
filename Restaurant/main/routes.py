from flask import Blueprint
from flask import render_template, flash, redirect, url_for
from Restaurant.main.forms import MessageForm
from Restaurant import  mail
from Restaurant.models import User, Product, CustomerOrder
from flask_login import current_user
from flask_mail import Message
from Restaurant.dicts import menu, images, menu_elements, menu_elements2, about_content


main = Blueprint('main', __name__)


@main.route('/thanks')
def thanks():
    return render_template('thank.html', menu=menu)


@main.route('/')
@main.route('/home')
def home():
    return render_template('home.html', menu=menu)


@main.route('/about')
def about():
    return render_template('About.html', about=about_content, menu=menu, images=images, title='About')


@main.route('/menu')
def menu_rend():
    return render_template('menu.html', menu=menu, menu_elements=menu_elements, menu_elements2=menu_elements2, title='Menu')

@main.route('/admin_panel')
def admin_panel():
    if current_user.username != 'admin':
        return redirect("home")
    else:
        users = User.query.all()
        orders = CustomerOrder.query.all()
        products = Product.query.all()
        return render_template('admin_panel.html', menu=menu, title='Admin Panel', orders=orders, last_user=len(users),users=users,
                           number_of_orders=len(orders), products=products, number_of_products=len(products))

@main.route('/order')
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


@main.route('/contact', methods=['GET','POST'])
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
        return redirect(url_for('main.contact'))
    return render_template('contact.html', menu=menu, title='Contact', form=form)