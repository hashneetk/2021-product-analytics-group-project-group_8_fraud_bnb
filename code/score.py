import sys
import numpy as np
import pandas as pd
import pickle
from textatistic import Textatistic
from tqdm import tqdm
import multiprocessing as mp
from multiprocessing import Pool
from sklearn.feature_extraction.text import TfidfVectorizer
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

reviews = pd.read_pickle('reviews.pkl')
listing = pd.read_csv('listings.csv')
df_listing = listing[listing['id'].isin(reviews['listing_id'])]
df_reviews = reviews[reviews['listing_id'].isin(listing['id'])]


def text_score(x):
    try:
        return Textatistic(x).scores['flesch_score']
    except:
        return np.NaN
analyser = SentimentIntensityAnalyzer()


def SentimentIntensityScore(sentence):
    score = analyser.polarity_scores(sentence)
    return score['compound']
scores = []
cancel_flag = []
length = []
sentiment_score = []
for i in tqdm(range(len(df_reviews['comments']))):
    x = df_reviews['comments'][i]
    if isinstance(x, str):
        clean_x = re.sub(r'!', '.', x)
        scores.append(text_score(clean_x))
        length.append(len(x.split(' ')))
        sentiment_score.append(SentimentIntensityScore(x))
        if 'cancel' in x:
            cancel_flag.append(1)
            continue
        else:
            cancel_flag.append(0)

    else:
        scores.append(np.NaN)
        length.append(np.NaN)
        cancel_flag.append(np.NaN)
        sentiment_score.append(np.NaN)
df_reviews['scores'] = scores
df_reviews['cancel_flag'] = cancel_flag
df_reviews['num_words'] = length
df_reviews['sentiment_score'] = sentiment_score
df_reviews['scores'] = df_reviews['scores'].\
    replace(0, np.median(df_reviews['scores']))
df_reviews['perc_scores'] = df_reviews['scores'].\
    rank(pct=True)
df_reviews['perc_flag'] = df_reviews['cancel_flag'].\
    rank(pct=True, ascending=True)
df_reviews['perc_sentiment_score'] = df_reviews['sentiment_score'].\
    rank(pct=True)
df_reviews['reviewer_num_reviews'] \
    = df_reviews.groupby('reviewer_id')['reviewer_id'].transform('count')
df_reviews['reviewer_overall_count'] = df_reviews['reviewer_num_reviews'].\
    rank(pct=True)
gp = df_reviews.groupby(['reviewer_id', 'listing_id'], as_index=False).\
    agg({'comments': 'count'})
df_reviews_new = gp.merge(df_reviews, on=['reviewer_id', 'listing_id']).\
    rename(columns={'comments_x': 'count_reviews'})
df_reviews_new['count_reviews_score'] = df_reviews_new['count_reviews'].\
    rank(method='max', ascending=False, pct=True)
df_reviews_new[df_reviews_new['count_reviews'] > 1]
[['count_reviews_score', 'count_reviews']]
gp1 = df_reviews_new.groupby(['listing_id'],
                             as_index=False).agg({'id': 'count'})
gp1 = gp1.rename(columns={'id': 'review_count'})
df_reviews_new = gp1.merge(df_reviews_new,
                           on=['listing_id'])
df_reviews_new['listing_review_count'] = \
    df_reviews_new['review_count'].rank(pct=True)

df_listing['review_overall_score'] = \
    df_listing['review_scores_accuracy'] \
    + df_listing['review_scores_rating'] \
    + df_listing['review_scores_cleanliness'] \
    + df_listing['review_scores_checkin'] \
    + df_listing['review_scores_communication'] \
    + df_listing['review_scores_location'] \
    + df_listing['review_scores_value']

df_listing.rename(columns={'id': 'listing_id'}, inplace=True)
m1 = df_listing[['listing_id', 'review_overall_score']]
df_reviews_new = df_reviews_new.merge(m1, on='listing_id')
df_reviews_new['overall_score'] = \
    df_reviews_new['review_overall_score'].rank(pct=True)

# Host values
df_listing['host_license_flag'] = 0
df_listing['host_license_flag'] = np.where(df_listing['license'].notna(), 1,
                                           df_listing['host_license_flag'])
df_listing['host_identity_flag'] = 0
df_listing['host_identity_flag'] = np.where(
    df_listing['host_identity_verified'] == 't',
    1, df_listing['host_identity_flag'])
df_listing['host_verification_list'] = \
    [len(i.replace('[', '').replace(']', '').
         replace("'", '').split(',')) for i in
     df_listing['host_verifications']]
df_listing['host_v_list_pt'] = \
    df_listing['host_verification_list'].rank(pct=True)
m2 = df_listing[['listing_id',
                 'host_v_list_pt', 'host_identity_flag', 'host_license_flag']]
df_reviews_new = df_reviews_new.merge(m2, on='listing_id')
df_lid = df_reviews_new[['listing_id', 'overall_score', 'listing_review_count',
                         'perc_scores', 'perc_flag', 'perc_sentiment_score',
                         'count_reviews_score',
                         'reviewer_overall_count',
                         'host_v_list_pt',
                         'host_identity_flag',
                         'host_license_flag',
                         'cancel_flag']]

df_lid['total_overall_score'] = \
    df_lid['overall_score'] + \
    df_lid['listing_review_count']
df_lid['total_review_score'] = \
    df_lid['perc_scores'] + df_lid['perc_sentiment_score']
df_lid['total_reviewer_score'] = \
    df_lid['count_reviews_score'] + df_lid['reviewer_overall_count']
df_lid['total_host_score'] = \
    df_lid['host_v_list_pt'] + \
    df_lid['host_identity_flag'] +\
    df_lid['host_license_flag']
df_final = \
    df_lid[['listing_id', 'total_overall_score',
            'total_review_score', 'total_reviewer_score',
            'total_host_score', 'cancel_flag']]
df_final['overall_score_pt'] = \
    df_final['total_overall_score'].rank(pct=True)
df_final['review_score_pt'] = \
    df_final['total_review_score'].rank(pct=True)
df_final['reviewer_score_pt'] = \
    df_final['total_reviewer_score'].rank(pct=True)
df_final['host_score_pt'] = \
    df_final['total_host_score'].rank(pct=True)
df_final['overall_score_pt'].fillna(0, inplace=True)
df_final['review_score_pt'].fillna(0, inplace=True)
df_final['reviewer_score_pt'] = df_final['reviewer_score_pt']*100
df_final['reviewer_score_pt'] = df_final['reviewer_score_pt'].astype(int)
df_final['host_score_pt'] = df_final['host_score_pt']*100
df_final['host_score_pt'] = df_final['host_score_pt'].astype(int)
df_final['review_score_pt'] = df_final['review_score_pt']*100
df_final['review_score_pt'] = df_final['review_score_pt'].astype(int)
df_final['overall_score_pt'] = df_final['overall_score_pt']*100
df_final['overall_score_pt'] = df_final['overall_score_pt'].astype(int)

df_final1 = df_final[['listing_id', 'overall_score_pt', 'review_score_pt',
                      'reviewer_score_pt', 'host_score_pt', 'cancel_flag']]

group = df_final1.groupby('listing_id', as_index=False).sum()
data = group[['listing_id', 'cancel_flag']]
df_final1 = df_final1.merge(data, on='listing_id')
df_final1 = df_final1.drop(columns=['cancel_flag_x'])
df_final1 = df_final1.rename(columns={'cancel_flag_y': 'cancel_flag'})
final = df_final1.groupby('listing_id', as_index=False).agg('mean')

q_low_reviewer = final['reviewer_score_pt'].quantile(0.01)
suspicious_reviewers = \
    final[final['reviewer_score_pt'] <
          q_low_reviewer]['listing_id']
final['suspicious_reviewer'] = \
    np.where(final['listing_id']
             .isin(suspicious_reviewers), 1, 0)
final['overall_score_pt'] = \
    final['overall_score_pt'].astype(int)
final['review_score_pt'] = \
    final['review_score_pt'].astype(int)
final['reviewer_score_pt'] = \
    final['reviewer_score_pt'].astype(int)
final['host_score_pt'] = \
    final['host_score_pt'].astype(int)
final['cancel_flag'] = \
    final['cancel_flag'].astype(int)

# Add details for sentiment score
df_reviews_new.loc[df_reviews_new['sentiment_score'] <
                   0.50, 'negative_review'] = 1
df_reviews_new['negative_review'] = df_reviews_new['negative_review'].fillna(0)
df_reviews_new.loc[(df_reviews_new['sentiment_score'] <= 0.50) &
                   (df_reviews_new['sentiment_score'] <= 0.60),
                   'neutral_review'] = 1
df_reviews_new['neutral_review'] = df_reviews_new['neutral_review'].fillna(0)
df_reviews_new.loc[df_reviews_new['sentiment_score'] >
                   0.60, 'positive_review'] = 1
df_reviews_new['positive_review'] = df_reviews_new['positive_review'].fillna(0)
df1 = df_reviews_new[['listing_id',
                      'sentiment_score',
                      'positive_review',
                      'neutral_review',
                      'negative_review']]
group2 = df1.groupby('listing_id', as_index=False).agg('sum')
final_1 = final.merge(group2, on='listing_id')
final_1.drop(columns='sentiment_score', inplace=True)
final_1['positive_review'] = final_1['positive_review'].astype(int)
final_1['negative_review'] = final_1['negative_review'].astype(int)
final_1['neutral_review'] = final_1['neutral_review'].astype(int)

# Make monthwise data
df_final1_copy = df_final1
df_final1_copy['date'] = df_reviews_new['date']
df_final1_copy['sentiment_score'] = \
    df_reviews_new['sentiment_score']
df_final1_copy['total_score'] = \
    df_final1_copy['overall_score_pt'] + \
    df_final1_copy['review_score_pt'] + \
    df_final1_copy['reviewer_score_pt']
df_final1_copy.drop(columns=['overall_score_pt',
                             'review_score_pt',
                             'reviewer_score_pt',
                             'host_score_pt',
                             'cancel_flag'], inplace=True)
df_final1_copy['sentiment_score'] = df_final1_copy['sentiment_score']*100
df_final1_copy['sentiment_score'] = \
    df_final1_copy['sentiment_score'].astype(int)
df_final1_copy['month_year'] = \
    pd.to_datetime(df_final1_copy['date']).dt.to_period('M')
df_final1_copy.drop(columns='date', inplace=True)
m3 = df_listing[['listing_id', 'availability_30']]
df_final2 = df_final1_copy.merge(m3, on='listing_id')
df_final2 = df_final2.groupby(['listing_id',
                               'month_year'], as_index=False).mean()
df_final2_new = df_final2.groupby('listing_id').\
    head(4).reset_index(drop=True)
gg = df_final2_new.groupby('listing_id', as_index=False).count()
listing_id_final = gg[gg['month_year'] == 4]['listing_id']
df_final2_new1 = \
    df_final2_new[df_final2_new['listing_id'].isin(listing_id_final)]
date = df_final2_new1['month_year']
df_final2_new1 = df_final2_new1.astype(int)
df_final2_new1['month_year'] = date
final_2 = final_1[final_1['listing_id'].isin(listing_id_final)]

# Convert to csv
final_2.to_csv('listing_score1.csv')
df_final2_new1.to_csv('monthly_score1.csv')




