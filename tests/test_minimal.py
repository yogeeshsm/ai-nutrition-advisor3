"""Ultra-minimal Flask server for testing"""
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head><title>AI Nutrition Advisor - TEST</title></head>
    <body>
        <h1>✅ SERVER IS RUNNING!</h1>
        <p>If you see this, Flask is working correctly.</p>
        <h2>Test Links:</h2>
        <ul>
            <li><a href="/test">Test Route</a></li>
        </ul>
    </body>
    </html>
    '''

@app.route('/test')
def test():
    return '<h1>Test route works!</h1>'

if __name__ == '__main__':
    print("="*60)
    print("MINIMAL TEST SERVER")
    print("Open: http://127.0.0.1:5000")
    print("="*60)
    app.run(host='0.0.0.0', port=5000, debug=True)
