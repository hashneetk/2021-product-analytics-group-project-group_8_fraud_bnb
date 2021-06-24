from app import classes

def query(listing_id):
    current_scores = classes.CurrentScore.query().filter(listing_id=listing_id).first()
    monthly_score = classes.MonthlyScore.query().filter(listing_id=listing_id)

    return current_scores, monthly_score