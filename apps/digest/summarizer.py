from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.luhn import LuhnSummarizer

def generate_summary(text: str, sentence_count: int = 2) -> str:
    try:
        print(">>> generate_summary called, text length:", len(text))
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LuhnSummarizer()
        summary = summarizer(parser.document, sentence_count)
        return " ".join(str(sentence) for sentence in summary)
    except Exception as e:
        print("Summary Error:", e)
        return ""
