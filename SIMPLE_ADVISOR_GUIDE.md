# 💚 Simple Nutrition Advisor for Rural Parents

## Overview

A simplified, parent-friendly nutrition assessment tool designed for children aged 0-6 years in rural areas with limited resources and low literacy.

## Access

**URL:** http://localhost:5000/simple-advisor

**Navigation:** AI Tools → Simple Guide (Parents)

## Features

### ✅ What It Does

1. **Identifies Nutrition Gaps** - Analyzes what foods the child has NOT eaten recently
2. **Assesses Risk Level** - Categorizes as Low, Medium, or High (without medical jargon)
3. **Suggests ONE Simple Food** - Provides a single, locally available, low-cost solution
4. **Specifies Frequency** - Clear guidance on how often to give the food
5. **Parent-Friendly Message** - Simple language suitable for low-literacy parents

### 🎯 Target Users

- Parents of children 0-6 years old
- Rural families with limited income
- Areas with limited food availability
- Low-literacy communities

## How to Use

### For Parents:

1. **Select child's age** in months (0-72 months)
2. **Check foods eaten** in the last 2-3 days from the list:
   - Rice, Roti, Dal, Milk, Curd, Egg
   - Spinach, Carrot, Potato, Ragi
   - Banana, Jaggery, and more
3. **Add other foods** if not in the list
4. **Click "Get Advice"**
5. **Receive:**
   - Risk Level (Low/Medium/High)
   - Main nutrition gap
   - ONE food to add
   - How often to give it
   - Simple explanation

## Food Groups Monitored

1. **Protein** (for strong muscles and growth)
   - Egg, Dal, Milk, Curd, Peanuts, Soya, Chicken, Fish

2. **Iron** (for good blood)
   - Egg, Spinach, Methi, Jaggery, Ragi, Bajra, Dates

3. **Calcium** (for strong bones)
   - Milk, Curd, Ragi, Spinach, Methi

4. **Vitamin A** (for good eyesight)
   - Carrot, Papaya, Mango, Pumpkin, Spinach, Egg

5. **Energy** (for active play)
   - Rice, Roti, Wheat, Jowar, Bajra, Potato

## Example Outputs

### Example 1: Limited Diet
**Input:** Child (18 months) eating only rice and dal

**Output:**
```
Risk Level: Medium
Main Nutrition Gap: Calcium for strong bones
One Food Fix: Milk or curd
Frequency: Daily (1 cup)
Parent Message: Your child needs Milk or curd Daily (1 cup). 
This makes bones and teeth strong. Very important for growing children.
```

### Example 2: Good Variety
**Input:** Child (24 months) eating rice, dal, egg, milk, carrot, spinach

**Output:**
```
Risk Level: Low
Main Nutrition Gap: None - eating variety of foods
One Food Fix: Continue current diet
Frequency: Daily
Parent Message: Good! Your child is eating different types of food. 
Keep giving variety.
```

### Example 3: High Risk
**Input:** Baby (8 months) eating only rice

**Output:**
```
Risk Level: High
Main Nutrition Gap: Protein for strong muscles and growth
One Food Fix: Egg (boiled)
Frequency: 3-4 times per week
Parent Message: Your baby needs Egg (boiled) 3-4 times per week. 
This helps them grow strong. Cook soft and mash well for easy eating.
```

## API Endpoint

### POST `/api/simple-nutrition-advice`

**Request Body:**
```json
{
  "foods_eaten": ["rice", "dal", "milk"],
  "child_age_months": 18
}
```

**Response:**
```json
{
  "risk_level": "Low",
  "main_gap": "Iron for good blood",
  "food_solution": "Ragi porridge",
  "frequency": "4-5 times per week",
  "parent_message": "Give Ragi porridge 4-5 times per week..."
}
```

## Design Principles

### ✅ DO:
- Use simple, local food names
- Suggest seasonal, traditional foods
- Give clear frequency (e.g., "3-4 times per week")
- Use parent-friendly language
- Focus on ONE recommendation

### ❌ DON'T:
- Give medical advice or diagnose diseases
- Suggest expensive or packaged foods
- Use technical nutrition terms
- Mention calorie counts
- Give multiple recommendations at once
- Suggest supplements

## Age-Specific Logic

### 0-6 Months
- **Priority:** Calcium (breastmilk/formula)
- **Risk:** Higher sensitivity to missing food groups

### 6-24 Months
- **Priority:** Protein and Iron (critical growth period)
- **Risk:** Moderate to high for multiple gaps

### 24-72 Months
- **Priority:** Balanced across all food groups
- **Risk:** Lower threshold for concern

## Risk Assessment

| Missing Groups | Age 0-24 months | Age 24-72 months |
|----------------|----------------|------------------|
| 1 group | Low | Low |
| 2 groups | Medium | Medium |
| 3+ groups | High | Medium |
| 4+ groups | High | High |

## Local Food Solutions

| Nutrient Gap | Primary Solution | Backup Solution |
|-------------|------------------|-----------------|
| Protein | Egg (boiled) | Dal (any type) |
| Iron | Ragi porridge | Jaggery with roti |
| Calcium | Milk or curd | Ragi with milk |
| Vitamin A | Carrot (cooked) | Pumpkin (seasonal) |
| Energy | Roti with ghee | Rice with dal |

## Integration with Other Features

This tool complements:
- **Growth Tracking** - Monitor if nutrition advice improves growth
- **Meal Planner** - Use suggested foods in meal plans
- **AI Chatbot** - Get detailed cooking instructions
- **Village Economy** - Find local prices for suggested foods

## Benefits

1. **Simple** - Easy to understand for low-literacy parents
2. **Practical** - Suggests locally available, affordable foods
3. **Actionable** - One clear recommendation to follow
4. **Cultural** - Respects traditional rural food preferences
5. **Effective** - Evidence-based nutrition priorities

## Technical Details

**Backend:** `simple_nutrition_advisor.py`
**Frontend:** `templates/simple_advisor.html`
**Routes:** 
- `/simple-advisor` (page)
- `/api/simple-nutrition-advice` (API)

**Dependencies:** None (pure Python logic)

---

**Created:** December 23, 2025
**Purpose:** Empower rural parents with simple, actionable nutrition guidance
**Status:** ✅ Active and Ready to Use
