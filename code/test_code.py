from app import classes
from app import db
from config import Config
from flask_sqlalchemy import SQLAlchemy
import score.py

def UserFromDB(username):
    user = classes.User.query.filter_by(username=username).first()
    return user


def test_db_existence():
    """
    Check whether the __init__ created a db and user class table.
    """
    db = SQLAlchemy()
    engine = db.create_engine(Config.SQLALCHEMY_DATABASE_URI, {})
    inspect = db.inspect(engine)
    assert (inspect.has_table("user"))


def test_UserFromDB():
    """
        Assuming that "sandhyakiran, sandhyakiran337@gmail.com,
        12345678" is always in the database
        """
    assert UserFromDB("sandhyakiran").email == "sandhyakiran337@gmail.com"
    assert UserFromDB("sandhyakiran").username == "sandhyakiran"


def test_listing_id_data():
    """
    Testing Data generated on Dashboard based on the
    corresponding Listing Value 13776
    is correct
    """
    assert classes.CurrentScore.query.filter_by(listing_id=13776).first().num_host_cancellations == 0
    assert classes.CurrentScore.query.filter_by(listing_id=13776).first().num_fraud_reviewers == 4

def test_num_items():
    """Check the num_items code to see the
    number of items in the string"""
    df = pd.DataFrame(columns=['test'])
    df = pd.DataFrame(np.array(["['a','b','c']"]), columns=df.columns)
    a = num_items(df['test'])
    assert [3] == a