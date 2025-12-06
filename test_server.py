"""Minimal Flask server for testing Child ID Card"""
from flask import Flask, jsonify, render_template, send_file
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
        <p><strong>Note:</strong> This is the test server with limited features. 
        The full application with 60+ routes including meal planning, analytics, health info, 
        immunization tracking, growth monitoring, nutrition lookup, WHO vaccines, chatbot, 
        and village economy features is currently unavailable due to dependency issues.</p>
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
    print("\n" + "="*60)
    print("API CALLED: /api/get-children")
    print("="*60)
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT id, name, date_of_birth, gender, village
            FROM children
            WHERE id != 1
            ORDER BY name ASC
        """
        print(f"Executing SQL:\n{query}")
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
        print(f"SUCCESS: Returning {len(children)} children")
        print("="*60 + "\n")
        return jsonify({'success': True, 'children': children})
    except Exception as e:
        import traceback
        print(f"ERROR OCCURRED:")
        print(f"Error message: {e}")
        print(f"\nFull traceback:")
        traceback.print_exc()
        print("="*60 + "\n")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/child-identity/create/<int:child_id>', methods=['POST'])
def create_child_card(child_id):
    """Create child identity card with QR code"""
    print(f"\n🎫 Creating card for child ID: {child_id}")
    try:
        card_number = card_manager.generate_card_number(child_id)
        qr_code_id = card_manager.generate_qr_code_id(child_id)
        
        # Generate complete child data for QR
        child_data = card_manager.get_child_data_for_qr(child_id)
        
        if not child_data:
            return jsonify({'success': False, 'message': 'Child not found'})
        
        # Store card info in database
        import json
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO child_identity_cards 
            (child_id, card_number, qr_code_id, qr_code_data, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (child_id, card_number, qr_code_id, json.dumps(child_data), datetime.now().isoformat()))
        conn.commit()
        conn.close()
        
        print(f"Card created: {card_number}")
        return jsonify({
            'success': True,
            'card_number': card_number,
            'qr_code_id': qr_code_id
        })
    except Exception as e:
        import traceback
        print(f"Error creating card: {e}")
        traceback.print_exc()
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/child-identity/get/<int:child_id>', methods=['GET'])
def get_child_card(child_id):
    """Get child identity card data"""
    try:
        # Get card from database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT card_number, qr_code_id, created_at
            FROM child_identity_cards
            WHERE child_id = ?
        """, (child_id,))
        
        card = cursor.fetchone()
        conn.close()
        
        if not card:
            return jsonify({'success': False, 'message': 'Card not found'})
        
        # Get complete child data for display
        child_data = card_manager.get_child_data_for_qr(child_id)
        
        return jsonify({
            'success': True,
            'card': {
                'card_number': card['card_number'],
                'qr_code_id': card['qr_code_id'],
                'created_at': card['created_at'],
                'qr_data': child_data
            }
        })
    except Exception as e:
        print(f"Error getting card: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/child-identity/qr/<int:child_id>', methods=['GET'])
def get_qr_code(child_id):
    """Generate and return QR code image"""
    try:
        child_data = card_manager.get_child_data_for_qr(child_id)
        if not child_data:
            return jsonify({'error': 'Child not found'}), 404
        
        # Generate QR code
        qr_image = card_manager.create_qr_code_image(child_data)
        
        # Convert to bytes
        img_io = BytesIO()
        qr_image.save(img_io, 'PNG')
        img_io.seek(0)
        
        return send_file(img_io, mimetype='image/png')
    except Exception as e:
        print(f"Error generating QR: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/child-identity/emergency-contact', methods=['POST'])
def add_emergency_contact():
    """Add emergency contact for child"""
    from flask import request
    try:
        data = request.get_json()
        child_id = data.get('child_id')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get current max priority
        cursor.execute("SELECT MAX(priority) FROM emergency_contacts WHERE child_id = ?", (child_id,))
        max_priority = cursor.fetchone()[0] or 0
        
        cursor.execute("""
            INSERT INTO emergency_contacts 
            (child_id, contact_name, contact_type, phone_number, relationship, priority)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            child_id,
            data.get('contact_name'),
            data.get('contact_type', 'Emergency'),
            data.get('phone_number'),
            data.get('relationship'),
            max_priority + 1
        ))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error adding contact: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/child-identity/family-health-risk', methods=['POST'])
def add_family_risk():
    """Add family health risk for child"""
    from flask import request
    try:
        data = request.get_json()
        child_id = data.get('child_id')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO family_health_risks 
            (child_id, condition_name, severity, family_member, precautions)
            VALUES (?, ?, ?, ?, ?)
        """, (
            child_id,
            data.get('condition_name'),
            data.get('severity'),
            data.get('family_member'),
            data.get('precautions', '')
        ))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error adding family risk: {e}")
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    print("="*60)
    print("MINIMAL TEST SERVER FOR CHILD ID CARD")
    print("="*60)
    print("URL: http://127.0.0.1:5000/child-identity-card")
    print("="*60)
    app.run(debug=False, port=5000, host='0.0.0.0')
