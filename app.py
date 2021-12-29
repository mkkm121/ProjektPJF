from flask import Flask, render_template, flash, redirect, url_for
from forms import RegistrationForm, LoginForm

app = Flask(__name__,static_url_path='/static')
app.config['SECRET_KEY']= 'c255e55a9f701bbdd7fbe16d88972d50'

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
    return render_template('home.html',menu=menu)

@app.route('/about')
def about():
    return render_template('About.html',about=about_content,menu=menu,images=images)

@app.route('/menu')
def menu_rend():
    return render_template('menu.html',menu=menu,menu_elements=menu_elements,menu_elements2=menu_elements2)

@app.route('/order')
def order():
    return render_template('order.html',menu=menu)

@app.route('/contact')
def contact():
    return render_template('contact.html',menu=menu)

@app.route('/kebab')
def kebab():
    return '<h2>KIEBAB NA CIENKIM Z OSTRYM SOSEM</h2>'

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('home'))
    return render_template('register.html',title='Register',form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@admin.com' and form.password.data == 'admin':
            flash('Zostales zalogowany!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Logowanie nieudane. Sprawdz login i haslo','danger')
    return render_template('login.html', title='Login', form=form)

if __name__ == '__main__':
    app.run(debug=True)
