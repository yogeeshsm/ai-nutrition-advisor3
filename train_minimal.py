"""
MINIMAL Working Food Classifier
"""
from PIL import Image
import numpy as np
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

IMG_DIR = Path("food images_dataset/data/data")
imgs = list(IMG_DIR.glob("*.jpg"))[:500]  # First 500 images

print(f"Loading {len(imgs)} images...")

X, y = [], []
labels_map = {}
label_id = 0

for img_path in imgs:
    img = Image.open(img_path).convert('RGB').resize((32,32))
    X.append(np.array(img).flatten()/255.0)
    
    # Extract food name from filename
    fname = img_path.name
    food_name = '.'.join(fname.split('.')[1:]).rsplit('.', 1)[0][:30]
    
    # Map to numeric label
    if food_name not in labels_map:
        labels_map[food_name] = label_id
        label_id += 1
    y.append(labels_map[food_name])

X = np.array(X)
y = np.array(y)

print(f"Data shape: {X.shape}, Labels: {len(set(y))} classes")

# Save label mapping
import json
with open('models/food_labels_map.json', 'w', encoding='utf-8') as f:
    json.dump({v: k for k, v in labels_map.items()}, f, indent=2, ensure_ascii=False)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

print("Training...")
clf = RandomForestClassifier(n_estimators=20, max_depth=8, n_jobs=-1)
clf.fit(X_train, y_train)

acc = clf.score(X_test, y_test)
print(f"Accuracy: {acc*100:.1f}%")

joblib.dump(clf, "models/food_model_quick.pkl")
print("Saved to: models/food_model_quick.pkl")
