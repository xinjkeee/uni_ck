from transformers import pipeline
from django.conf import settings
import re
import logging

logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    _instance = None
    _analyzer = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SentimentAnalyzer, cls).__new__(cls)
            try:
                # Use a model better suited for book reviews
                cls._analyzer = pipeline(
                    "sentiment-analysis",
                    model="nlptown/bert-base-multilingual-uncased-sentiment",
                    device=-1  # Use CPU
                )
            except Exception as e:
                logger.error(f"Failed to initialize sentiment analyzer: {str(e)}")
                # Fallback to a simpler model if the main one fails
                try:
                    cls._analyzer = pipeline(
                        "sentiment-analysis",
                        model="distilbert-base-uncased-finetuned-sst-2-english",
                        device=-1
                    )
                except Exception as e:
                    logger.error(f"Failed to initialize fallback sentiment analyzer: {str(e)}")
                    cls._analyzer = None
        return cls._instance

    def analyze(self, text):
        """
        Analyze the sentiment of the given text.
        Returns a tuple of (sentiment, confidence)
        where sentiment is one of: 'positive', 'negative', 'neutral'
        """
        if not text:
            return 'neutral', 0.5

        # Check for strong negative expressions first
        negative_patterns = [
            r"very bad",
            r"terrible",
            r"awful",
            r"horrible",
            r"worst",
            r"disappointing",
            r"waste of time",
            r"don't buy",
            r"don't read",
            r"hate",
            r"dislike",
            r"poor",
            r"not worth",
            r"avoid",
            r"regret"
        ]

        # Check for strong positive expressions
        positive_patterns = [
            r"excellent",
            r"amazing",
            r"wonderful",
            r"fantastic",
            r"great",
            r"best",
            r"love",
            r"highly recommend",
            r"must read",
            r"brilliant",
            r"outstanding",
            r"superb",
            r"masterpiece",
            r"enjoyed",
            r"loved"
        ]

        text_lower = text.lower()
        
        # Check for strong negative expressions
        for pattern in negative_patterns:
            if re.search(pattern, text_lower):
                return 'negative', 0.9

        # Check for strong positive expressions
        for pattern in positive_patterns:
            if re.search(pattern, text_lower):
                return 'positive', 0.9

        # If no strong expressions found and model is available, use the model
        if self._analyzer is not None:
            try:
                result = self._analyzer(text)[0]
                label = result['label']
                score = result['score']
                
                # Map the model's 5-star rating to our sentiment choices
                # 1-2 stars: negative
                # 3 stars: neutral
                # 4-5 stars: positive
                if label in ['1 star', '2 stars']:
                    return 'negative', score
                elif label == '3 stars':
                    return 'neutral', score
                else:
                    return 'positive', score
            except Exception as e:
                logger.error(f"Error in sentiment analysis: {str(e)}")
                # Fallback to pattern-based analysis
                return self._fallback_analysis(text_lower)
        else:
            # If model is not available, use fallback analysis
            return self._fallback_analysis(text_lower)

    def _fallback_analysis(self, text_lower):
        """
        Fallback sentiment analysis using simple word counting
        """
        positive_words = ['good', 'great', 'enjoy', 'like', 'love', 'recommend']
        negative_words = ['bad', 'poor', 'dislike', 'hate', 'terrible', 'awful']
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return 'positive', 0.7
        elif negative_count > positive_count:
            return 'negative', 0.7
        else:
            return 'neutral', 0.5 