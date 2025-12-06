"""Simple Flask server for Child ID Card features"""
from flask import Flask, jsonify, render_template, send_file, request
import sqlite3
from datetime import datetime
from io import BytesIO
from child_identity_qr import ChildIdentityCard

app = Flask(__name__)
card_manager = ChildIdentityCard()

def get_db_connection():
    conn = sqlite3.connect('nutrition_advisor.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return """
    <html>
    <head><title>AI Nutrition Advisor</title></head>
    <body>
        <h1>AI Nutrition Advisor</h1>
        <h2>Available Features:</h2>
        <ul>
            <li><a href='/child-identity-card'>Child ID Card</a> - Generate QR codes for children</li>
            <li><a href='/child-identity-scanner'>ASHA Scanner</a> - Scan child QR codes</li>
        </ul>
        <p><strong>Note:</strong> This is a limited test server. 
        The full application with meal planning, analytics, health tracking, 
        and other features is currently unavailable.</p>
    </body>
    </html>
    """

@app.route('/child-identity-card')
def child_card():
    return render_template('child_identity_card.html')

@app.route('/child-identity-scanner')
def child_scanner():
    return render_template('child_scanner.html')

@app.route('/api/get-children', methods=['GET'])
def api_get_children():
    """Get all children"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT id, name, date_of_birth, gender, village
            FROM children
            WHERE id != 1
            ORDER BY name ASC
        """
        cursor.execute(query)
        
        children = []
        for row in cursor.fetchall():
            dob = datetime.strptime(row['date_of_birth'], '%Y-%m-%d')
            age = (datetime.now() - dob).days // 365
            
            children.append({
                'id': row['id'],
                'name': row['name'],
                'date_of_birth': row['date_of_birth'],
                'gender': row['gender'],
                'village': row['village'] if row['village'] else 'N/A',
                'age': age
            })
        
        conn.close()
        return jsonify({'success': True, 'children': children})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/child-identity/create/<int:child_id>', methods=['POST'])
def api_create_card(child_id):
    """Create child identity card"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM children WHERE id = ?", (child_id,))
        child = cursor.fetchone()
        
        if not child:
            return jsonify({'success': False, 'error': 'Child not found'})
        
        card_number = card_manager.create_card(
            child_id=child_id,
            child_name=child['name'],
            date_of_birth=child['date_of_birth'],
            gender=child['gender'],
            village=child['village']
        )
        
        conn.close()
        return jsonify({'success': True, 'card_number': card_number})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/child-identity/get/<int:child_id>', methods=['GET'])
def api_get_card(child_id):
    """Get child identity card data"""
    try:
        card_data = card_manager.get_card_data(child_id)
        
        if card_data:
            return jsonify({'success': True, 'card': card_data})
        else:
            return jsonify({'success': False, 'error': 'Card not found'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/child-identity/qr/<int:child_id>', methods=['GET'])
def api_get_qr(child_id):
    """Get QR code image for child"""
    try:
        qr_image = card_manager.generate_qr_image(child_id)
        
        if qr_image:
            img_io = BytesIO()
            qr_image.save(img_io, 'PNG')
            img_io.seek(0)
            return send_file(img_io, mimetype='image/png')
        else:
            return jsonify({'success': False, 'error': 'QR code not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/child-identity/emergency-contact', methods=['POST'])
def api_add_emergency_contact():
    """Add emergency contact"""
    try:
        data = request.json
        card_manager.add_emergency_contact(
            child_id=data['child_id'],
            contact_name=data['contact_name'],
            relationship=data['relationship'],
            phone=data['phone']
        )
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/child-identity/family-health-risk', methods=['POST'])
def api_add_family_health_risk():
    """Add family health risk"""
    try:
        data = request.json
        card_manager.add_family_health_risk(
            child_id=data['child_id'],
            risk_type=data['risk_type'],
            details=data.get('details', '')
        )
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    print("Starting server on http://127.0.0.1:5000")
    try:
        app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
    except KeyboardInterrupt:
        print("\nServer stopped")
    except Exception as e:
        print(f"Server error: {e}")
