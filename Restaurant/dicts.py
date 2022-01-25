menu = [
    {
        'name':'HOME',
        'url':'/home'
    },
    {
        'name':'O nas',
        'url': '/about'
    },
{
        'name':'Oferta',
        'url':'/menu'
    },
{
        'name':'Zamów',
        'url':'/order'
    },
{
        'name':'Kontakt',
        'url':'/contact'
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
        'image':'background-image: url("https://images.pexels.com/photos/103124/pexels-photo-103124.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940")',
    },
{
        'image':'Sniadania',
        'func' : 'openForm()'

    },
{
        'image':'background-image: url("https://images.pexels.com/photos/2116094/pexels-photo-2116094.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940")'
    },
{
        'image':'Obiady',
        'func' : 'openForm2()'
    },
]
menu_elements2 = [
{
    'image':'Kolacje',
    'func' : 'openForm3()'
    },
{
    'image':'background-image: url("https://images.pexels.com/photos/4101805/pexels-photo-4101805.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940")'
    },
{
    'image':'Przystawki',
    'func' : 'openForm4()'

    },
{
    'image': 'background-image: url("https://images.pexels.com/photos/5975907/pexels-photo-5975907.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940")'
    },
]

images = [
    {
        'img':'static/food2.jfif',
        'name':'img-1',
        'prev':'img-3',
        'next':'img-2',
    },
    {
        'img': 'https://as1.ftcdn.net/jpg/02/21/07/80/1000_F_221078059_5lMlCvNQ3lGlJAXuX1nuIFoWNTAwjkdf.jpg',
        'name':'img-2',
        'prev':'img-1',
        'next':'img-3',
    },
    {
        'img': 'static/food.jpg',
        'name':'img-3',
        'prev':'img-2',
        'next':'img-1',
    }
]