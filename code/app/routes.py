from app import application, classes, db
from flask import render_template, redirect, url_for
from flask_wtf import FlaskForm
from flask_login import current_user, login_user, login_required, logout_user
from flask_wtf.file import FileField, FileRequired
from wtforms import SubmitField, TextField, validators


@application.route('/', methods=['GET'])
@application.route('/about', methods=['GET'])
def index():
    """Index page: Renders about.html with team member names and project
    description"""

    return (render_template(
        'about.html',
        authors='Hashneet Kaur, \
    Phillip Navo, Shruti Roy, Vaishnavi Kashyap, Sandhya Kiran, \
    Kaiqi Guo, Jordan Uyeki, and Audrey Barszcz',
        description=
        'Vacation rental scams have been prevalent since well before the pandemic, '
        'so why haven’t rental websites such as Airbnb incorporated scam detection into their'
        ' products? A team member recently experienced this scenario - the 15 person family arrived at a beautiful '
        'Beverly Hills mansion after having paid a large sum of money, only to find out that the mansion, in fact, did not exist. '
        'While they got their money back, the situation could have been completely avoided with proper vetting, '
        'and the experience was left wanting. Our product will take into account several factors such as listing reviews, '
        'host reviews, analysis of pictures and address verification in order to establish trust and reliability for the consumer renting on Airbnb.',
        ))


@application.route('/search/<username>', methods=['POST', 'GET'])
@login_required
def search(username):
    listing_id_form = classes.ListIdForm()
    if listing_id_form.validate_on_submit():
        listing_id = listing_id_form.listing_id.data
        score = classes.Listings.query \
                .filter_by(listing_id=int(listing_id)).first().listing_reliability

        if not score:
            score = 'Sorry, score not found.'

        return render_template('search_result.html',
                               listing_id=listing_id,
                               username=username,
                               score=score,
                            )

    return render_template(
        'search.html',
        username=username,
        form=listing_id_form,
    )


@application.route('/register', methods=('GET', 'POST'))
def register():
    """Register page: Renders register.html with sign up form asking for username, email, and password
    """
    registration_form = classes.RegistrationForm()
    if registration_form.validate_on_submit():
        username = registration_form.username.data
        password = registration_form.password.data
        email = registration_form.email.data

        user_count = classes.User.query.filter_by(username=username).count() \
            + classes.User.query.filter_by(email=email).count()
        if (user_count > 0):
            return '<h1>Error - Existing user : ' + username \
                   + ' OR ' + email + '</h1>'
        else:
            user = classes.User(username, email, password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('register.html', form=registration_form)


@application.route('/login', methods=['GET', 'POST'])
def login():
    """Login page: Renders login.html with submit form for username and password
    """
    login_form = classes.LogInForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data

        user = classes.User.query.filter_by(username=username).first()

        if user is not None and user.check_password(password):
            login_user(user)
            return redirect(url_for('search', username=username))

    return render_template('login.html', form=login_form)


@application.route('/logout')
@login_required
def logout():
    """Logout page: Unauthorized server error (expected)
    """
    before_logout = '<h1> Before logout - is_autheticated : ' \
                    + str(current_user.is_authenticated) + '</h1>'

    logout_user()

    after_logout = '<h1> After logout - is_autheticated : ' \
                   + str(current_user.is_authenticated) + '</h1>'
    return before_logout + after_logout