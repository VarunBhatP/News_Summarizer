from django.core.management.base import BaseCommand
from apps.digest.services.rss import fetch_and_store_articles

class Command(BaseCommand):
    help = "Fetch latest articles from all RSS sources and store in DB"

    def handle(self, *args, **options):
        self.stdout.write("Fetching latest articles...")
        fetch_and_store_articles()
        self.stdout.write(self.style.SUCCESS("Articles fetched and stored successfully."))
