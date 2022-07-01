from flask import Blueprint, render_template, request
from app.extensions import MongoConnect
import os

STATIC_DIR = os.path.abspath('../static')
home = Blueprint('home', __name__,
        template_folder = 'templates',
        static_folder = 'static')

@home.route('/', methods=['GET'])
def view():
    if request.method == 'GET': 
        data = {}
        obj = MongoConnect(data)
        response = obj.read()
        return render_template('home.html', response=response) # Returning response and rendering template
