from flask import Blueprint
import secrets
from flask import render_template, flash, redirect, url_for, request, session, make_response
from Restaurant import  db
from Restaurant.models import User, CustomerOrder
from Restaurant.main.forms import MessageForm
from flask_login import current_user, login_required
from Restaurant.dicts import menu
import pdfkit
import stripe

publishable_key = 'pk_test_51KJOqPEYj7vDaQKMeUXoae6KDiwR4ZzdYMuL253SpbAaXVPkTuFe2HJmzKhJy5CZsDN8e2UDs3O31mBooP4KUeAm00quIG2yWO'
stripe.api_key ='sk_test_51KJOqPEYj7vDaQKMyvJ1mEnuYCicRV52A2edrB1gV3zeQysFf100zn8cxQzdYpkiBQg7oZGQ6Ux1ux25L6iGyvl600dpXiuAab'

order = Blueprint('order', __name__)


@order.route('/payment', methods=['POST'])
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
    return redirect(url_for('main.thanks'))


@order.route('/payment_delivery', methods=['POST'])
def payment_delivery():
    invoice = request.form.get('invoice')
    order = CustomerOrder.query.filter_by(invoice=invoice).first()
    order.status = 'Płatność przy odbiorze'
    db.session.commit()
    return redirect(url_for('main.thanks'))


@order.route('/getorder')
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
            return redirect(url_for('order.orders', invoice=invoice))
        except Exception as e:
            print(e)
            flash("Coś poszło nie tak",'danger')
            return redirect(url_for('cart.getcart'))


@order.route('/orders/<invoice>')
@login_required
def orders(invoice):
    if current_user.is_authenticated:
       total = 0
       orders = CustomerOrder.query.filter_by(invoice=invoice).first()
       customer = User.query.filter_by(id=orders.customer_id).first()
       for _key, product in orders.orders.items():
           total += float(product['price']) * int(product['quantity'])
    else:
        return redirect(url_for('users.login'))
    return render_template('user-order.html', menu=menu, invoice=invoice, total=str(total), customer=customer, orders=orders)


@order.route('/get_pdf/<invoice>', methods=['POST'])
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

            rendered = render_template('pdf.html', invoice=invoice, total=total, customer=customer,
                                       orders=orders)
            config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
            pdf = pdfkit.from_string(rendered, False, configuration=config)
            response = make_response(pdf)
            response.headers['content-Type'] = 'application/pdf'
            response.headers['content-Disposition'] = 'inline: filename=' + invoice + '.pdf'
            return response
        return request(url_for('orders.orders'))


@order.route("/<invoice>", methods=['POST'])
@login_required
def order_again(invoice):
    form = MessageForm()
    orders = CustomerOrder.query.filter_by(invoice=invoice).first()
    session['cart'] = orders.orders
    total = 0
    for key, product in session['cart'].items():
        total += float(product['price']) * int(product['quantity'])
    return render_template('cart.html', menu=menu, title='Cart', form=form, total=total)


@order.route('/update_order',methods=['POST'])
def update_order():
    if request.method == "POST":
        invoice = request.form.get("invoice")
        status = request.form.get("status")
        order = CustomerOrder.query.filter_by(invoice=invoice).first()
        order.status = status
        db.session.commit()
    return redirect(request.referrer)

