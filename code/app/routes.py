from app import application
from flask import render_template
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import SubmitField, TextField, validators

from selen_scrap import get_info


class URLFile(FlaskForm):
    url = TextField('ListURL', [validators.required(), validators.URL()])
    submit = SubmitField('Submit')


@application.route('/', methods=['POST', 'GET'])
@application.route('/about', methods=['POST', 'GET'])
def index():
    """Index page: Renders about.html with team member names and project
    description"""
    url = URLFile()
    if url.validate_on_submit():
        return (render_template('about.html', authors='Hashneet Kaur, \
        Phillip Navo, Shruti Roy, Vaishnavi Kashyap, Sandhya Kiran, \
        Kaiqi Guo, Jordan Uyeki, and Audrey Barszcz',
        description='*project description goes here*')
        )

#     return('<h1> Welcome to FraudBnB </h1>')
    return (render_template('search.html', authors='Hashneet Kaur, \
    Phillip Navo, Shruti Roy, Vaishnavi Kashyap, Sandhya Kiran, \
    Kaiqi Guo, Jordan Uyeki, and Audrey Barszcz',
            description='*project description goes here*', form=url))


@application.route('/search', methods=['POST', 'GET'])
def search():
    url = URLFile()
    if url.validate_on_submit():
        page_info = get_info(url.url.data)

        return render_template(
            'search_result.html', authors='Hashneet Kaur, \
            Phillip Navo, Shruti Roy, Vaishnavi Kashyap, Sandhya Kiran, \
            Kaiqi Guo, Jordan Uyeki, and Audrey Barszcz',
                description='*:)*',
                list_name=page_info['listing_name'],
                host_name=page_info['host_name'],
                reviews=page_info['reviews'],
                rating=page_info['rating']
        )

    return render_template(
            'search.html', authors='Hashneet Kaur, \
        Phillip Navo, Shruti Roy, Vaishnavi Kashyap, Sandhya Kiran, \
        Kaiqi Guo, Jordan Uyeki, and Audrey Barszcz',
                description='*:)*',
                form=url,
    )
