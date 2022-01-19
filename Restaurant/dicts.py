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
        'image':'background-image: url(/static/food.jpg)',
    },
{
        'image':'Śniadanie',
        'func' : 'openForm()'

    },
{
        'image':'background-image: url(/static/food2.jfif)'
    },
{
        'image':'Obiad',
        'func' : 'openForm2()'
    },
]
menu_elements2 = [
{
    'image':'Kolacja',
    'func' : 'openForm3()'
    },
{
    'image':'background-image: url(/static/food3.jpg)'
    },
{
    'image':'Przystawki',
    'func' : 'openForm4()'

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