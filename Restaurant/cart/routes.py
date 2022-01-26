from flask import render_template, flash, redirect, url_for, request, session, Blueprint
from Restaurant import Product
from Restaurant.main.forms import MessageForm
from Restaurant.dicts import menu
cart = Blueprint('cart', __name__)

def MagerDicts(dict1, dict2):
    if isinstance(dict1,list) and isinstance(dict2,list):
        return dict1+dict2
    elif isinstance(dict1,dict) and isinstance(dict2,dict):
        return dict(list(dict1.items())+list(dict2.items()))
    return False


@cart.route("/addcart", methods=['POST'])
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


@cart.route("/cart")
def getcart():
    form = MessageForm()
    if 'cart' not in session or len(session['cart']) <= 0:
        return redirect(request.referrer)
    total = 0
    for key, product in session['cart'].items():
        total += (product['price']) * int(product['quantity'])

    total = str(total)
    return render_template('cart.html', menu=menu, title='Cart', form=form, total=total)


@cart.route('/updatecart/<int:code>', methods=['POST'])
def updatecart(code):
    if 'cart' not in session and len(session['cart']) <= 0:
        return redirect(url_for('main.home'))
    if request.method == "POST":
        quantity = request.form.get("quantity")
        try:
            session.modified = True
            for key, item in session['cart'].items():
                if int(key) == code:
                    item['quantity'] = quantity
                    flash("Koszyk został zaktualizowany",'success')
                    return redirect(url_for('cart.getcart'))
        except Exception as e:
            print(e)
            return redirect(url_for('cart.getcart'))


@cart.route('/deletecart/<int:id>')
def deletecart(id):
    if 'cart' not in session and len(session['cart']) <= 0:
        return redirect(url_for('main.home'))
    try:
        session.modified = True
        for key, item in session['cart'].items():
            if int(key) == id:
                flash("Koszyk został zaktualizowany", 'success')
                session['cart'].pop(key, None)
                if len(session['cart']) == 0:
                    return redirect(url_for('main.order'))
                else:
                    return redirect(url_for('cart.getcart'))
    except Exception as e:
        print(e)
        return redirect(url_for('cart.getcart'))


@cart.route('/clearcart')
def clearcart():
    try:
        session.pop('cart', None)
        return redirect(url_for('main.order'))
    except Exception as e:
        print(e)


def updateshoppingcart():
    for key, shopping in session['Shoppingcart'].items():
        session.modified = True
        del shopping['image']
        del shopping['colors']
    return updateshoppingcart