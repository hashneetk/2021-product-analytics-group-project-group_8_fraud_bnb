from app import application
from flask import render_template

@application.route('/')
@application.route('/index')
def index():
    return('<h1> Hello world </h1>')