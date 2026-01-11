"""Simple test to verify trained model works in Flask"""
from flask import Flask, jsonify
from malnutrition_predictor import get_predictor

app = Flask(__name__)

@app.route('/test-prediction')
def test_prediction():
    predictor = get_predictor()
    result = predictor.predict(59, 18.0, 109.0)
    return jsonify({
        'test': 'Lakshmi (59mo, 18kg, 109cm)',
        'status': result['nutrition_status'],
        'risk': result['risk_level'],
        'confidence': result['confidence']
    })

if __name__ == '__main__':
    print("Starting test server on port 5001...")
    app.run(port=5001, debug=False)
