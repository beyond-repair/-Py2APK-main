import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer


class SentimentClassifier:
    """Performs sentiment analysis on input text."""

    def __init__(self, model_name="distilbert-base-uncased-"
                 "finetuned-sst-2-english"):
        """Initializes model and tokenizer."""
        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_name
        ).to(self.device)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def predict_sentiment(self, text: str) -> str:
        """Predicts sentiment (positive/negative) of the given text."""
        inputs = self.tokenizer(text, return_tensors="pt").to(self.device)
        with torch.no_grad():
            outputs = self.model(**inputs)
            predictions = torch.argmax(outputs.logits, dim=-1)
        return "positive" if predictions.item() == 1 else "negative"


# Example usage (for testing purposes)
if __name__ == "__main__":
    classifier = SentimentClassifier()
    text = "This is a great movie! I really enjoyed it."
    sentiment = classifier.predict_sentiment(text)
    print(f"Sentiment: {sentiment}")