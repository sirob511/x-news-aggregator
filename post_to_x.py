import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Load credentials from .env
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

# Endpoint and tweet text
tweet_text = "Hello world! 👋 This is my first post using the v2 Twitter API."

url = "https://api.twitter.com/2/tweets"

# Use OAuth1 for authentication
from requests_oauthlib import OAuth1

auth = OAuth1(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Send the tweet
response = requests.post(url, json={"text": tweet_text}, auth=auth)

if response.status_code == 201:
    print("Tweet posted successfully.")
else:
    print(f"Tweet failed: {response.status_code} - {response.text}")
