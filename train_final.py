"""
Indian Food Classifier using CSV labels
Fast and accurate training
"""

import numpy as np
import pandas as pd
from PIL import Image
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import joblib
import json

print("="*70)
print("INDIAN FOOD IMAGE CLASSIFIER - FINAL VERSION")
print("="*70)

# Configuration
IMAGE_DIR = Path("food images_dataset/data/data")
CSV_FILE = Path("food images_dataset/cuisine_updated.csv")
MODEL_DIR = Path("models")
MODEL_DIR.mkdir(exist_ok=True)

IMG_SIZE = 48  # Balanced size
MAX_IMAGES_PER_CLASS = 50  # Limit per class for speed

print("\n[1/5] Loading CSV data...")
df = pd.read_csv(CSV_FILE)
print(f"Total recipes in CSV: {len(df)}")

# Get image files
image_files = {img.name: str(img) for img in IMAGE_DIR.glob("*.jpg")}
print(f"Total image files: {len(image_files)}")

# Match CSV names with image files
print("\n[2/5] Matching images with labels...")
matched_data = []

for idx, row in df.iterrows():
    name = row['name']
    # Try to find matching image
    for img_name, img_path in image_files.items():
        if name.replace(' ', '_') in img_name or name.replace(' ', '-') in img_name:
            matched_data.append((img_path, name, row.get('cuisine', 'Indian')))
            break

print(f"Matched {len(matched_data)} images with labels")

# Balance classes - take top N recipes with most matches
from collections import Counter
name_counts = Counter([d[1] for d in matched_data])
print(f"\nTop 15 foods by image count:")
for name, count in name_counts.most_common(15):
    print(f"  {name}: {count} images")

# Keep foods with at least 5 images
MIN_IMAGES = 5
valid_names = {name for name, count in name_counts.items() if count >= MIN_IMAGES}
filtered_data = [d for d in matched_data if d[1] in valid_names]

print(f"\n[OK] {len(valid_names)} food types with {MIN_IMAGES}+ images")
print(f"[OK] {len(filtered_data)} total training images")

# Sample to balance
from collections import defaultdict
balanced_data = defaultdict(list)
for path, name, cuisine in filtered_data:
    if len(balanced_data[name]) < MAX_IMAGES_PER_CLASS:
        balanced_data[name].append((path, name))

final_data = []
for name, items in balanced_data.items():
    final_data.extend(items)

print(f"[OK] Balanced dataset: {len(final_data)} images")

# Load and process images
print("\n[3/5] Processing images...")
X = []
y = []
success = 0

for i, (img_path, food_name) in enumerate(final_data):
    if i % 50 == 0:
        print(f"  Processing: {i}/{len(final_data)}")
    
    try:
        img = Image.open(img_path).convert('RGB')
        img = img.resize((IMG_SIZE, IMG_SIZE), Image.LANCZOS)
        img_array = np.array(img).flatten() / 255.0
        
        X.append(img_array)
        y.append(food_name)
        success += 1
    except:
        continue

X = np.array(X)
y = np.array(y)

print(f"[OK] Processed {success} images successfully")
print(f"[OK] Feature matrix: {X.shape}")

# Encode labels
le = LabelEncoder()
y_encoded = le.fit_transform(y)
NUM_CLASSES = len(le.classes_)

print(f"[OK] {NUM_CLASSES} food classes")

# Split dataset
print("\n[4/5] Training model...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.25, random_state=42, stratify=y_encoded
)

print(f"Training set: {len(X_train)} images")
print(f"Test set: {len(X_test)} images")

# Train Random Forest
clf = RandomForestClassifier(
    n_estimators=50,
    max_depth=15,
    min_samples_split=5,
    n_jobs=-1,
    random_state=42,
    verbose=0
)

print("Training Random Forest classifier...")
clf.fit(X_train, y_train)

# Evaluate
train_acc = accuracy_score(y_train, clf.predict(X_train))
test_acc = accuracy_score(y_test, clf.predict(X_test))

print(f"\nTraining Accuracy: {train_acc*100:.2f}%")
print(f"Test Accuracy: {test_acc*100:.2f}%")

# Get per-class accuracy
y_pred = clf.predict(X_test)
report = classification_report(y_test, y_pred, target_names=le.classes_, output_dict=True)

# Save model
print("\n[5/5] Saving model...")
joblib.dump(clf, MODEL_DIR / 'food_classifier_final.pkl')
joblib.dump(le, MODEL_DIR / 'label_encoder_final.pkl')

metadata = {
    'model_type': 'RandomForestClassifier',
    'num_classes': NUM_CLASSES,
    'classes': le.classes_.tolist(),
    'img_size': IMG_SIZE,
    'train_samples': len(X_train),
    'test_samples': len(X_test),
    'train_accuracy': float(train_acc),
    'test_accuracy': float(test_acc),
    'per_class_f1': {name: report[name]['f1-score'] for name in le.classes_ if name in report}
}

with open(MODEL_DIR / 'food_model_metadata.json', 'w', encoding='utf-8') as f:
    json.dump(metadata, f, indent=2, ensure_ascii=False)

print("\n" + "="*70)
print("MODEL TRAINING COMPLETE!")
print("="*70)
print(f"Model Type: Random Forest")
print(f"Food Classes: {NUM_CLASSES}")
print(f"Test Accuracy: {test_acc*100:.2f}%")
print(f"Trained on: {len(X_train)} images")
print(f"Saved to: models/food_classifier_final.pkl")
print("="*70)

# Create prediction script
pred_code = """import joblib
import numpy as np
from PIL import Image

# Load model
clf = joblib.load('models/food_classifier_final.pkl')
le = joblib.load('models/label_encoder_final.pkl')

def predict_food(image_path):
    '''Predict food from image path'''
    img = Image.open(image_path).convert('RGB')
    img = img.resize((48, 48))
    X = np.array(img).flatten() / 255.0
    
    pred_idx = clf.predict([X])[0]
    proba = clf.predict_proba([X])[0]
    confidence = proba[pred_idx]
    food_name = le.inverse_transform([pred_idx])[0]
    
    # Get top 3 predictions
    top3_idx = np.argsort(proba)[-3:][::-1]
    top3 = [(le.inverse_transform([idx])[0], proba[idx]) for idx in top3_idx]
    
    return food_name, confidence, top3

# Example usage
if __name__ == '__main__':
    test_img = 'food images_dataset/data/data/1.Doddapatre_Tambuli_Recipe_Karuveppilai_Thayir_Pachadi-1.jpg'
    food, conf, top3 = predict_food(test_img)
    
    print(f'\\nPredicted: {food} ({conf*100:.1f}% confidence)\\n')
    print('Top 3 predictions:')
    for i, (name, prob) in enumerate(top3, 1):
        print(f'  {i}. {name}: {prob*100:.1f}%')
"""

with open('predict_indian_food.py', 'w') as f:
    f.write(pred_code)

print("\n[INFO] Test with: python predict_indian_food.py")
