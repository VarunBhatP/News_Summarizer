from nltk.tokenize import sent_tokenize

def generate_summary(text, max_sentences=2):
    """
    A very simple extractive summarizer:
    - Splits text into sentences
    - Returns the first N sentences
    """
    if not text:
        return ""

    sentences = sent_tokenize(text)
    return " ".join(sentences[:max_sentences])
