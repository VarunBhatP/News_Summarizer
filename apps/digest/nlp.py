import re
import heapq
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

nltk.download("punkt")
nltk.download("stopwords")

def summarize_text_simple(text, max_sentences=3):
    """Simple frequency-based extractive summarizer"""
    sentences = sent_tokenize(text)
    if len(sentences) <= max_sentences:
        return text  # no need to summarize

    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words("english"))
    word_frequencies = {}

    for word in words:
        if word.isalpha() and word not in stop_words:
            word_frequencies[word] = word_frequencies.get(word, 0) + 1

    max_freq = max(word_frequencies.values())
    for word in word_frequencies:
        word_frequencies[word] /= max_freq

    sentence_scores = {}
    for sent in sentences:
        for word in word_tokenize(sent.lower()):
            if word in word_frequencies:
                sentence_scores[sent] = sentence_scores.get(sent, 0) + word_frequencies[word]

    best_sentences = heapq.nlargest(max_sentences, sentence_scores, key=sentence_scores.get)
    return " ".join(best_sentences)
