from flask_wtf import FlaskForm
from flask_login import UserMixin
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired

from app import db, login_manager


class User(db.Model, UserMixin):
    "Class for user table"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Listings(db.Model):
    "Class for listings table"
    listing_id = db.Column(db.Integer)
    review_id = db.Column(db.Integer, primary_key=True)
    review_date = db.Column(db.DateTime)
    reviewer_id = db.Column(db.Integer)
    reviewer_name = db.Column(db.String())
    scores = db.Column(db.Float)
    cancel_flag = db.Column(db.Float)
    num_words = db.Column(db.Float)
    sentiment_score = db.Column(db.Float)
    num_reviews = db.Column(db.Integer)
    similarity = db.Column(db.Float)
    perc_scores = db.Column(db.Float)
    perc_flag = db.Column(db.Float)
    perc_sentiment_score = db.Column(db.Float)
    review_reliability = db.Column(db.Float)
    listing_reliability = db.Column(db.Float)


class MonthlyScore(db.Model):
    "Class for listings table"
    listing_id = db.Column(db.Integer, primary_key=True)
    score_month = db.Column(db.String(7), primary_key=True)
    avg_sentiment_score = db.Column(db.Integer)
    listing_availability = db.Column(db.Integer)
    avg_rating = db.Column(db.Float)


class CurrentScore(db.Model):
    "Class for listings table"
    listing_id = db.Column(db.Integer, primary_key=True)
    overall_reliability = db.Column(db.Integer)
    review_reliability = db.Column(db.Integer)
    reviewer_reliability = db.Column(db.Integer)
    host_reliability = db.Column(db.Integer)
    num_fraud_reviewers = db.Column(db.Integer)
    num_host_cancellations = db.Column(db.Integer)
    num_positive = db.Column(db.Integer)
    num_neutral = db.Column(db.Integer)
    num_negative = db.Column(db.Integer)

class RegistrationForm(FlaskForm):
    "Class for register form"
    username = StringField('Username:', validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField('Submit')


class LogInForm(FlaskForm):
    "Class for login form"
    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField('Login')


class ListIdForm(FlaskForm):
    listing_id = StringField('ListURL', validators=[DataRequired()])
    submit = SubmitField('Submit')


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


db.create_all()
db.session.commit()
