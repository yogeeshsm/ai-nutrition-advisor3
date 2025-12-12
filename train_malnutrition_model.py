"""
Train Random Forest Model for Malnutrition Prediction using Real CSV Data
Uses CUDA acceleration when available for faster training
"""

import pandas as pd
import numpy as np
import pickle
import os
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import LabelEncoder

# Try to use CUDA-accelerated cuML if available
USE_CUDA = False
try:
    from cuml.ensemble import RandomForestClassifier as cuRF
    import cudf
    USE_CUDA = True
    print("✅ CUDA/cuML detected - using GPU acceleration!")
except ImportError:
    print("⚠️  cuML not available - using CPU with optimized sklearn")
    print("   To enable GPU: pip install cuml-cu11 (requires NVIDIA GPU)")

def load_and_preprocess_data(csv_path):
    """Load CSV data and prepare for training"""
    print(f"\n📂 Loading data from: {csv_path}")
    
    df = pd.read_csv(csv_path)
    print(f"✅ Loaded {len(df)} samples")
    print(f"\nColumns: {list(df.columns)}")
    print(f"\nNutrition status distribution:")
    print(df['nutrition_status'].value_counts())
    
    # Fix bad data: Recalculate BMI if it looks wrong (e.g. all 10.0)
    # BMI = weight(kg) / (height(m))^2
    print("\n🛠️  Recalculating BMI from weight and height to ensure accuracy...")
    df['height_m'] = df['height_cm'] / 100.0
    df['bmi'] = df['weight_kg'] / (df['height_m'] ** 2)
    
    # Prepare features and target
    feature_columns = ['age_months', 'weight_kg', 'height_cm', 'muac_cm', 'bmi']
    X = df[feature_columns].values
    
    # Encode target labels
    le = LabelEncoder()
    y = le.fit_transform(df['nutrition_status'])
    
    print(f"\nFeatures shape: {X.shape}")
    print(f"Target classes: {le.classes_}")
    
    return X, y, le, feature_columns

def train_model_cpu(X_train, y_train, X_test, y_test):
    """Train Random Forest on CPU with optimizations"""
    print("\n🔧 Training Random Forest on CPU...")
    print("   Using optimized sklearn with parallel processing")
    
    model = RandomForestClassifier(
        n_estimators=200,  # More trees for better accuracy
        max_depth=15,
        min_samples_split=10,
        min_samples_leaf=4,
        max_features='sqrt',
        random_state=42,
        n_jobs=-1,  # Use all CPU cores
        verbose=1,
        class_weight='balanced'
    )
    
    start_time = datetime.now()
    model.fit(X_train, y_train)
    train_time = (datetime.now() - start_time).total_seconds()
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\n✅ Training completed in {train_time:.2f} seconds")
    print(f"📊 Test Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    
    return model, accuracy

def train_model_gpu(X_train, y_train, X_test, y_test):
    """Train Random Forest on GPU using cuML"""
    print("\n🚀 Training Random Forest on GPU (CUDA)...")
    
    # Convert to cuDF for GPU processing
    X_train_gpu = cudf.DataFrame(X_train)
    y_train_gpu = cudf.Series(y_train)
    X_test_gpu = cudf.DataFrame(X_test)
    
    model = cuRF(
        n_estimators=200,
        max_depth=15,
        max_features='sqrt',
        random_state=42,
        n_streams=4  # Parallel CUDA streams
    )
    
    start_time = datetime.now()
    model.fit(X_train_gpu, y_train_gpu)
    train_time = (datetime.now() - start_time).total_seconds()
    
    # Evaluate
    y_pred = model.predict(X_test_gpu).to_numpy()
    y_test_np = y_test
    accuracy = accuracy_score(y_test_np, y_pred)
    
    print(f"\n✅ GPU Training completed in {train_time:.2f} seconds")
    print(f"📊 Test Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"⚡ GPU Speedup achieved!")
    
    return model, accuracy

def save_model(model, label_encoder, feature_columns, accuracy, model_path='models/malnutrition'):
    """Save trained model and metadata"""
    os.makedirs(model_path, exist_ok=True)
    
    # Save main model
    model_file = os.path.join(model_path, 'trained_model.pkl')
    with open(model_file, 'wb') as f:
        pickle.dump(model, f)
    print(f"\n💾 Model saved: {model_file}")
    
    # Save label encoder
    encoder_file = os.path.join(model_path, 'label_encoder.pkl')
    with open(encoder_file, 'wb') as f:
        pickle.dump(label_encoder, f)
    print(f"💾 Label encoder saved: {encoder_file}")
    
    # Save metadata
    metadata = {
        'training_date': datetime.now().isoformat(),
        'accuracy': accuracy,
        'feature_columns': feature_columns,
        'classes': label_encoder.classes_.tolist(),
        'use_cuda': USE_CUDA
    }
    
    metadata_file = os.path.join(model_path, 'model_metadata.pkl')
    with open(metadata_file, 'wb') as f:
        pickle.dump(metadata, f)
    print(f"💾 Metadata saved: {metadata_file}")

def main():
    print("="*80)
    print("   MALNUTRITION PREDICTION MODEL TRAINING")
    print("="*80)
    
    # Load data
    csv_path = 'malnutrition_data _ad.csv'
    X, y, label_encoder, feature_columns = load_and_preprocess_data(csv_path)
    
    # Split data
    print(f"\n📊 Splitting data: 80% train, 20% test")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"   Training samples: {len(X_train)}")
    print(f"   Testing samples: {len(X_test)}")
    
    # Train model (GPU or CPU)
    if USE_CUDA:
        model, accuracy = train_model_gpu(X_train, y_train, X_test, y_test)
    else:
        model, accuracy = train_model_cpu(X_train, y_train, X_test, y_test)
    
    # Detailed evaluation
    print("\n" + "="*80)
    print("   MODEL EVALUATION")
    print("="*80)
    
    y_pred = model.predict(X_test) if not USE_CUDA else model.predict(cudf.DataFrame(X_test)).to_numpy()
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))
    
    print("\nConfusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    
    # Feature importance
    if hasattr(model, 'feature_importances_'):
        print("\n📈 Feature Importance:")
        importances = model.feature_importances_ if not USE_CUDA else model.feature_importances_.to_numpy()
        for feat, imp in zip(feature_columns, importances):
            print(f"   {feat:20s}: {imp:.4f}")
    
    # Save model
    save_model(model, label_encoder, feature_columns, accuracy)
    
    print("\n" + "="*80)
    print("   ✅ MODEL TRAINING COMPLETE!")
    print("="*80)
    print(f"\n📊 Final Accuracy: {accuracy*100:.2f}%")
    print(f"🎯 Ready for predictions!")
    print("\nNext steps:")
    print("  1. Restart Flask server to load new model")
    print("  2. Test predictions at /malnutrition-prediction")
    print("="*80)

if __name__ == '__main__':
    main()
