from django.core.management.base import BaseCommand
from apps.digest.pipeline import fetch_and_store_articles
from apps.digest.models import Article
from apps.digest.summarizer import generate_summary

class Command(BaseCommand):
    help = "Fetch RSS articles and generate summaries"

    def handle(self, *args, **kwargs):
        self.stdout.write("🔄 Fetching articles...")
        fetch_and_store_articles()

        self.stdout.write("✂️ Generating summaries...")
        for a in Article.objects(summary__in=["", None]):
            if a.text:
                a.summary = generate_summary(a.text[:2000])
                a.save()
                self.stdout.write(f"✅ {a.title}")
        
        self.stdout.write("🎉 Done!")
