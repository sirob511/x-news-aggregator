import os
import feedparser
import requests
from dotenv import load_dotenv
from requests_oauthlib import OAuth1
import random
import json
from pathlib import Path

# Load env vars
load_dotenv()

# X API credentials
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

# RSS feed URL
FEED_URL = "https://www.infoq.com/feed/"

comment_templates = [
    "Interesting read on system architecture:",
    "Solid write-up worth a look:",
    "Insightful post on scale and design:",
    "For anyone thinking about infra tradeoffs:",
    "Today’s pick from the design trenches:",
]

POSTED_LINKS_FILE = "posted_links.json"

def load_posted_links():
    if not Path(POSTED_LINKS_FILE).exists():
        return set()
    with open(POSTED_LINKS_FILE, "r") as f:
        return set(json.load(f))

def save_posted_link(link):
    posted = load_posted_links()
    posted.add(link)
    with open(POSTED_LINKS_FILE, "w") as f:
        json.dump(list(posted), f, indent=2)


# Fetch latest article
def fetch_latest_article(feed_url):
    feed = feedparser.parse(feed_url)
    if not feed.entries:
        return None, None, None

    posted_links = load_posted_links()

    for entry in feed.entries:
        title = entry.title
        link = entry.link

        if link not in posted_links:
            comment = random.choice(comment_templates)
            full_tweet = f"{comment}\n{title}\n{link}"
            return title, link, full_tweet

    return None, None, None


# Post to X
def post_to_x(text):
    url = "https://api.twitter.com/2/tweets"
    auth = OAuth1(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    response = requests.post(url, json={"text": text}, auth=auth)
    return response.status_code, response.text

if __name__ == "__main__":
    print("Running RSS to X integration...")

    title, link, tweet = fetch_latest_article(FEED_URL)
    if tweet:
        print(f"Tweet content:\n{tweet}")
        status, result = post_to_x(tweet)
        print(f"Tweet status: {status}")
        print(result)

        if status == 201 or "duplicate content" in result.lower():
            save_posted_link(link)
            print("Link recorded.")
        else:
            print("Tweet failed and not recorded.")
    else:
        print("No new articles found to post.")

