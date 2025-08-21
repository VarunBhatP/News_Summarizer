from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.luhn import LuhnSummarizer
import re


def summarize_text(text: str, sentence_count: int = 2) -> str:
    """
    Summarize text using Sumy Luhn algorithm.
    Fallback to first N sentences if Sumy fails.
    """

    if not text or not text.strip():
        return "No content to summarize."

    try:
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LuhnSummarizer()
        summary = summarizer(parser.document, sentence_count)

        result = " ".join(str(sentence) for sentence in summary)
        if result.strip():
            return result

        # Fallback: if summarizer returns empty
        return " ".join(re.split(r'(?<=[.!?]) +', text)[:sentence_count])

    except Exception as e:
        # Hard fallback: just return first 200 chars
        return (text or "")[:200] + f"\n[Fallback summarizer used: {e}]"
