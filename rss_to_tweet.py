import os
import feedparser
import requests
from dotenv import load_dotenv
from requests_oauthlib import OAuth1
import random
import json
from pathlib import Path
import argparse

# Load env vars
load_dotenv()

# X API credentials
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

# RSS feed URL
#FEED_URL = "https://www.infoq.com/feed/"
#FEED_URL = "https://dev.to/t/rss"

FEED_URLS = [
    "https://netflixtechblog.com/feed",
    "https://www.wired.com/feed/rss",
    "https://techcrunch.com/feed/",
    "https://aws.amazon.com/blogs/aws/feed/",
    "http://highscalability.com/blog/rss.xml",
    "https://cloud.google.com/blog/rss/",
    "https://azure.microsoft.com/en-us/blog/feed/",
    "https://www.thoughtspot.com/blog/feed/",
    "https://hnrss.org/frontpage",           # now first
    "https://www.infoq.com/feed/"            # now second
]

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
def fetch_latest_article(feed_urls):
    posted_links = load_posted_links()

    for feed_url in feed_urls:
        feed = feedparser.parse(feed_url)
        if not feed.entries:
            continue

        for entry in feed.entries:
            title = entry.title
            link = entry.link

            # Clean common prefixes
            for prefix in ["Presentation: ", "Article: ", "News: "]:
                if title.startswith(prefix):
                    title = title[len(prefix):]

            if link not in posted_links:
                comment = random.choice(comment_templates)
                full_tweet = f"{comment} {title}\n{link}"
                return title, link, full_tweet

    return None, None, None


# Post to X
def post_to_x(text):
    url = "https://api.twitter.com/2/tweets"
    auth = OAuth1(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    response = requests.post(url, json={"text": text}, auth=auth)
    return response.status_code, response.text

# Parse CLI arguments
parser = argparse.ArgumentParser(description="Curated Digest Bot")
parser.add_argument("--dry-run", action="store_true", help="Print tweet but do not post")
args = parser.parse_args()

if __name__ == "__main__":
    print("Running RSS to X integration...")
    
    random.shuffle(FEED_URLS)
    title, link, tweet = fetch_latest_article(FEED_URLS)
    if tweet:
        if args.dry_run:
            print("Dry run: not posting to X.")
            print(f"Preview tweet:\n{tweet}")
        else:
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

