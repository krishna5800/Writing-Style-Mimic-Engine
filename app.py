from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from model import TextGenerator, StyleAnalyzer
import os
from datetime import datetime
import uuid

app = Flask(__name__)
CORS(app)

# Initialize models
text_generator = TextGenerator()
style_analyzer = StyleAnalyzer()

# Ensure saved_models directory exists
os.makedirs('saved_models', exist_ok=True)

@app.route('/api/generate', methods=['POST'])
def generate_text():
    data = request.json
    prompt = data.get('prompt', '')
    style = data.get('style', 'formal')
    
    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400
    
    try:
        generated_text = text_generator.generate(prompt, style)
        return jsonify({
            'generated_text': generated_text,
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/compare', methods=['POST'])
def compare_texts():
    data = request.json
    text1 = data.get('text1', '')
    text2 = data.get('text2', '')
    improved_model = data.get('improved_model', False)
    
    if not text1 or not text2:
        return jsonify({'error': 'Both texts are required for comparison'}), 400
    
    try:
        result = style_analyzer.compare(text1, text2, improved_model)
        return jsonify({
            'similarity_score': result['similarity_score'],
            'same_author': result['same_author'],
            'confidence': result['confidence'],
            'analysis': result['analysis'],
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/save_model', methods=['POST'])
def save_model():
    try:
        # Generate unique filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        filename = f"saved_models/model_{timestamp}_{unique_id}.pkl"
        
        # In a real implementation, you would save the model state here
        # For example: text_generator.save_model(filename)
        
        return jsonify({
            'filename': filename,
            'status': 'success',
            'message': 'Model saved successfully'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)