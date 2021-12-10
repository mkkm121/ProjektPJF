from flask import Flask, render_template

app = Flask(__name__,static_url_path='/static')

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
        'image':'background-image: url(/static/food.jpg)'
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
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html',menu=menu)

@app.route('/about')
def about():
    return render_template('About.html',about=about_content,menu=menu)

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


if __name__ == '__main__':
    app.run(debug=True)
