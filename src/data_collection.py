import pandas as pd
import tweepy
import tweepy.errors
from src.twitter_api import authenticate_twitter_api,search_tweets
from dotenv import load_dotenv
import os 
import logging 
import requests
import time

load_dotenv()
logging.basicConfig(level=logging.ERROR)


def ensure_dir():
    if not os.path.exists("data"):
        os.makedirs("data")


def collect_samsung_tweets():
        auth = authenticate_twitter_api()
        querry = "Samsung"
        count = 100
        max_retries = 3
        retries = 0
        data = {
            "tweet": [],
            "location": [],
            "date": [],
            "language": [],
            "retweet_count": [],
            "like_count": [],
            "verifier": [],
            "user_id": [],
            "hash_tags": [],

        }
        while retries < max_retries:
            try: 

                values_scraping = search_tweets(query=querry,count=count,api = auth)
                if values_scraping is None:
                    logging.error("Failed to retrieve tweets")
                    return None

            
                for value in values_scraping:
                    data["tweet"].append(value.text)
                    data["location"].append(value.user.location)
                    data["date"].append(value.created_at)
                    data["language"].append(value.lang)
                    data["retweet_count"].append(value.retweet_count)
                    data["like_count"].append(value.favorite_count)
                    data["verifier"].append(value.user.verified)
                    data["user_id"].append(value.user.id)
                    data["hash_tags"].append([hashtag['text'] for hashtag in value.entities['hashtags']])
                    print(f"Tweet {len(data['tweet'])} scraped")


                
                break
            except tweepy.errors.TooManyRequests as e:
                    retries += 1
                    logging.error(f"Rate limit reached: {e}")
                    time.sleep(60)
            

            if data['tweet']:
                df = pd.DataFrame(data)
                ensure_dir()
                df.to_csv("data/samsung_tweets.csv", index=False)
                print("Data scraped successfully")
                return df
            else:
                print("No data was collected")
                return None


def test_api_access():
    client = authenticate_twitter_api()
    try:
        # Try to fetch your own user info
        me = client.get_me()
        print(f"Successfully fetched user info: @{me.data.username}")
        
        # Try to fetch a tweet
        tweet = client.get_tweet('1460323737035677698')  # Using a known tweet ID
        print(f"Successfully fetched tweet: {tweet.data.text}")
        
    except Exception as e:
        print(f"Error testing API access: {e}")