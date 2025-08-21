from django.core.management.base import BaseCommand
from apps.digest.pipeline import fetch_and_store_articles

class Command(BaseCommand):
    help = "Fetch RSS and summarize for all sources (or a single category)."

    def add_arguments(self, parser):
        parser.add_argument("--category", type=str, default=None)

    def handle(self, *args, **options):
        category = options.get("category")
        fetch_and_store_articles(category)
        self.stdout.write(self.style.SUCCESS(f"Done: {category or 'all categories'}"))
