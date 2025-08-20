from apps.digest.models import Article
from apps.digest.summarizer import generate_summary

qs = Article.objects(summary__in=["", None])[:5]
print("Total to process:", qs.count())

for idx, a in enumerate(qs):
    print(f"\n[{idx+1}] Title:", a.title)
    print("    Text length:", len(a.text) if a.text else 0)

    if not a.text:
        print("    ❌ No text, skipping.")
        continue

    try:
        print("    Calling summarizer...")
        summary = generate_summary(a.text[:500])
        print("    Got summary:", summary[:100])
        a.summary = summary
        a.save()
        print("    ✅ Saved")
    except Exception as e:
        print("    ❌ Error:", e)
