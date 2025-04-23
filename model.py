import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random
from typing import Dict, Union

class TextGenerator:
    def __init__(self):
        # Initialize any required models or parameters
        self.style_templates = {
            'formal': "After careful consideration of the given input: '{prompt}', it can be concluded that the most appropriate response would be as follows. The analysis indicates that {filler}.",
            'casual': "Hey! So about '{prompt}' - I was thinking, you know, maybe like {filler}. But what do I know, right?",
            'technical': "The input '{prompt}' can be processed according to the following technical specifications. Parameters include {filler}, resulting in an optimal output configuration.",
            'creative': "The whisper of '{prompt}' danced through the imagination, weaving a tapestry of {filler} that sparkled with possibility.",
            'shakespearean': "Verily, upon hearing '{prompt}', mine own heart didst proclaim: {filler}, and thus the tale unfolds.",
            'hemingway': "It was a good prompt. '{prompt}'. He drank his coffee. The coffee was strong. {filler}. That was all.",
            'academic': "Recent scholarship on '{prompt}' (Smith et al., 2023) suggests that {filler}, with significant implications for future research.",
            'journalistic': "BREAKING: New developments in '{prompt}' have experts stunned. Sources reveal that {filler}, potentially changing everything.",
            'custom': "In the requested style, the prompt '{prompt}' might be expressed as follows: {filler}."
        }
        
        self.filler_phrases = [
            "a comprehensive analysis of the available data",
            "an interesting perspective worth considering",
            "a multifaceted approach to problem-solving",
            "a remarkable discovery that challenges assumptions",
            "a nuanced interpretation of the facts",
            "a compelling narrative that engages the reader",
            "a thorough examination of the underlying principles",
            "a creative solution to the presented challenge"
        ]
    
    def generate(self, prompt: str, style: str = 'formal') -> str:
        """Generate text in the specified style based on the given prompt."""
        template = self.style_templates.get(style, self.style_templates['formal'])
        filler = random.choice(self.filler_phrases)
        
        return template.format(prompt=prompt, filler=filler)
    
    def save_model(self, filename: str):
        """Save the model to a file (placeholder implementation)."""
        # In a real implementation, this would save the model state
        with open(filename, 'w') as f:
            f.write("Model state would be saved here in a real implementation")
        return True

class StyleAnalyzer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 3),
            max_features=5000
        )
    
    def compare(self, text1: str, text2: str, improved_model: bool = False) -> Dict[str, Union[float, bool, str]]:
        """Compare the writing styles of two texts and return similarity metrics."""
        # Vectorize the texts
        vectors = self.vectorizer.fit_transform([text1, text2])
        
        # Calculate cosine similarity
        similarity = cosine_similarity(vectors[0], vectors[1])[0][0]
        similarity_score = round(similarity * 100, 2)
        
        # Determine if same author (simplified heuristic)
        if improved_model:
            same_author = similarity_score > 75
            confidence = min(100, max(50, similarity_score + random.uniform(-10, 10)))
        else:
            same_author = similarity_score > 65
            confidence = min(100, max(40, similarity_score + random.uniform(-15, 15)))
        
        # Generate analysis text
        analysis = self._generate_analysis(similarity_score, same_author)
        
        return {
            'similarity_score': similarity_score,
            'same_author': same_author,
            'confidence': round(confidence, 2),
            'analysis': analysis
        }
    
    def _generate_analysis(self, score: float, same_author: bool) -> str:
        """Generate human-readable analysis of the style comparison."""
        if score > 80:
            desc = "The texts show very strong stylistic similarities, with nearly identical patterns in word choice, sentence structure, and rhetorical devices."
        elif score > 60:
            desc = "The texts demonstrate significant stylistic overlap, sharing many characteristics in their writing patterns."
        elif score > 40:
            desc = "The texts have moderate stylistic similarities, with some common elements but also noticeable differences."
        else:
            desc = "The texts show minimal stylistic similarities, with distinct writing patterns and approaches."
        
        if same_author:
            desc += " The consistent stylistic markers suggest these texts were likely written by the same author."
        else:
            desc += " The divergent stylistic elements indicate these texts were probably written by different authors."
        
        return desc
    
    def save_model(self, filename: str):
        """Save the model to a file (placeholder implementation)."""
        # In a real implementation, this would save the model state
        with open(filename, 'w') as f:
            f.write("Model state would be saved here in a real implementation")
        return True