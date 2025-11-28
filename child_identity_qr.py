"""
Child Identity Card - QR Code Generation & Management
Generates unique QR codes for each child containing:
- Vaccination data
- Nutrition levels
- Emergency contacts
- Family health risks
Can be scanned instantly by ASHA/Anganwadi workers
"""

import qrcode
import json
import sqlite3
import hashlib
from datetime import datetime
from io import BytesIO
import base64
import os
from dotenv import load_dotenv

load_dotenv()

class ChildIdentityCard:
    """Manages digital child identity cards with QR codes"""
    
    def __init__(self, db_path="nutrition_advisor.db"):
        self.db_path = db_path
        self.qr_version = 1  # Can hold ~2953 bytes of data
    
    def get_db_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def generate_card_number(self, child_id):
        """Generate unique card number (e.g., CHILD_982374)"""
        # Generate 6-digit number from child_id and timestamp
        timestamp = datetime.now().strftime("%H%M%S")
        unique_num = str(child_id).zfill(2) + timestamp[:4]
        card_number = f"CHILD_{unique_num}"
        return card_number
    
    def generate_qr_code_id(self, child_id):
        """Generate unique QR code identifier (same as card number for consistency)"""
        return self.generate_card_number(child_id)
    
    def get_child_vaccination_summary(self, child_id):
        """Get vaccination summary for QR code"""
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Get vaccination data from immunisation_schedule table
            cursor.execute("""
                SELECT COUNT(*) as total,
                       SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) as completed
                FROM immunisation_schedule
                WHERE child_id = ?
            """, (child_id,))
            
            result = cursor.fetchone()
            total = result['total'] or 0
            completed = result['completed'] or 0
            
            # Get next vaccine
            cursor.execute("""
                SELECT vaccine_name, due_date
                FROM immunisation_schedule
                WHERE child_id = ? AND status != 'Completed'
                ORDER BY due_date ASC
                LIMIT 1
            """, (child_id,))
            
            next_vaccine = cursor.fetchone()
            
            conn.close()
            
            return {
                'total_vaccinations': total,
                'completed_vaccinations': completed,
                'pending_vaccinations': total - completed,
                'next_vaccine_name': next_vaccine['vaccine_name'] if next_vaccine else 'None',
                'next_vaccine_date': next_vaccine['due_date'] if next_vaccine else 'N/A',
                'completion_percentage': round((completed / total * 100) if total > 0 else 0, 1)
            }
        except Exception as e:
            print(f"Error getting vaccination summary: {e}")
            return {
                'total_vaccinations': 0,
                'completed_vaccinations': 0,
                'pending_vaccinations': 0,
                'next_vaccine_name': 'N/A',
                'next_vaccine_date': 'N/A',
                'completion_percentage': 0
            }
    
    def get_child_nutrition_summary(self, child_id):
        """Get nutrition summary for QR code"""
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Get latest growth tracking
            cursor.execute("""
                SELECT weight_kg, height_cm, measurement_date
                FROM growth_tracking
                WHERE child_id = ?
                ORDER BY measurement_date DESC
                LIMIT 1
            """, (child_id,))
            
            growth = cursor.fetchone()
            
            # Calculate MUAC status based on weight/height ratio (simplified)
            muac_status = "Normal"
            weight = 0
            height = 0
            nutrition_score = 50
            
            if growth:
                weight = growth[0]
                height = growth[1]
                bmi = (weight / ((height/100) ** 2)) if height > 0 else 0
                if bmi < 14:
                    muac_status = "Severe Wasting"
                    nutrition_score = 30
                elif bmi < 15:
                    muac_status = "Moderate Wasting"
                    nutrition_score = 50
                elif bmi < 16:
                    muac_status = "Mild Wasting"
                    nutrition_score = 65
                else:
                    muac_status = "Normal"
                    # Calculate score based on weight (14.2kg at 4-5 years = good)
                    ideal_weight = 16.0
                    nutrition_score = min(100, int((weight / ideal_weight) * 100))
            
            conn.close()
            
            return {
                'nutrition_status': muac_status,
                'current_weight_kg': weight if growth else 'N/A',
                'current_height_cm': height if growth else 'N/A',
                'muac': muac_status,
                'nutrition_score': nutrition_score,
                'last_measured': growth[2] if growth else 'N/A'
            }
        except Exception as e:
            print(f"Error getting nutrition summary: {e}")
            return {
                'nutrition_status': 'Unknown',
                'current_weight_kg': 'N/A',
                'current_height_cm': 'N/A',
                'last_measured': 'N/A'
            }
    
    def get_emergency_contacts(self, child_id):
        """Get emergency contacts for QR code"""
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT contact_name, contact_type, phone_number, relationship, priority
                FROM emergency_contacts
                WHERE child_id = ?
                ORDER BY priority ASC
                LIMIT 5
            """, (child_id,))
            
            contacts = []
            for row in cursor.fetchall():
                contacts.append({
                    'name': row['contact_name'],
                    'type': row['contact_type'],
                    'phone': row['phone_number'],
                    'relationship': row['relationship'],
                    'priority': row['priority']
                })
            
            conn.close()
            return contacts
        except Exception as e:
            print(f"Error getting emergency contacts: {e}")
            return []
    
    def get_family_health_risks(self, child_id):
        """Get family health risks for QR code"""
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT condition_name, severity, family_member, precautions
                FROM family_health_risks
                WHERE child_id = ?
                ORDER BY severity DESC
                LIMIT 5
            """, (child_id,))
            
            risks = []
            for row in cursor.fetchall():
                risks.append({
                    'condition': row['condition_name'],
                    'severity': row['severity'],
                    'family_member': row['family_member'],
                    'precautions': row['precautions']
                })
            
            conn.close()
            return risks
        except Exception as e:
            print(f"Error getting family health risks: {e}")
            return []
    
    def get_child_data_for_qr(self, child_id):
        """Compile all child data for QR code"""
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT id, name, date_of_birth, gender, parent_name, 
                       village, address
                FROM children
                WHERE id = ?
            """, (child_id,))
            
            child = cursor.fetchone()
            conn.close()
            
            if not child:
                return None
            
            # Compile all data
            data = {
                'child_id': child['id'],
                'name': child['name'],
                'date_of_birth': child['date_of_birth'],
                'gender': child['gender'],
                'parents': {
                    'parent': child['parent_name'] if child['parent_name'] else 'N/A'
                },
                'location': {
                    'village': child['village'] if child['village'] else 'N/A',
                    'address': child['address'] if child['address'] else 'N/A'
                },
                'vaccination': self.get_child_vaccination_summary(child_id),
                'nutrition': self.get_child_nutrition_summary(child_id),
                'emergency_contacts': self.get_emergency_contacts(child_id),
                'family_health_risks': self.get_family_health_risks(child_id),
                'generated_at': datetime.now().isoformat()
            }
            
            return data
        except Exception as e:
            print(f"Error getting child data: {e}")
            return None
    
    def create_qr_code_image(self, data_dict, size=10, border=4):
        """
        Create QR code image from child data
        
        Args:
            data_dict: Dictionary with child information
            size: Box size in pixels
            border: Border thickness in boxes
        
        Returns:
            PIL Image object
        """
        # Convert data to JSON string
        json_data = json.dumps(data_dict, ensure_ascii=False)
        
        # Create QR code
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction
            box_size=size,
            border=border,
        )
        
        qr.add_data(json_data)
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        return img
    
    def create_child_identity_card(self, child_id):
        """
        Create complete child identity card with QR code
        
        Args:
            child_id: ID of the child
        
        Returns:
            Dictionary with card details and QR code image path
        """
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Check if card already exists
            cursor.execute("""
                SELECT id, qr_code_id FROM child_identity_cards WHERE child_id = ?
            """, (child_id,))
            
            existing = cursor.fetchone()
            if existing:
                # Reactivate if deactivated
                cursor.execute("""
                    UPDATE child_identity_cards SET is_active = 1, updated_at = ?
                    WHERE child_id = ?
                """, (datetime.now().isoformat(), child_id))
                conn.commit()
                conn.close()
                return {
                    'success': True,
                    'message': 'Card already exists',
                    'card_id': existing['id'],
                    'qr_code_id': existing['qr_code_id']
                }
            
            # Get child data
            child_data = self.get_child_data_for_qr(child_id)
            if not child_data:
                return {'success': False, 'message': 'Child not found'}
            
            # Generate QR code data and image
            qr_code_id = self.generate_qr_code_id(child_id)
            card_number = self.generate_card_number(child_id)
            
            # Add QR ID and card number to data
            child_data['qr_code_id'] = qr_code_id
            child_data['card_number'] = card_number
            
            # Create QR code image
            qr_image = self.create_qr_code_image(child_data)
            
            # Save QR code image
            qr_folder = "static/qr_codes"
            os.makedirs(qr_folder, exist_ok=True)
            
            image_filename = f"child_{child_id}_{qr_code_id[:8]}.png"
            image_path = os.path.join(qr_folder, image_filename)
            qr_image.save(image_path)
            
            # Store QR code data as JSON
            qr_data_json = json.dumps(child_data)
            
            # Insert into database
            cursor.execute("""
                INSERT INTO child_identity_cards 
                (child_id, qr_code_id, qr_code_data, qr_code_image_path, card_number)
                VALUES (?, ?, ?, ?, ?)
            """, (child_id, qr_code_id, qr_data_json, image_path, card_number))
            
            conn.commit()
            
            return {
                'success': True,
                'message': 'Child identity card created successfully',
                'card_id': cursor.lastrowid,
                'qr_code_id': qr_code_id,
                'card_number': card_number,
                'image_path': image_path,
                'child_data': child_data
            }
        
        except Exception as e:
            conn.rollback()
            return {'success': False, 'message': f'Error creating card: {str(e)}'}
        finally:
            conn.close()
    
    def get_identity_card(self, child_id):
        """Retrieve child identity card"""
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT * FROM child_identity_cards WHERE child_id = ? AND is_active = 1
            """, (child_id,))
            
            card = cursor.fetchone()
            conn.close()
            
            if not card:
                return None
            
            return {
                'id': card['id'],
                'child_id': card['child_id'],
                'qr_code_id': card['qr_code_id'],
                'card_number': card['card_number'],
                'image_path': card['qr_code_image_path'],
                'qr_data': json.loads(card['qr_code_data']),
                'created_at': card['created_at'],
                'updated_at': card['updated_at']
            }
        except Exception as e:
            print(f"Error retrieving card: {e}")
            return None
    
    def scan_qr_code(self, qr_code_id):
        """
        Scan QR code and retrieve child data
        Simulates ASHA/Anganwadi worker scanning with phone
        """
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT child_id, qr_code_data, card_number FROM child_identity_cards
                WHERE qr_code_id = ? AND is_active = 1
            """, (qr_code_id,))
            
            card = cursor.fetchone()
            conn.close()
            
            if not card:
                return {'success': False, 'message': 'QR code not found'}
            
            qr_data = json.loads(card['qr_code_data'])
            
            return {
                'success': True,
                'message': 'QR code scanned successfully',
                'child_data': qr_data,
                'card_number': card['card_number'],
                'scanned_at': datetime.now().isoformat()
            }
        
        except Exception as e:
            return {'success': False, 'message': f'Scan error: {str(e)}'}
    
    def add_emergency_contact(self, child_id, contact_name, phone_number, 
                             contact_type='Phone', relationship='', priority=1):
        """Add emergency contact for child"""
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO emergency_contacts
                (child_id, contact_name, contact_type, phone_number, relationship, priority)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (child_id, contact_name, contact_type, phone_number, relationship, priority))
            
            conn.commit()
            conn.close()
            
            # Update the QR card with new data
            self.create_child_identity_card(child_id)
            
            return {'success': True, 'message': 'Emergency contact added'}
        except Exception as e:
            conn.rollback()
            conn.close()
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def add_family_health_risk(self, child_id, condition_name, severity='Medium',
                              family_member='', description='', precautions=''):
        """Add family health risk for child"""
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO family_health_risks
                (child_id, condition_name, severity, family_member, description, precautions)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (child_id, condition_name, severity, family_member, description, precautions))
            
            conn.commit()
            conn.close()
            
            # Update the QR card with new data
            self.create_child_identity_card(child_id)
            
            return {'success': True, 'message': 'Family health risk added'}
        except Exception as e:
            conn.rollback()
            conn.close()
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def get_qr_code_base64(self, child_id):
        """Get QR code as base64 for embedding in HTML"""
        card = self.get_identity_card(child_id)
        
        if not card:
            return None
        
        try:
            # Read QR code image
            with open(card['image_path'], 'rb') as f:
                image_data = f.read()
            
            # Convert to base64
            base64_data = base64.b64encode(image_data).decode('utf-8')
            return f"data:image/png;base64,{base64_data}"
        except Exception as e:
            print(f"Error converting QR to base64: {e}")
            return None
    
    # ===== ASHA WORKER UPDATE FUNCTIONS =====
    
    def mark_vaccination_complete(self, child_id, vaccine_name, notes=''):
        """ASHA worker marks a vaccination as completed"""
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE immunisation_schedule 
                SET administered_date = ?, status = ?, notes = ?
                WHERE child_id = ? AND vaccine_name = ?
            """, (datetime.now().isoformat(), 'Completed', notes, child_id, vaccine_name))
            
            conn.commit()
            
            # Update QR card with new data
            self.create_child_identity_card(child_id)
            
            return {
                'success': True,
                'message': f'{vaccine_name} marked as completed',
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            conn.rollback()
            return {'success': False, 'message': f'Error: {str(e)}'}
        finally:
            conn.close()
    
    def update_nutrition_measurement(self, child_id, weight_kg, height_cm, notes=''):
        """ASHA worker updates child's weight and height"""
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO growth_tracking 
                (child_id, measurement_date, weight_kg, height_cm)
                VALUES (?, ?, ?, ?)
            """, (child_id, datetime.now().isoformat(), weight_kg, height_cm))
            
            conn.commit()
            
            # Update QR card with new data
            self.create_child_identity_card(child_id)
            
            return {
                'success': True,
                'message': f'Nutrition data updated: {weight_kg}kg, {height_cm}cm',
                'weight_kg': weight_kg,
                'height_cm': height_cm,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            conn.rollback()
            return {'success': False, 'message': f'Error: {str(e)}'}
        finally:
            conn.close()
    
    def get_pending_vaccinations(self, child_id):
        """Get list of pending vaccinations for ASHA worker to mark"""
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT vaccine_name, due_date, status
                FROM immunisation_schedule
                WHERE child_id = ? AND status = 'Pending'
                ORDER BY due_date ASC
            """, (child_id,))
            
            pending = []
            for row in cursor.fetchall():
                pending.append({
                    'vaccine_name': row['vaccine_name'],
                    'due_date': row['due_date'],
                    'status': row['status']
                })
            
            conn.close()
            return pending
        except Exception as e:
            print(f"Error getting pending vaccinations: {e}")
            return []
    
    def get_all_vaccinations(self, child_id):
        """Get all vaccinations with status for display"""
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT vaccine_name, due_date, administered_date, status, notes
                FROM immunisation_schedule
                WHERE child_id = ?
                ORDER BY due_date ASC
            """, (child_id,))
            
            vaccinations = []
            for row in cursor.fetchall():
                vaccinations.append({
                    'vaccine_name': row['vaccine_name'],
                    'due_date': row['due_date'],
                    'administered_date': row['administered_date'],
                    'status': row['status'],
                    'notes': row['notes']
                })
            
            conn.close()
            return vaccinations
        except Exception as e:
            print(f"Error getting vaccinations: {e}")
            return []
    
    def calculate_nutrition_score(self, child_id):
        """Calculate nutrition score based on growth patterns"""
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Get latest measurement
            cursor.execute("""
                SELECT weight_kg, height_cm FROM growth_tracking
                WHERE child_id = ?
                ORDER BY measurement_date DESC
                LIMIT 1
            """, (child_id,))
            
            latest = cursor.fetchone()
            if not latest:
                return 50  # Default if no data
            
            # Simple score based on nutrition status
            score = 70  # Base score
            
            # Get child's age to determine if measurements are normal
            cursor.execute("""
                SELECT date_of_birth FROM children WHERE id = ?
            """, (child_id,))
            
            child = cursor.fetchone()
            if child:
                dob = datetime.fromisoformat(child['date_of_birth'])
                age_months = (datetime.now() - dob).days / 30.44
                
                # Simple BMI-like calculation
                if age_months > 0:
                    weight = latest['weight_kg']
                    score = min(100, int(70 + (weight / age_months)))
            
            conn.close()
            return score
        except Exception as e:
            print(f"Error calculating nutrition score: {e}")
            return 50


def register_child_identity_routes(app):
    """Register child identity card routes with Flask app"""
    from flask import render_template, request, jsonify, send_file
    
    child_card = ChildIdentityCard()
    
    @app.route('/child-identity-card')
    def child_identity_dashboard():
        """Child identity card management dashboard"""
        return render_template('child_identity_card.html')
    
    @app.route('/api/child-identity/create/<int:child_id>', methods=['POST'])
    def create_child_card(child_id):
        """Create child identity card with QR code"""
        result = child_card.create_child_identity_card(child_id)
        return jsonify(result)
    
    @app.route('/api/child-identity/get/<int:child_id>', methods=['GET'])
    def get_child_card(child_id):
        """Get child identity card data"""
        card = child_card.get_identity_card(child_id)
        
        if not card:
            return jsonify({'success': False, 'message': 'Card not found'}), 404
        
        return jsonify({'success': True, 'card': card})
    
    @app.route('/api/child-identity/scan/<qr_code_id>', methods=['GET'])
    def scan_child_qr(qr_code_id):
        """Scan child QR code"""
        result = child_card.scan_qr_code(qr_code_id)
        return jsonify(result)
    
    @app.route('/api/child-identity/qr/<int:child_id>', methods=['GET'])
    def get_qr_image(child_id):
        """Get QR code image"""
        card = child_card.get_identity_card(child_id)
        
        if not card:
            return jsonify({'success': False, 'message': 'QR code not found'}), 404
        
        return send_file(card['image_path'], mimetype='image/png')
    
    @app.route('/api/child-identity/emergency-contact', methods=['POST'])
    def add_emergency_contact():
        """Add emergency contact"""
        data = request.json
        
        result = child_card.add_emergency_contact(
            child_id=data.get('child_id'),
            contact_name=data.get('contact_name'),
            phone_number=data.get('phone_number'),
            contact_type=data.get('contact_type', 'Phone'),
            relationship=data.get('relationship', ''),
            priority=data.get('priority', 1)
        )
        
        return jsonify(result)
    
    @app.route('/api/child-identity/family-health-risk', methods=['POST'])
    def add_family_risk():
        """Add family health risk"""
        data = request.json
        
        result = child_card.add_family_health_risk(
            child_id=data.get('child_id'),
            condition_name=data.get('condition_name'),
            severity=data.get('severity', 'Medium'),
            family_member=data.get('family_member', ''),
            description=data.get('description', ''),
            precautions=data.get('precautions', '')
        )
        
        return jsonify(result)
    
    @app.route('/child-identity-scanner')
    def child_scanner():
        """QR code scanner interface for ASHA/Anganwadi workers"""
        return render_template('child_scanner.html')


if __name__ == "__main__":
    print("🎫 Child Identity Card System Ready!")
    print("Features:")
    print("  ✅ Unique QR code per child")
    print("  ✅ Vaccination tracking")
    print("  ✅ Nutrition levels")
    print("  ✅ Emergency contacts")
    print("  ✅ Family health risks")
    print("  ✅ Instant scanning by ASHA workers")
