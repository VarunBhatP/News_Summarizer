from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.luhn import LuhnSummarizer

def summarize_text(text: str, sentence_count: int = 2) -> str:
    try:
        parser = PlaintextParser.from_string(text or "", Tokenizer("english"))
        summarizer = LuhnSummarizer()
        summary = summarizer(parser.document, sentence_count)
        return " ".join(str(sentence) for sentence in summary) or (text or "")[:200]
    except Exception:
        return (text or "")[:200]
