import tweepy
import os
from dotenv import load_dotenv
import logging

import tweepy.errors




load_dotenv()
load_dotenv()

def authenticate_twitter_api():
    consumer_key = os.getenv('API_KEY')
    consumer_secret = os.getenv('API_SECRET_KEY')
    access_token = os.getenv('ACCESS_TOKEN')
    access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

    auth = tweepy.OAuth1UserHandler(
        consumer_key, consumer_secret, access_token, access_token_secret
    )
    return tweepy.API(auth)

def search_tweets(query, count,  api):
    try:
        results = api.search_tweets(q=query, count=count)
        return results
    except tweepy.errors.TooManyRequests as e:
        print(f"An error occurred: {e}")
        return None



