import time
from .services.rss import fetch_and_store_articles

def run():
    while True:
        print("Fetching new articles...")
        fetch_and_store_articles()
        time.sleep(1800)  # 30 minutes
