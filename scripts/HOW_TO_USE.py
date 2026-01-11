"""
🎫 MOBILE CHILD ID CARD - USER GUIDE
====================================

📱 HOW TO USE THIS FEATURE

STEP 1: START THE SERVER
-------------------------
1. Open terminal/command prompt
2. Navigate to project folder
3. Run: python flask_app.py
4. Server starts at: http://127.0.0.1:5000


STEP 2: CREATE CHILD ID CARD (For Parents/Admin)
-------------------------------------------------
1. Open browser: http://127.0.0.1:5000/child-identity-card

2. You'll see a dropdown with all children:
   - Lakshmi (5y)
   - Aarav Singh (2y)
   - Anaya Patel (2y)
   - etc.

3. Select "Lakshmi (5y)" from dropdown

4. Click "Generate QR Card" button

5. The system creates:
   ✅ Unique QR code (CHILD_982374)
   ✅ Digital ID card with all child data
   ✅ QR image you can save/print

6. Save or screenshot the QR code
   - Parents can save it on their phone
   - Can print physical copy
   - Can share via WhatsApp


STEP 3: SCAN QR CODE (For ASHA Workers)
----------------------------------------
1. ASHA worker opens: http://127.0.0.1:5000/child-identity-scanner

2. Three ways to scan:
   
   Option A - Camera Scan (Recommended):
   • Click "Start Camera" button
   • Point camera at parent's QR code
   • Auto-detects and loads child data
   
   Option B - Manual Entry:
   • Type QR ID in search box (e.g., CHILD_982374)
   • Click "Search by QR ID"
   
   Option C - Upload Image:
   • Click "Upload QR Image"
   • Select QR code image from phone
   • System reads and loads data

3. Child's complete profile appears:
   📋 Name: Lakshmi
   🎂 Age: 5 years
   🆔 ID: CHILD_982374
   
   💉 Vaccinations:
   ✔ BCG (Completed)
   ✔ OPV 1, 2, 3 (Completed)
   ✔ DPT 1, 2, 3 (Completed)
   ❗ MR (Pending) ← Shows "Mark Done" button
   ❗ JE (Pending)
   ❗ Booster DPT (Pending)
   
   📏 Nutrition:
   Weight: 14.2 kg
   Height: 97 cm
   MUAC: Normal
   Score: 88/100
   
   ⚠️ Family Health Risks:
   • Mother has anemia (High)
   • Father has hypertension (Medium)
   
   📞 Emergency Contacts:
   • Ravi (Father): 9876543210
   • Sunita (Mother): 9876543211
   • Aunt: 9829345234


STEP 4: ASHA UPDATES (Mark Vaccination)
----------------------------------------
1. ASHA sees "MR (Measles-Rubella)" has ❗ Pending

2. After giving MR vaccine, clicks "Mark Done" button

3. System:
   ✅ Updates database (status: Completed)
   ✅ Regenerates QR code with new data
   ✅ Shows success message
   ✅ Page refreshes with updated status

4. Now MR shows: ✔ MR (Completed)

5. Progress updates:
   Before: 7/10 vaccinations (70%)
   After: 8/10 vaccinations (80%)


STEP 5: ASHA UPDATES (Nutrition)
---------------------------------
1. ASHA measures child's weight and height

2. Enters in "ASHA Update Nutrition" section:
   • New Weight: 14.5 kg
   • New Height: 98 cm

3. Clicks "Save Nutrition Update"

4. System:
   ✅ Saves new growth measurement
   ✅ Recalculates nutrition score
   ✅ Updates QR code
   ✅ Shows success message

5. Updated data appears:
   Weight: 14.5 kg (was 14.2 kg)
   Height: 98 cm (was 97 cm)
   Score: 90/100 (was 88/100)


STEP 6: PARENT SEES UPDATED CARD
---------------------------------
1. Parent goes back to: http://127.0.0.1:5000/child-identity-card

2. Selects "Lakshmi" again

3. Clicks "Generate QR Card" (or "View Existing Card")

4. Updated card shows:
   ✔ MR vaccine now marked as completed
   ✔ New weight: 14.5 kg
   ✔ New height: 98 cm
   ✔ Updated nutrition score: 90/100

5. Parent can:
   • Save new QR code
   • Print updated card
   • Share with family


🎯 REAL-WORLD USAGE SCENARIOS
==============================

Scenario 1: Anganwadi Center Visit
-----------------------------------
• Mother brings Lakshmi to Anganwadi
• Shows QR code from phone
• Worker scans → Instant access to:
  - Vaccination history
  - Due vaccines
  - Growth chart
  - Health alerts
• Worker gives pending vaccine
• Marks as done in system
• Mother's card auto-updates


Scenario 2: Home Visit by ASHA Worker
--------------------------------------
• ASHA visits Lakshmi's home
• Scans QR from mother's phone
• Checks:
  ✅ Vaccination status (7/10 done)
  ✅ Nutrition score (88/100 - good)
  ⚠️ Mother has anemia (high risk)
• Advises mother about iron supplements
• Measures child (14.5 kg, 98 cm)
• Updates in system immediately


Scenario 3: Emergency Hospital Visit
-------------------------------------
• Lakshmi has fever
• Father takes to hospital
• Shows QR code to doctor
• Doctor scans → Sees:
  - Complete vaccination record
  - Current health status
  - Family health risks (important!)
  - Emergency contacts
• Doctor makes informed decision quickly


Scenario 4: School Admission
-----------------------------
• School needs health records
• Mother shows QR code
• School admin scans → Downloads:
  - Vaccination certificate
  - Growth chart
  - Health clearance
• No need for physical documents


🔧 TROUBLESHOOTING
==================

Problem: Can't start server
Solution: 
  cd "c:\Users\S M Yogesh\OneDrive\ドキュメント\ai nutrition advisor3w"
  python flask_app.py

Problem: Dropdown shows no children
Solution: 
  python add_test_children.py
  (Creates test data)

Problem: QR scanner not working
Solution:
  • Allow camera permissions in browser
  • Try manual QR ID entry instead
  • Use "Upload QR Image" option

Problem: Updates not saving
Solution:
  • Check internet connection
  • Refresh browser page
  • Check server logs for errors


📞 QUICK ACCESS LINKS
=====================
Parent/Admin Dashboard: http://127.0.0.1:5000/child-identity-card
ASHA Scanner: http://127.0.0.1:5000/child-identity-scanner
Main Home: http://127.0.0.1:5000


✨ KEY BENEFITS
===============
✅ Instant access to child health records
✅ No paperwork needed
✅ Offline-capable (QR contains all data)
✅ Real-time updates
✅ Emergency contact information
✅ Family health risk tracking
✅ Progress monitoring (vaccination %, nutrition score)
✅ Works on any smartphone
✅ Multi-user access (parent, ASHA, doctor)
✅ Audit trail of all updates
"""

print(__doc__)
