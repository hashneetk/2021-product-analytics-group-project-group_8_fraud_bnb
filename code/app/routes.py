from app import application
from flask import render_template

@application.route('/')
@application.route('/about')
def index():
    """Index page: Renders about.html with team member names and project description"""
#     return('<h1> Welcome to FraudBnB </h1>')
    return (render_template('about.html', authors='Hashneet Kaur, Phillip Navo, Shruti Roy, Vaishnavi Kashyap, Sandhya Kiran, Kaiqi Guo, Jordan Uyeki, and Audrey Barszcz', description='*project description goes here*'))