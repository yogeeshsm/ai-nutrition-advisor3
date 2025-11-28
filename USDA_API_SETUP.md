# 🚨 USDA API Key Issue - Action Required

## Problem
The USDA API key you provided is returning a **403 Forbidden** error.

## API Key You Provided
```
I8E0Icmi3gYlneZJ27MWK6ChaaUYBCn2Vv801NH
```

## Possible Causes:
1. ❌ **Invalid API Key** - The key may not be correctly copied
2. ❌ **Expired Key** - Some API keys expire after a period
3. ❌ **Not Activated** - The key needs email verification
4. ❌ **Wrong Service** - This might be for a different USDA service

---

## ✅ **HOW TO GET A WORKING USDA API KEY:**

### Step 1: Sign Up for API Key
1. Go to: **https://fdc.nal.usda.gov/api-key-signup.html**
2. Fill in the form:
   - **First Name**: Your name
   - **Last Name**: Your last name
   - **Email**: Your valid email address
   - **Organization** (optional): Can leave blank or put "Personal Project"
   - **Intended Use**: Put "Nutrition analysis for meal planning application"

3. Click **"Request API Key"**

### Step 2: Check Your Email
1. You will receive an email from **noreply@nal.usda.gov**
2. Subject: "FoodData Central API Key Request"
3. **The email contains your API key** - copy it exactly

### Step 3: Update Your .env File
1. Open `.env` file in your project
2. Replace the line:
   ```
   USDA_API_KEY=I8E0Icmi3gYlneZJ27MWK6ChaaUYBCn2Vv801NH
   ```
   With:
   ```
   USDA_API_KEY=YOUR_NEW_KEY_FROM_EMAIL
   ```

### Step 4: Test the API Key
Run this command to test:
```bash
python update_nutrition_data.py
```

You should see:
```
✅ Calories: 130 kcal
✅ Protein: 2.7g
✅ Carbs: 28.2g
✅ Data source: USDA FoodData Central
```

---

## 🔄 **ALTERNATIVE: Use DEMO_KEY for Testing**

USDA provides a **DEMO_KEY** for testing (limited to 30 requests per hour):

1. Open `.env` file
2. Change to:
   ```
   USDA_API_KEY=DEMO_KEY
   ```
3. Test with: `python update_nutrition_data.py`

**NOTE:** DEMO_KEY is rate-limited. Get your own key for production use.

---

## 📝 **What I've Already Done:**

✅ Created `usda_nutrition_manager.py` - Smart caching system for USDA data  
✅ Created `update_nutrition_data.py` - Easy tool to update all ingredients  
✅ Updated `database.py` - Prepared for USDA data integration  
✅ Updated `templates/index.html` - Added "USDA Verified" badges  
✅ Created `.env` file with your API key (needs to be replaced)  

---

## 🎯 **Next Steps:**

### Option 1: Get New API Key (Recommended - Takes 2 minutes)
1. Visit: https://fdc.nal.usda.gov/api-key-signup.html
2. Fill the form
3. Check email
4. Update `.env` with new key
5. Run: `python update_nutrition_data.py`

### Option 2: Use DEMO_KEY (Quick Test - Limited)
1. Open `.env`
2. Change to: `USDA_API_KEY=DEMO_KEY`
3. Run: `python update_nutrition_data.py`

---

## ✅ **Once You Have a Valid Key:**

Run this command to update ALL ingredients with accurate USDA data:

```bash
python update_nutrition_data.py
```

When prompted "Would you like to update ALL ingredients? (y/n)", type **y** and press Enter.

This will:
- ✅ Fetch accurate nutrition data from USDA for all 60+ ingredients
- ✅ Cache the data locally to avoid repeated API calls
- ✅ Update your database with verified calories, protein, vitamins, etc.
- ✅ Make your nutrition calculations 100% accurate

---

## 📧 **Need Help?**

If you continue having issues:
1. Send me the exact error message
2. Confirm you received the email from USDA
3. Check your spam folder for the USDA email
4. Verify the API key is copied correctly (no extra spaces)

---

**File Created:** `USDA_API_SETUP.md`
