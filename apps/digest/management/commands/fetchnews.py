from django.core.management.base import BaseCommand
from apps.digest.pipeline import fetch_and_store_news

class Command(BaseCommand):
    help = "Fetch latest news and store in MongoDB"

    def add_arguments(self, parser):
        parser.add_argument("--category", type=str, default="general")

    def handle(self, *args, **options):
        category = options["category"]
        fetch_and_store_news(category)
        self.stdout.write(self.style.SUCCESS(f"News fetched for {category}!"))
