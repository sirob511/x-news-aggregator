import os
import feedparser
import requests
from dotenv import load_dotenv
from requests_oauthlib import OAuth1

# Load env vars
load_dotenv()

# X API credentials
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

# RSS feed URL
FEED_URL = "https://www.infoq.com/feed/"

# Fetch latest article
def fetch_latest_article(feed_url):
    feed = feedparser.parse(feed_url)
    if not feed.entries:
        return None
    entry = feed.entries[0]
    title = entry.title
    link = entry.link
    return f"{title}\n{link}"

# Post to X
def post_to_x(text):
    url = "https://api.twitter.com/2/tweets"
    auth = OAuth1(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    response = requests.post(url, json={"text": text}, auth=auth)
    return response.status_code, response.text

if __name__ == "__main__":
    print("Running RSS to X integration...")
    tweet = fetch_latest_article(FEED_URL)
    if tweet:
        print(f"Tweet content:\n{tweet}")
        status, result = post_to_x(tweet)
        print(f"Tweet status: {status}")
        print(result)
    else:
        print("No articles found.")