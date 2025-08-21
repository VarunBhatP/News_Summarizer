import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

import string
stop_words = set(stopwords.words("english"))

def extract_keywords(text: str, max_keywords: int = 5):
    if not text:
        return []
    tokens = word_tokenize(text.lower())
    words = [w for w in tokens if w.isalpha() and w not in stop_words]
    freq = nltk.FreqDist(words)
    return [word for word, _ in freq.most_common(max_keywords)]
