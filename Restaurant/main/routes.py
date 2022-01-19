from flask import Blueprint, render_template,request
from Restaurant import Product
from Restaurant.dicts import menu, menu_elements, menu_elements2, images, about_content

main = Blueprint('main', __name__)

