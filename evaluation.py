from sklearn.metrics import accuracy_score

class StyleAccuracyChecker:
    def __init__(self, model):
        self.model = model
        self.true_labels = []
        self.pred_labels = []

    def evaluate(self, test_cases):
        """
        Evaluate model accuracy
        
        Args:
            test_cases: List of dictionaries with:
                - 'text1': first text
                - 'text2': second text 
                - 'label': 1 (same author) or 0 (different)
        
        Returns:
            dict: Accuracy metrics
        """
        predictions = []
        truths = []
        
        for case in test_cases:
            pred = self.model.compare(case['text1'], case['text2'])['same_author']
            predictions.append(1 if pred else 0)
            truths.append(case['label'])
        
        self.true_labels = truths
        self.pred_labels = predictions
        
        return {
            'accuracy': accuracy_score(truths, predictions),
            'correct': sum(1 for t,p in zip(truths,predictions) if t==p),
            'total': len(truths)
        }

# Usage Example:
if __name__ == "__main__":
    # Mock model (replace with your actual model)
    class MockModel:
        def compare(self, t1, t2):
            return {'same_author': len(t1.split()) > 5 and len(t2.split()) > 5}
    
    # Initialize
    evaluator = StyleAccuracyChecker(MockModel())
    
    # PROPERLY STRUCTURED TEST DATA
    test_cases = [
        {'text1': "Short text", 
         'text2': "Another short",
         'label': 0},  # Different authors
         
        {'text1': "Longer sample text here", 
         'text2': "Extended content example",
         'label': 1}   # Same author
    ]
    
    # Evaluate
    results = evaluator.evaluate(test_cases)
    print(f"Accuracy: {results['accuracy']:.1%} ({results['correct']}/{results['total']})")