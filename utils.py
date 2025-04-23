import re
from typing import List, Dict
import string
from collections import Counter
import numpy as np

def preprocess_text(text: str) -> str:
    """Basic text preprocessing."""
    # Convert to lowercase
    text = text.lower()
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text

def calculate_text_features(text: str) -> Dict[str, float]:
    """Calculate various text features for style analysis."""
    words = text.split()
    sentences = re.split(r'[.!?]', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # Basic statistics
    word_count = len(words)
    sentence_count = len(sentences)
    avg_word_length = sum(len(word) for word in words) / word_count if word_count else 0
    avg_sentence_length = word_count / sentence_count if sentence_count else 0
    
    # Word frequency distribution
    word_freq = Counter(words)
    unique_words = len(word_freq)
    lexical_diversity = unique_words / word_count if word_count else 0
    
    # Common style markers
    features = {
        'word_count': word_count,
        'sentence_count': sentence_count,
        'avg_word_length': avg_word_length,
        'avg_sentence_length': avg_sentence_length,
        'lexical_diversity': lexical_diversity,
        'unique_words': unique_words
    }
    
    return features

def normalize_features(features: Dict[str, float]) -> Dict[str, float]:
    """Normalize feature values to 0-1 range."""
    # These are example ranges - in a real system you'd use actual data distributions
    max_values = {
        'word_count': 1000,
        'sentence_count': 50,
        'avg_word_length': 10,
        'avg_sentence_length': 30,
        'lexical_diversity': 1,
        'unique_words': 500
    }
    
    normalized = {}
    for key, value in features.items():
        max_val = max_values.get(key, 1)
        normalized[key] = min(value / max_val, 1) if max_val else 0
    
    return normalized

def calculate_feature_distance(features1: Dict[str, float], features2: Dict[str, float]) -> float:
    """Calculate Euclidean distance between two sets of normalized features."""
    keys = set(features1.keys()).union(set(features2.keys()))
    squared_diff = sum((features1.get(k, 0) - features2.get(k, 0))**2 for k in keys)
    return np.sqrt(squared_diff)

def get_ngrams(text: str, n: int) -> List[str]:
    """Generate n-grams from text."""
    words = text.split()
    return [' '.join(words[i:i+n]) for i in range(len(words)-n+1)]