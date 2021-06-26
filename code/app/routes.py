from app import application, classes, db
from flask import render_template, request,redirect, url_for
from flask_wtf import FlaskForm
from flask_login import current_user, login_user, login_required, logout_user
from flask_wtf.file import FileField, FileRequired
from wtforms import SubmitField, TextField, validators
from flask_bootstrap import Bootstrap


from create_map import map_html

def page_not_found(e):
  return render_template('404.html'), 404

application.register_error_handler(404, page_not_found)

@application.route('/', methods=['GET'])
@application.route('/index', methods=['GET'])
@application.route('/about', methods=['GET'])
def index():
    """Index page: Renders about.html with team member names and project
    description"""
    return render_template(
        'index.html',
        authenticated_user=current_user.is_authenticated,
        username=current_user.username if current_user.is_authenticated else ''
    )


@application.route('/register', methods=('GET', 'POST'))
def register():
    """Register page: Renders register.html with sign up
    form asking for username, email, and password
    """
    registration_form = classes.RegistrationForm()
    if registration_form.validate_on_submit():
        username = registration_form.username.data
        password = registration_form.password.data
        email = registration_form.email.data

        user_count = classes.User.query.filter_by(username=username).count() \
            + classes.User.query.filter_by(email=email).count()
        if (user_count > 0):
            return render_template(
                'register.html',
                form=registration_form,
                error_msg=f'username: {username} or email: {email} already taken!'
            )
        else:
            user = classes.User(username, email, password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('register.html', form=registration_form)


@application.route('/login', methods=['GET', 'POST'])
def login():
    """Login page: Renders login.html with submit
    form for username and password
    """
    login_form = classes.LogInForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data

        user = classes.User.query.filter_by(username=username).first()

        if user is not None and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            return render_template(
                'login.html',
                form=login_form,
                error_msg='Invalid username or password!'
            )

    return render_template('login.html', form=login_form)


@application.route('/logout')
@login_required
def logout():
    """Logout page: Unauthorized server error (expected)
    """
    logout_user()
    return redirect(url_for('index'))


@application.route('/reliability-map/<max_listing>')
@login_required
def display_n_listing(max_listing):
    return map_html(max_listing)


@application.route('/analysis-reports')
@login_required
def analysis_reports():
    return render_template(
        'analysis-reports.html',
        authenticated_user=current_user.is_authenticated,
        not_at_index=True,
        username=current_user.username,
    )


@application.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    """DashBoard page: 
    With a listing ID as an input given by authenticated user,
    Outputs charts with :
    Overall Reliability, Reviews Reliability, Reviewer Reliability, Host Reliability 
    as scores,
    Number of Fraud Reviewers, Number of Host Cancellations,
    Average Review Sentiment Scores of the latest 4 months,
    Average Ratings Scores of the latest 4 months,
    Listing Availability of the latest 4 months,
    Number of Positive, Neutral and Negative Reviews.
    """
    listingid = request.args.get('key')
    dates = ['2020-02','2020-03','2020-04','2020-05']
    sentiments = ["Postive","Neutral","Negative"]
    sentiment_values = [20, 30, 50]
    listing_availability = [55, 49, 44, 24, 15]
    avg_review_sentiment_scores = [95, 87, 44, 94, 95]
    avg_rating_scores = [5, 4, 4, 3]

    host_cancellations = 1
    fraud_reviewers = 2
    overall_reliability = 80
    review_reliability = 60
    reviewer_reliability = 30
    host_reliability = 20


    if listingid is not None:
        # print("input from browser",listingid)
        dates = []
        for row in classes.MonthlyScore.query.filter_by(listing_id = listingid).limit(4):
            dates.append(row.score_month)
        # print("dates: ", test)

        # Pie chart
        pos_score = classes.CurrentScore.query.filter_by(listing_id = listingid).first().num_positive
        neu_score = classes.CurrentScore.query.filter_by(listing_id = listingid).first().num_neutral
        neg_score = classes.CurrentScore.query.filter_by(listing_id = listingid).first().num_negative
        sentiment_values = [pos_score, neu_score, neg_score]

        # small cards
        host_cancellations = classes.CurrentScore.query.filter_by(listing_id = listingid).first().num_host_cancellations
        fraud_reviewers = classes.CurrentScore.query.filter_by(listing_id = listingid).first().num_fraud_reviewers

        # top cards
        overall_reliability = int(classes.CurrentScore.query.filter_by(listing_id = listingid).first().overall_reliability)
        review_reliability = classes.CurrentScore.query.filter_by(listing_id = listingid).first().review_reliability
        reviewer_reliability = classes.CurrentScore.query.filter_by(listing_id = listingid).first().reviewer_reliability
        host_reliability = classes.CurrentScore.query.filter_by(listing_id = listingid).first().host_reliability

        listing_availability = []
        for row in classes.MonthlyScore.query.filter_by(listing_id = listingid).limit(4):
            listing_availability.append(row.listing_availability)

        avg_review_sentiment_scores = []
        for row in classes.MonthlyScore.query.filter_by(listing_id = listingid).limit(4):
            avg_review_sentiment_scores.append(row.avg_sentiment_score)

        avg_rating_scores = []
        for row in classes.MonthlyScore.query.filter_by(listing_id = listingid).limit(4):
            avg_rating_scores.append(row.avg_rating)




    return render_template('dashboard.html',authenticated_user=current_user.username,dates=dates,sentiments=sentiments
                                        ,sentiment_values=sentiment_values
                                        ,listing_availability=listing_availability
                                        ,avg_review_sentiment_scores=avg_review_sentiment_scores
                                        ,avg_rating_scores=avg_rating_scores, 
                                        host_cancellations = host_cancellations, 
                                        fraud_reviewers= fraud_reviewers
                                        ,overall_reliability = overall_reliability,
                                        review_reliability = review_reliability,
                                        reviewer_reliability = reviewer_reliability,
                                        host_reliability = host_reliability)
