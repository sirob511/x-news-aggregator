import feedparser
"""
rss_reader.py
This script fetches and displays articles from an RSS feed using the `feedparser` library.
Functions:
    fetch_articles(feed_url: str, max_articles: int = 5) -> None:
        Fetches and prints a specified number of articles from the given RSS feed URL.
Constants:
    FEED_URL (str): The default URL of the RSS feed to fetch articles from.
Usage:
    Run the script directly to fetch and display articles from the default RSS feed.
"""

FEED_URL = "https://www.infoq.com/feed/"

def fetch_articles(feed_url, max_articles=25):
    feed = feedparser.parse(feed_url)
    print(f"Feed Title: {feed.feed.title}\n")

    for entry in feed.entries[:max_articles]:
        title = entry.title
        link = entry.link
        author = getattr(entry, 'author', 'Unknown Author')
        published = getattr(entry, 'published', 'Unknown Date')
        
        print(f"Title: {title}")
        print(f"Author: {author}")
        print(f"Date: {published}")
        print(f"Link: {link}")
        print("-" * 40)

if __name__ == "__main__":
    fetch_articles(FEED_URL)
