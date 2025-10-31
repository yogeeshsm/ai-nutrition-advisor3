# 📸 Visual Guide - AI Nutrition Advisor

## Application Screenshots & Walkthrough

---

## 🏠 Home Screen

### Header Section
```
┌─────────────────────────────────────────────────────────┐
│         🍽️ AI Nutrition Advisor                        │
│   Generate Balanced Weekly Meal Plans for              │
│          Anganwadi Children                             │
└─────────────────────────────────────────────────────────┘
```

### Sidebar Navigation
```
┌──────────────────┐
│  ⚙️ Settings     │
├──────────────────┤
│ 🌐 Language      │
│  [English ▼]     │
├──────────────────┤
│ 📍 Navigate      │
│  ○ 🏠 Meal       │
│     Planner      │
│  ○ 📊 Analytics  │
│     Dashboard    │
│  ○ ℹ️ About      │
└──────────────────┘
```

---

## 📝 Input Section

### Step 1: Basic Information
```
┌────────────────────────────────────────────────────────┐
│ 📝 Input Details                                       │
├────────────────────────────────────────────────────────┤
│                                                        │
│ 👶 Number of Children    💰 Weekly Budget (₹)        │
│ [   20    ]              [   2000.00   ]             │
│                                                        │
│ 👧 Age Group              Per Child/Week: ₹100.00    │
│ [3-6 years ▼]            Per Child/Day: ₹14.29      │
│                          Per Meal: ₹4.76             │
└────────────────────────────────────────────────────────┘
```

### Step 2: Ingredient Selection
```
┌────────────────────────────────────────────────────────┐
│ 🥗 Select Available Ingredients                        │
├────────────────────────────────────────────────────────┤
│ [✅ Select All] [❌ Clear All]                         │
│ [🌾 Basic Only] [⭐ Recommended]                      │
└────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────┐
│ Tabs: [🌾 Grains] [🫘 Pulses] [🥬 Vegetables] ...   │
├──────────────────────────────────────────────────────┤
│                                                      │
│ 🌾 Grains Tab:                                       │
│                                                      │
│ ☑️ 🌾 Rice                    ₹45/kg    🔥 360 kcal │
│ ☑️ 🌾 Wheat Flour (Atta)     ₹35/kg    🔥 340 kcal │
│ ☑️ 🌾 Jowar (Sorghum)        ₹50/kg    🔥 329 kcal │
│ ☐ 🌾 Ragi (Finger Millet)   ₹60/kg    🔥 328 kcal │
│ ☐ 🌾 Poha (Flattened Rice)  ₹55/kg    🔥 350 kcal │
│                                                      │
└──────────────────────────────────────────────────────┘

✅ Selected 12 ingredients
```

### Step 3: Generate
```
┌────────────────────────────────────────────────────────┐
│                                                        │
│              [🚀 Generate Meal Plan]                  │
│                                                        │
└────────────────────────────────────────────────────────┘
```

---

## 📋 Results Screen

### Summary Metrics
```
┌───────────────────────────────────────────────────────┐
│ 📋 Your Weekly Meal Plan                              │
├───────────────────────────────────────────────────────┤
│                                                       │
│ ┌──────────┬──────────┬──────────┬──────────┐       │
│ │💰 Total  │⭐ Score  │🔥 Avg    │💪 Avg    │       │
│ │  Cost    │          │ Calories │ Protein  │       │
│ ├──────────┼──────────┼──────────┼──────────┤       │
│ │₹1,847.50 │  92/100  │  1,340   │ 20.5g    │       │
│ │          │          │          │          │       │
│ │-7.6% of  │Excellent │Per child │Per child │       │
│ │budget    │          │          │          │       │
│ └──────────┴──────────┴──────────┴──────────┘       │
└───────────────────────────────────────────────────────┘
```

### Meal Plan Table
```
┌─────────────────────────────────────────────────────────────────┐
│ 🗓️ 7-Day Meal Schedule                                         │
├──────┬───────┬────────────┬──────────┬──────────┬──────────────┤
│ Day  │ Meal  │ Ingredient │ Category │ Qty/Child│ Cost (₹)    │
├──────┼───────┼────────────┼──────────┼──────────┼──────────────┤
│Monday│Breakfast│🌾 Poha   │ Grains   │  40.0g   │  4.40       │
│      │       │🥛 Milk     │ Dairy    │ 150.0g   │ 16.50       │
│      │       │🍯 Jaggery  │ Sweetener│  10.0g   │  1.20       │
│      ├───────┼────────────┼──────────┼──────────┼──────────────┤
│      │Lunch  │🌾 Rice     │ Grains   │  80.0g   │  7.20       │
│      │       │🫘 Dal      │ Pulses   │  40.0g   │  9.60       │
│      │       │🥬 Spinach  │ Vegetables│ 50.0g   │  4.50       │
│      │       │🧈 Oil      │ Fats     │   5.0g   │  1.50       │
│      ├───────┼────────────┼──────────┼──────────┼──────────────┤
│      │Snack  │🍎 Fruits   │ Fruits   │ 100.0g   │ 10.00       │
│      ├───────┼────────────┼──────────┼──────────┼──────────────┤
│      │Dinner │🌾 Roti     │ Grains   │  70.0g   │  4.90       │
│      │       │🥬 Veg Curry│ Vegetables│ 80.0g   │  6.40       │
│      │       │🫘 Dal      │ Pulses   │  30.0g   │  7.20       │
└──────┴───────┴────────────┴──────────┴──────────┴──────────────┘
         ... continues for all 7 days ...
```

### Day-wise Tabs
```
┌─────────────────────────────────────────────────────────┐
│ 📅 Day-wise Breakdown                                   │
├─────────────────────────────────────────────────────────┤
│ Tabs: [Monday] [Tuesday] [Wednesday] ... [Sunday]      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ Monday Selected:                                        │
│                                                         │
│ ### Breakfast 🍽️                                       │
│ Poha (40g), Milk (150g), Jaggery (10g)                │
│ ⚡ 285 kcal | 💪 6.2g protein | 💰 ₹22.10             │
│ ───────────────────────────────────────                │
│                                                         │
│ ### Lunch 🍽️                                           │
│ Rice (80g), Dal (40g), Spinach (50g), Oil (5g)        │
│ ⚡ 480 kcal | 💪 13.5g protein | 💰 ₹22.80            │
│ ───────────────────────────────────────                │
│                                                         │
│ [Similar for Snack and Dinner]                         │
│                                                         │
│ Daily Summary:                                          │
│ Total Cost: ₹264.00                                    │
│ Calories: 1,340                                        │
│ Protein: 20.5g                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 📊 Nutrition Analysis

### Macronutrient Distribution
```
┌────────────────────────────────┐
│ Macronutrient Distribution     │
│      (Calories)                │
│                                │
│         ╭─────╮                │
│     ╭───┤     ├───╮            │
│    │    │     │    │           │
│    │ 🟥 │ 🟦 │ 🟨 │          │
│    │Pro │Carb│Fat │           │
│    │20% │65% │15% │           │
│     ╰───┴─────┴───╯            │
│                                │
└────────────────────────────────┘
```

### Requirements vs Achieved
```
┌──────────────────────────────────────┐
│ Weekly Nutritional Requirements      │
│        vs Achieved                   │
│                                      │
│ Calories  ████████████ 98%          │
│           ████████████              │
│                                      │
│ Protein   ███████████░ 95%          │
│           ███████████               │
│                                      │
│ Carbs     █████████████ 102%        │
│           █████████████             │
│                                      │
│ Fat       ███████████░ 92%          │
│           ███████████               │
│                                      │
│ [Similar bars for Fiber, Iron, etc.]│
└──────────────────────────────────────┘
```

### Target Achievement
```
┌────────────────────────────────────────────────┐
│ 🎯 Target Achievement                          │
├────────┬────────┬────────┬────────┬───────────┤
│Calories│Protein │ Carbs  │  Fat   │  Fiber    │
│        │        │        │        │           │
│  98%   │  95%   │ 102%   │  92%   │  88%     │
│  -2%   │  -5%   │  +2%   │  -8%   │  -12%    │
│ normal │ normal │ normal │ normal │    off    │
└────────┴────────┴────────┴────────┴───────────┘
```

---

## 📥 Export Options

```
┌─────────────────────────────────────────────────┐
│ 📥 Export Meal Plan                             │
├─────────────────────────────────────────────────┤
│                                                 │
│  [📄 Download CSV]  [📋 Download JSON]         │
│                                                 │
│         [📑 Generate PDF]                       │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## 📊 Analytics Dashboard

### Summary Cards
```
┌──────────────────────────────────────────────────────┐
│ 📊 Analytics Dashboard                               │
├──────────────────────────────────────────────────────┤
│                                                      │
│ ┌───────────┬───────────┬───────────┬──────────┐   │
│ │📋 Total   │⭐ Avg     │💰 Avg     │👶 Avg    │   │
│ │  Plans    │ Nutrition │  Cost     │ Children │   │
│ │           │  Score    │           │          │   │
│ ├───────────┼───────────┼───────────┼──────────┤   │
│ │    45     │   87.3    │₹2,145.50 │   22     │   │
│ └───────────┴───────────┴───────────┴──────────┘   │
└──────────────────────────────────────────────────────┘
```

### Charts
```
┌─────────────────────────────────────┐
│ Budget vs Nutrition Score           │
│                                     │
│ 100│         ●  ●                   │
│    │      ●                         │
│  90│   ●        ●                   │
│    │●                               │
│  80│                                │
│    └────────────────────           │
│    1000  2000  3000  4000          │
│         Budget (₹)                 │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ Most Popular Age Group Plans        │
│                                     │
│ 3-6 years   ████████████ 25        │
│ 6-10 years  ████████ 15            │
│ 1-3 years   ████ 5                 │
│                                     │
└─────────────────────────────────────┘
```

### Recent Plans Table
```
┌────────────────────────────────────────────────────────┐
│ 📋 Recent Meal Plans                                   │
├──────────┬────────┬──────┬──────────┬──────┬─────────┤
│Plan Name │Budget  │Kids  │Age Group │Score │Created  │
├──────────┼────────┼──────┼──────────┼──────┼─────────┤
│Plan_...  │2000.00 │  20  │3-6 years │ 92.0 │Oct 31   │
│Plan_...  │2500.00 │  25  │3-6 years │ 88.5 │Oct 30   │
│Plan_...  │1500.00 │  15  │1-3 years │ 84.2 │Oct 29   │
└──────────┴────────┴──────┴──────────┴──────┴─────────┘
```

---

## ℹ️ About Page

```
┌─────────────────────────────────────────────────────┐
│ ℹ️ About AI Nutrition Advisor                      │
├─────────────────────────────────────────────────────┤
│                                                     │
│ ### 🎯 Purpose                                      │
│                                                     │
│ The AI Nutrition Advisor is designed to help       │
│ Anganwadi workers generate balanced, cost-         │
│ effective weekly meal plans...                     │
│                                                     │
│ ### ✨ Key Features                                 │
│                                                     │
│ - 🤖 AI-Powered Optimization                       │
│ - 🍽️ 7-Day Meal Plans                             │
│ - 📊 Nutrition Analysis                            │
│ - 💰 Budget Management                             │
│ - 📥 Export Options                                │
│ ...                                                 │
│                                                     │
│ [More sections...]                                  │
│                                                     │
│ 💚 Made with love for India's children             │
└─────────────────────────────────────────────────────┘
```

---

## 🎨 Color Scheme

### Status Colors
- 🟢 Green (Excellent): 90-110% of target
- 🟡 Yellow (Good): 80-120% of target
- 🟠 Orange (Fair): 70-130% of target
- 🔴 Red (Poor): <70% or >130%

### Category Colors
- 🔴 Red (#FF6B6B): Protein, primary actions
- 🔵 Blue (#4ECDC4): Carbs, secondary actions
- 🟡 Yellow (#FFE66D): Fat, highlights

---

## 💡 Interactive Elements

### Buttons
```
┌──────────────────────┐
│  🚀 Generate Plan    │  ← Primary action (red)
└──────────────────────┘

┌──────────────────────┐
│  📄 Download CSV     │  ← Secondary action (blue)
└──────────────────────┘
```

### Inputs
```
Number Input:  [  20  ▲▼]
Dropdown:      [3-6 years ▼]
Multiselect:   ☑️ Rice
               ☐ Wheat
```

### Metrics
```
┌──────────────┐
│ ⭐ Score     │
│              │
│    92/100    │
│              │
│  Excellent   │
└──────────────┘
```

---

## 📱 Responsive Layout

### Desktop View
```
┌──────────┬─────────────────────────────────┐
│          │                                 │
│ Sidebar  │      Main Content Area          │
│          │                                 │
│ Settings │   [Input Section]               │
│          │                                 │
│ Navigate │   [Ingredient Selection]        │
│          │                                 │
│          │   [Results Display]             │
│          │                                 │
└──────────┴─────────────────────────────────┘
```

### Mobile View (Collapsed Sidebar)
```
┌─────────────────────────┐
│ ☰                       │  ← Menu icon
├─────────────────────────┤
│                         │
│   Main Content          │
│   (Full Width)          │
│                         │
└─────────────────────────┘
```

---

## ⌨️ Keyboard Shortcuts (Browser)

- `Ctrl + R` - Refresh page
- `Ctrl + F` - Find text
- `F11` - Fullscreen
- `Ctrl + +/-` - Zoom in/out
- `F12` - Developer tools

---

## 🎬 User Flow Animation

```
Start
  ↓
Select Language (Optional)
  ↓
Enter Number of Children → Budget → Age Group
  ↓
Select Ingredients (Category Tabs)
  ↓
Click "Generate Meal Plan"
  ↓
⏳ Optimization (5-15 sec)
  ↓
✅ View Results
  ↓
Review Nutrition Charts
  ↓
Check Day-wise Plans
  ↓
Export (CSV/PDF/JSON)
  ↓
End
```

---

## 🔄 Loading States

### During Optimization
```
┌────────────────────────────┐
│  🔄 Optimizing meal plan   │
│     Please wait...         │
│                            │
│  [████████░░░░] 75%       │
└────────────────────────────┘
```

### Success
```
✅ Meal plan generated successfully!
🎈🎈🎈 [Balloons animation]
```

### Error
```
❌ Could not generate optimal plan.
💡 Try increasing budget or selecting more ingredients
```

---

## 📊 Data Visualization Examples

### Pie Chart (Macros)
```
     Protein (20%)
    ┌────────────┐
    │      🔴    │
    │  🔵     🟡 │
    │    Food    │
    │  Pyramid   │
    └────────────┘
    Carbs (65%)  Fat (15%)
```

### Bar Chart (Requirements)
```
Required ░░░░░░░░░░
Achieved ████████░░
```

---

This visual guide provides a comprehensive overview of the application's user interface and user experience without actual screenshots. All elements are implemented in the actual application!

**For actual screenshots, run the application and take screenshots of each section.**

---

**Last Updated**: October 2025
