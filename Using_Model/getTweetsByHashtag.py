from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Create a sid object called SentimentIntensityAnalyzer()
sid = SentimentIntensityAnalyzer()
import geocoder

def get_trends(api, loc):
    # Object that has location's latitude and longitude.
    g = geocoder.osm(loc)

    closest_loc = api.closest_trends(g.lat, g.lng)
    trends = api.get_place_trends(closest_loc[0]["woeid"])
    return trends[0]["trends"]

from tweepy import OAuthHandler
# from tweepy.streaming import StreamListener
import tweepy
import json
import pandas as pd
import csv
import re
# from textblob import TextBlob
import string
# import preprocessor as p
import os
import time
# from sentimentAnalysis import VaderAnalysis

# import configparser


from dotenv import load_dotenv

load_dotenv()

consumer_key = os.getenv('consumer_key')
consumer_secret = os.getenv('consumer_secret')
access_key = os.getenv('access_key')
access_secret = os.getenv('access_secret')
# Pass your twitter credentials to tweepy via its OAuthHandler
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)
trends = get_trends(api, "India")


def get_n_tweets(api, hashtag, n, lang=None):
    tweets = tweepy.Cursor(
        api.search_tweets,
        q=hashtag,
        lang=lang,
        tweet_mode = 'extended'
    ).items(n)
    return tweets

tweet_list = []
for hashtag in trends:
    tweets = get_n_tweets(api, hashtag['name'], 1)
    current_list = [tweet for tweet in tweets]
    tweet_list += current_list
    
db_tweets = pd.DataFrame(columns = ['username', 'text', 'sentiment'])

for tweet in tweet_list:
# Pull the values
    username = tweet.user.screen_name
    try:
        text = tweet.retweeted_status.full_text
    except AttributeError:  # Not a Retweet
        text = tweet.full_text
    sentiment = sid.polarity_scores(str(text))
    if(sentiment['compound'] < 0):
        ith_tweet = [username, text, sentiment]
        db_tweets.loc[len(db_tweets)] = ith_tweet
    
db_tweets.to_csv('sentiment_1.csv', index = False)