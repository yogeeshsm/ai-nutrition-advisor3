"""
🆘 Emergency Malnutrition Alert Network
Auto-alerts healthcare workers when severe malnutrition is detected

Alert Chain:
1. Anganwadi Worker (immediate)
2. PHC (Primary Health Center) 
3. NGO Volunteers
4. District Health Officer (severe cases)
"""

import json
import os
from datetime import datetime, timedelta
from enum import Enum
import hashlib

# Alert severity levels
class AlertLevel(Enum):
    WARNING = "warning"      # Moderate malnutrition - monitor closely
    CRITICAL = "critical"    # Severe malnutrition - needs intervention
    EMERGENCY = "emergency"  # Life-threatening - immediate action required

# Alert status
class AlertStatus(Enum):
    PENDING = "pending"
    ACKNOWLEDGED = "acknowledged"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    ESCALATED = "escalated"

# Responder types
class ResponderType(Enum):
    ANGANWADI_WORKER = "anganwadi_worker"
    PHC_STAFF = "phc_staff"
    NGO_VOLUNTEER = "ngo_volunteer"
    ASHA_WORKER = "asha_worker"
    DISTRICT_OFFICER = "district_officer"


class EmergencyAlertSystem:
    """Emergency Malnutrition Alert Network"""
    
    def __init__(self, db_connection=None):
        self.db = db_connection
        self.alerts_file = "emergency_alerts.json"
        self.responders_file = "alert_responders.json"
        self._load_data()
    
    def _load_data(self):
        """Load alerts and responders from files"""
        # Load alerts
        if os.path.exists(self.alerts_file):
            with open(self.alerts_file, 'r') as f:
                self.alerts = json.load(f)
        else:
            self.alerts = []
        
        # Load responders
        if os.path.exists(self.responders_file):
            with open(self.responders_file, 'r') as f:
                self.responders = json.load(f)
        else:
            self.responders = self._get_default_responders()
            self._save_responders()
    
    def _save_alerts(self):
        """Save alerts to file"""
        with open(self.alerts_file, 'w') as f:
            json.dump(self.alerts, f, indent=2, default=str)
    
    def _save_responders(self):
        """Save responders to file"""
        with open(self.responders_file, 'w') as f:
            json.dump(self.responders, f, indent=2)
    
    def _get_default_responders(self):
        """Default responders for demo"""
        return [
            {
                "id": "AWW001",
                "name": "Lakshmi Devi",
                "type": "anganwadi_worker",
                "phone": "+91-9876543210",
                "email": "lakshmi.aww@anganwadi.gov.in",
                "village": "Hosahalli",
                "priority": 1,
                "active": True
            },
            {
                "id": "ASHA001",
                "name": "Kavitha M",
                "type": "asha_worker",
                "phone": "+91-9876543211",
                "email": "kavitha.asha@health.gov.in",
                "village": "Hosahalli",
                "priority": 1,
                "active": True
            },
            {
                "id": "PHC001",
                "name": "Dr. Ramesh Kumar",
                "type": "phc_staff",
                "phone": "+91-9876543212",
                "email": "dr.ramesh@phc-mandya.gov.in",
                "village": "Mandya PHC",
                "priority": 2,
                "active": True
            },
            {
                "id": "NGO001",
                "name": "Suresh Gowda",
                "type": "ngo_volunteer",
                "phone": "+91-9876543213",
                "email": "suresh@childcare-ngo.org",
                "village": "Mandya District",
                "priority": 2,
                "active": True
            },
            {
                "id": "DHO001",
                "name": "Dr. Prasad",
                "type": "district_officer",
                "phone": "+91-9876543214",
                "email": "dho@mandya.health.gov.in",
                "village": "Mandya District HQ",
                "priority": 3,
                "active": True
            }
        ]
    
    def assess_malnutrition_severity(self, child_data):
        """
        Assess malnutrition severity based on child data
        
        Args:
            child_data: dict with weight, height, age, z_scores, etc.
        
        Returns:
            AlertLevel or None if normal
        """
        # Get z-scores (weight-for-age, height-for-age, weight-for-height)
        wfa_zscore = child_data.get('wfa_zscore', 0)
        hfa_zscore = child_data.get('hfa_zscore', 0)
        wfh_zscore = child_data.get('wfh_zscore', 0)
        
        # Also check MUAC if available (Mid-Upper Arm Circumference)
        muac = child_data.get('muac_cm', None)
        
        # Check for edema (sign of severe malnutrition)
        has_edema = child_data.get('has_edema', False)
        
        # EMERGENCY: Immediate life-threatening
        if has_edema:
            return AlertLevel.EMERGENCY
        if muac and muac < 11.5:  # MUAC < 11.5cm = SAM
            return AlertLevel.EMERGENCY
        if wfh_zscore < -3:  # Severe Acute Malnutrition
            return AlertLevel.EMERGENCY
        
        # CRITICAL: Severe malnutrition needing intervention
        if wfh_zscore < -2 or wfa_zscore < -3:
            return AlertLevel.CRITICAL
        if muac and muac < 12.5:  # MUAC 11.5-12.5 = MAM
            return AlertLevel.CRITICAL
        
        # WARNING: Moderate - needs monitoring
        if wfa_zscore < -2 or hfa_zscore < -2:
            return AlertLevel.WARNING
        
        return None  # Normal - no alert needed
    
    def create_alert(self, child_id, child_name, child_data, alert_level, village="Unknown"):
        """
        Create emergency alert for a malnourished child
        
        Returns:
            Alert ID and list of notified responders
        """
        alert_id = f"ALT-{datetime.now().strftime('%Y%m%d%H%M%S')}-{child_id}"
        
        # Build alert message
        alert = {
            "id": alert_id,
            "child_id": child_id,
            "child_name": child_name,
            "child_age_months": child_data.get('age_months', 0),
            "village": village,
            "alert_level": alert_level.value,
            "status": AlertStatus.PENDING.value,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "child_data": {
                "weight_kg": child_data.get('weight_kg'),
                "height_cm": child_data.get('height_cm'),
                "muac_cm": child_data.get('muac_cm'),
                "wfa_zscore": child_data.get('wfa_zscore'),
                "hfa_zscore": child_data.get('hfa_zscore'),
                "wfh_zscore": child_data.get('wfh_zscore'),
                "has_edema": child_data.get('has_edema', False)
            },
            "message": self._generate_alert_message(child_name, child_data, alert_level),
            "notified_responders": [],
            "acknowledgements": [],
            "interventions": [],
            "escalation_history": []
        }
        
        # Determine who to notify based on alert level
        responders_to_notify = self._get_responders_for_alert(alert_level, village)
        
        # Send notifications
        notifications = []
        for responder in responders_to_notify:
            notification = self._send_notification(responder, alert)
            notifications.append(notification)
            alert["notified_responders"].append({
                "responder_id": responder["id"],
                "responder_name": responder["name"],
                "responder_type": responder["type"],
                "notified_at": datetime.now().isoformat(),
                "method": notification["method"],
                "status": notification["status"]
            })
        
        # Save alert
        self.alerts.append(alert)
        self._save_alerts()
        
        return {
            "alert_id": alert_id,
            "alert_level": alert_level.value,
            "notifications_sent": len(notifications),
            "responders": [r["name"] for r in responders_to_notify],
            "message": alert["message"]
        }
    
    def _generate_alert_message(self, child_name, child_data, alert_level):
        """Generate human-readable alert message"""
        
        level_emoji = {
            AlertLevel.WARNING: "⚠️",
            AlertLevel.CRITICAL: "🔴",
            AlertLevel.EMERGENCY: "🆘"
        }
        
        level_text = {
            AlertLevel.WARNING: "MODERATE MALNUTRITION - Monitor Closely",
            AlertLevel.CRITICAL: "SEVERE MALNUTRITION - Intervention Needed",
            AlertLevel.EMERGENCY: "EMERGENCY - Immediate Action Required"
        }
        
        msg = f"""
{level_emoji.get(alert_level, '⚠️')} {level_text.get(alert_level, 'ALERT')}

Child: {child_name}
Age: {child_data.get('age_months', 'Unknown')} months

Measurements:
• Weight: {child_data.get('weight_kg', 'N/A')} kg
• Height: {child_data.get('height_cm', 'N/A')} cm
• MUAC: {child_data.get('muac_cm', 'N/A')} cm

Z-Scores:
• Weight-for-Age: {child_data.get('wfa_zscore', 'N/A')}
• Height-for-Age: {child_data.get('hfa_zscore', 'N/A')}
• Weight-for-Height: {child_data.get('wfh_zscore', 'N/A')}

Edema: {'YES ⚠️' if child_data.get('has_edema') else 'No'}

Action Required: Please visit child immediately and assess condition.
"""
        return msg.strip()
    
    def _get_responders_for_alert(self, alert_level, village):
        """Get appropriate responders based on alert level"""
        responders = []
        
        # Priority 1: Always alert (Anganwadi + ASHA workers)
        priority_1_types = ["anganwadi_worker", "asha_worker"]
        
        # Priority 2: For critical and emergency
        priority_2_types = ["phc_staff", "ngo_volunteer"]
        
        # Priority 3: Emergency only (District officers)
        priority_3_types = ["district_officer"]
        
        for responder in self.responders:
            if not responder.get("active", True):
                continue
            
            r_type = responder["type"]
            
            # Priority 1 - Always
            if r_type in priority_1_types:
                responders.append(responder)
            
            # Priority 2 - Critical and Emergency
            elif r_type in priority_2_types and alert_level in [AlertLevel.CRITICAL, AlertLevel.EMERGENCY]:
                responders.append(responder)
            
            # Priority 3 - Emergency only
            elif r_type in priority_3_types and alert_level == AlertLevel.EMERGENCY:
                responders.append(responder)
        
        # Sort by priority
        responders.sort(key=lambda x: x.get("priority", 99))
        
        return responders
    
    def _send_notification(self, responder, alert):
        """
        Send notification to responder
        In production, this would integrate with SMS/WhatsApp/Email APIs
        """
        notification = {
            "responder_id": responder["id"],
            "alert_id": alert["id"],
            "timestamp": datetime.now().isoformat(),
            "method": "sms",  # or email, whatsapp
            "status": "sent"  # or failed, pending
        }
        
        # Log notification (in production, send actual SMS/Email)
        print(f"📱 ALERT SENT to {responder['name']} ({responder['type']})")
        print(f"   Phone: {responder['phone']}")
        print(f"   Level: {alert['alert_level'].upper()}")
        print(f"   Child: {alert['child_name']}")
        
        # Here you would integrate with:
        # - Twilio for SMS
        # - SendGrid/SES for Email
        # - WhatsApp Business API
        
        return notification
    
    def acknowledge_alert(self, alert_id, responder_id, notes=""):
        """Responder acknowledges receiving the alert"""
        for alert in self.alerts:
            if alert["id"] == alert_id:
                alert["acknowledgements"].append({
                    "responder_id": responder_id,
                    "timestamp": datetime.now().isoformat(),
                    "notes": notes
                })
                if alert["status"] == AlertStatus.PENDING.value:
                    alert["status"] = AlertStatus.ACKNOWLEDGED.value
                alert["updated_at"] = datetime.now().isoformat()
                self._save_alerts()
                return True
        return False
    
    def update_intervention(self, alert_id, responder_id, intervention_type, notes):
        """Record intervention action taken"""
        for alert in self.alerts:
            if alert["id"] == alert_id:
                alert["interventions"].append({
                    "responder_id": responder_id,
                    "intervention_type": intervention_type,
                    "notes": notes,
                    "timestamp": datetime.now().isoformat()
                })
                alert["status"] = AlertStatus.IN_PROGRESS.value
                alert["updated_at"] = datetime.now().isoformat()
                self._save_alerts()
                return True
        return False
    
    def resolve_alert(self, alert_id, responder_id, outcome, notes=""):
        """Mark alert as resolved"""
        for alert in self.alerts:
            if alert["id"] == alert_id:
                alert["status"] = AlertStatus.RESOLVED.value
                alert["resolution"] = {
                    "responder_id": responder_id,
                    "outcome": outcome,
                    "notes": notes,
                    "resolved_at": datetime.now().isoformat()
                }
                alert["updated_at"] = datetime.now().isoformat()
                self._save_alerts()
                return True
        return False
    
    def escalate_alert(self, alert_id, reason):
        """Escalate unresolved alert to higher authority"""
        for alert in self.alerts:
            if alert["id"] == alert_id:
                alert["status"] = AlertStatus.ESCALATED.value
                alert["escalation_history"].append({
                    "reason": reason,
                    "timestamp": datetime.now().isoformat()
                })
                
                # Notify district officer
                district_officers = [r for r in self.responders if r["type"] == "district_officer"]
                for officer in district_officers:
                    self._send_notification(officer, alert)
                    alert["notified_responders"].append({
                        "responder_id": officer["id"],
                        "responder_name": officer["name"],
                        "responder_type": officer["type"],
                        "notified_at": datetime.now().isoformat(),
                        "method": "escalation",
                        "status": "sent"
                    })
                
                alert["updated_at"] = datetime.now().isoformat()
                self._save_alerts()
                return True
        return False
    
    def get_alert(self, alert_id):
        """Get single alert by ID"""
        for alert in self.alerts:
            if alert["id"] == alert_id:
                return alert
        return None
    
    def get_all_alerts(self, status=None, level=None, limit=50):
        """Get all alerts with optional filtering"""
        filtered = self.alerts.copy()
        
        if status:
            filtered = [a for a in filtered if a["status"] == status]
        
        if level:
            filtered = [a for a in filtered if a["alert_level"] == level]
        
        # Sort by created_at descending
        filtered.sort(key=lambda x: x["created_at"], reverse=True)
        
        return filtered[:limit]
    
    def get_pending_alerts(self):
        """Get alerts that need attention"""
        return [a for a in self.alerts if a["status"] in [
            AlertStatus.PENDING.value, 
            AlertStatus.ACKNOWLEDGED.value,
            AlertStatus.ESCALATED.value
        ]]
    
    def get_village_stats(self, village=None):
        """Get alert statistics for a village"""
        alerts = self.alerts if not village else [a for a in self.alerts if a["village"] == village]
        
        return {
            "total_alerts": len(alerts),
            "pending": len([a for a in alerts if a["status"] == AlertStatus.PENDING.value]),
            "in_progress": len([a for a in alerts if a["status"] == AlertStatus.IN_PROGRESS.value]),
            "resolved": len([a for a in alerts if a["status"] == AlertStatus.RESOLVED.value]),
            "emergency_count": len([a for a in alerts if a["alert_level"] == AlertLevel.EMERGENCY.value]),
            "critical_count": len([a for a in alerts if a["alert_level"] == AlertLevel.CRITICAL.value]),
            "warning_count": len([a for a in alerts if a["alert_level"] == AlertLevel.WARNING.value])
        }
    
    # Responder management
    def add_responder(self, responder_data):
        """Add a new responder"""
        responder_id = f"{responder_data['type'][:3].upper()}{len(self.responders)+1:03d}"
        responder_data["id"] = responder_id
        responder_data["active"] = True
        self.responders.append(responder_data)
        self._save_responders()
        return responder_id
    
    def update_responder(self, responder_id, updates):
        """Update responder details"""
        for responder in self.responders:
            if responder["id"] == responder_id:
                responder.update(updates)
                self._save_responders()
                return True
        return False
    
    def get_responders(self, responder_type=None):
        """Get all responders"""
        if responder_type:
            return [r for r in self.responders if r["type"] == responder_type]
        return self.responders
    
    def auto_escalate_old_alerts(self, hours=24):
        """Auto-escalate alerts not acknowledged within specified hours"""
        cutoff = datetime.now() - timedelta(hours=hours)
        escalated = []
        
        for alert in self.alerts:
            if alert["status"] == AlertStatus.PENDING.value:
                created = datetime.fromisoformat(alert["created_at"])
                if created < cutoff:
                    self.escalate_alert(
                        alert["id"], 
                        f"Auto-escalated: No acknowledgement after {hours} hours"
                    )
                    escalated.append(alert["id"])
        
        return escalated


# Singleton instance
_alert_system = None

def get_alert_system():
    """Get singleton instance of alert system"""
    global _alert_system
    if _alert_system is None:
        _alert_system = EmergencyAlertSystem()
    return _alert_system


# Quick test
if __name__ == "__main__":
    system = EmergencyAlertSystem()
    
    # Test alert creation
    test_child = {
        "age_months": 18,
        "weight_kg": 6.5,
        "height_cm": 72,
        "muac_cm": 11.0,  # Severe
        "wfa_zscore": -3.5,
        "hfa_zscore": -2.1,
        "wfh_zscore": -3.2,
        "has_edema": False
    }
    
    level = system.assess_malnutrition_severity(test_child)
    print(f"\nAssessed Level: {level}")
    
    if level:
        result = system.create_alert(
            child_id=1,
            child_name="Baby Raju",
            child_data=test_child,
            alert_level=level,
            village="Hosahalli"
        )
        print(f"\n✅ Alert Created: {result['alert_id']}")
        print(f"   Level: {result['alert_level']}")
        print(f"   Notified: {', '.join(result['responders'])}")
