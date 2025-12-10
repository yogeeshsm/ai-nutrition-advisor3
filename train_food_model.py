"""
Training Script for Food Recognition Model
Train custom model on your own Indian food dataset

DATASET STRUCTURE REQUIRED:
dataset/
├── train/
│   ├── rice/
│   │   ├── image1.jpg
│   │   ├── image2.jpg
│   │   └── ...
│   ├── ragi_ball/
│   │   ├── image1.jpg
│   │   └── ...
│   ├── dal/
│   ├── egg/
│   ├── banana/
│   ├── chapati/
│   ├── chicken_curry/
│   ├── milk/
│   ├── yogurt/
│   └── vegetable_curry/
└── validation/
    ├── rice/
    ├── ragi_ball/
    └── ... (same structure)

INSTRUCTIONS:
1. Collect 50-100 images per food category
2. Organize them in the folder structure above
3. Run: python train_food_model.py
4. Model will be saved to models/food_model.h5
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# Configuration
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 20
DATASET_PATH = 'dataset'
MODEL_SAVE_PATH = 'models/food_model.h5'
TRAIN_PATH = os.path.join(DATASET_PATH, 'train')
VAL_PATH = os.path.join(DATASET_PATH, 'validation')


def check_dataset_structure():
    """Verify dataset exists and has proper structure"""
    print("\n" + "="*60)
    print("CHECKING DATASET STRUCTURE")
    print("="*60)
    
    if not os.path.exists(DATASET_PATH):
        print(f"\n❌ Dataset folder not found: {DATASET_PATH}")
        print("\n📁 Please create dataset structure:")
        print("""
dataset/
├── train/
│   ├── rice/
│   ├── ragi_ball/
│   ├── dal/
│   ├── egg/
│   ├── banana/
│   ├── chapati/
│   ├── chicken_curry/
│   ├── milk/
│   ├── yogurt/
│   └── vegetable_curry/
└── validation/
    └── (same folders as train)
        """)
        return False
    
    # Check train folder
    if not os.path.exists(TRAIN_PATH):
        print(f"❌ Training folder not found: {TRAIN_PATH}")
        return False
    
    # Check validation folder
    if not os.path.exists(VAL_PATH):
        print(f"❌ Validation folder not found: {VAL_PATH}")
        return False
    
    # Count images in each category
    print("\n📊 Dataset Statistics:")
    print("-" * 60)
    
    train_classes = os.listdir(TRAIN_PATH)
    total_train = 0
    total_val = 0
    
    for food_class in sorted(train_classes):
        train_class_path = os.path.join(TRAIN_PATH, food_class)
        val_class_path = os.path.join(VAL_PATH, food_class)
        
        if os.path.isdir(train_class_path):
            train_count = len([f for f in os.listdir(train_class_path) 
                              if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
            val_count = 0
            
            if os.path.exists(val_class_path):
                val_count = len([f for f in os.listdir(val_class_path) 
                                if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
            
            total_train += train_count
            total_val += val_count
            
            status = "✅" if train_count >= 20 else "⚠️"
            print(f"{status} {food_class:20s} Train: {train_count:3d}  Val: {val_count:3d}")
    
    print("-" * 60)
    print(f"Total:                  Train: {total_train:3d}  Val: {total_val:3d}")
    
    if total_train < 100:
        print("\n⚠️  WARNING: Small dataset. Recommended: 50+ images per class")
        print("   Model may not perform well with < 20 images per class")
    
    if total_val == 0:
        print("\n⚠️  WARNING: No validation data. Using 20% of training data")
    
    return True


def create_data_generators():
    """Create data generators with augmentation"""
    print("\n" + "="*60)
    print("CREATING DATA GENERATORS")
    print("="*60)
    
    # Training data augmentation
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest',
        validation_split=0.2 if not os.path.exists(VAL_PATH) else 0.0
    )
    
    # Validation data (no augmentation)
    val_datagen = ImageDataGenerator(
        rescale=1./255
    )
    
    # Create generators
    if os.path.exists(VAL_PATH) and len(os.listdir(VAL_PATH)) > 0:
        # Use separate validation folder
        train_generator = train_datagen.flow_from_directory(
            TRAIN_PATH,
            target_size=IMG_SIZE,
            batch_size=BATCH_SIZE,
            class_mode='categorical'
        )
        
        val_generator = val_datagen.flow_from_directory(
            VAL_PATH,
            target_size=IMG_SIZE,
            batch_size=BATCH_SIZE,
            class_mode='categorical'
        )
    else:
        # Split training data
        train_generator = train_datagen.flow_from_directory(
            TRAIN_PATH,
            target_size=IMG_SIZE,
            batch_size=BATCH_SIZE,
            class_mode='categorical',
            subset='training'
        )
        
        val_generator = train_datagen.flow_from_directory(
            TRAIN_PATH,
            target_size=IMG_SIZE,
            batch_size=BATCH_SIZE,
            class_mode='categorical',
            subset='validation'
        )
    
    print(f"\n✅ Training samples: {train_generator.samples}")
    print(f"✅ Validation samples: {val_generator.samples}")
    print(f"✅ Number of classes: {train_generator.num_classes}")
    print(f"✅ Class names: {list(train_generator.class_indices.keys())}")
    
    return train_generator, val_generator


def build_model(num_classes):
    """Build the model architecture"""
    print("\n" + "="*60)
    print("BUILDING MODEL ARCHITECTURE")
    print("="*60)
    
    # Base model - MobileNetV2 (efficient for deployment)
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=(224, 224, 3),
        include_top=False,
        weights='imagenet'
    )
    
    # Freeze base model initially
    base_model.trainable = False
    
    # Add custom classification head
    model = keras.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.5),
        layers.BatchNormalization(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    # Compile model
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    print(f"\n✅ Model built successfully")
    print(f"   Base model: MobileNetV2")
    print(f"   Total parameters: {model.count_params():,}")
    print(f"   Output classes: {num_classes}")
    
    return model, base_model


def train_model(model, base_model, train_gen, val_gen):
    """Train the model"""
    print("\n" + "="*60)
    print("TRAINING MODEL")
    print("="*60)
    
    # Callbacks
    checkpoint = keras.callbacks.ModelCheckpoint(
        MODEL_SAVE_PATH,
        monitor='val_accuracy',
        save_best_only=True,
        verbose=1
    )
    
    early_stop = keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=5,
        restore_best_weights=True,
        verbose=1
    )
    
    reduce_lr = keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.2,
        patience=3,
        min_lr=0.00001,
        verbose=1
    )
    
    # Phase 1: Train with frozen base
    print("\n📊 Phase 1: Training custom layers (base model frozen)")
    print("-" * 60)
    
    history1 = model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=EPOCHS // 2,
        callbacks=[checkpoint, early_stop, reduce_lr],
        verbose=1
    )
    
    # Phase 2: Fine-tune base model
    print("\n📊 Phase 2: Fine-tuning all layers")
    print("-" * 60)
    
    # Unfreeze base model
    base_model.trainable = True
    
    # Recompile with lower learning rate
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.0001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    history2 = model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=EPOCHS // 2,
        callbacks=[checkpoint, early_stop, reduce_lr],
        verbose=1
    )
    
    return model, history1, history2


def plot_training_history(history1, history2):
    """Plot training curves"""
    print("\n" + "="*60)
    print("GENERATING TRAINING PLOTS")
    print("="*60)
    
    # Combine histories
    acc = history1.history['accuracy'] + history2.history['accuracy']
    val_acc = history1.history['val_accuracy'] + history2.history['val_accuracy']
    loss = history1.history['loss'] + history2.history['loss']
    val_loss = history1.history['val_loss'] + history2.history['val_loss']
    
    epochs_range = range(len(acc))
    
    plt.figure(figsize=(15, 5))
    
    # Accuracy plot
    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, acc, label='Training Accuracy')
    plt.plot(epochs_range, val_acc, label='Validation Accuracy')
    plt.axvline(x=len(history1.history['accuracy']), color='r', 
                linestyle='--', label='Fine-tuning starts')
    plt.legend(loc='lower right')
    plt.title('Training and Validation Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.grid(True)
    
    # Loss plot
    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, loss, label='Training Loss')
    plt.plot(epochs_range, val_loss, label='Validation Loss')
    plt.axvline(x=len(history1.history['loss']), color='r', 
                linestyle='--', label='Fine-tuning starts')
    plt.legend(loc='upper right')
    plt.title('Training and Validation Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.grid(True)
    
    plt.tight_layout()
    
    # Save plot
    plot_path = 'models/training_history.png'
    os.makedirs('models', exist_ok=True)
    plt.savefig(plot_path)
    print(f"✅ Training plots saved to: {plot_path}")
    
    plt.show()


def evaluate_model(model, val_gen):
    """Evaluate final model performance"""
    print("\n" + "="*60)
    print("FINAL MODEL EVALUATION")
    print("="*60)
    
    loss, accuracy = model.evaluate(val_gen, verbose=0)
    
    print(f"\n📊 Final Results:")
    print(f"   Validation Loss: {loss:.4f}")
    print(f"   Validation Accuracy: {accuracy*100:.2f}%")
    
    if accuracy >= 0.90:
        print("\n✅ Excellent! Model is ready for deployment")
    elif accuracy >= 0.75:
        print("\n✅ Good! Model should work well")
    elif accuracy >= 0.60:
        print("\n⚠️  Fair. Consider collecting more data")
    else:
        print("\n❌ Poor performance. Need more/better quality data")
    
    return loss, accuracy


def save_class_mapping(train_gen):
    """Save class indices for later use"""
    import pickle
    
    class_indices = train_gen.class_indices
    mapping_path = 'models/class_mapping.pkl'
    
    os.makedirs('models', exist_ok=True)
    
    with open(mapping_path, 'wb') as f:
        pickle.dump(class_indices, f)
    
    print(f"✅ Class mapping saved to: {mapping_path}")


def main():
    """Main training pipeline"""
    print("\n" + "="*60)
    print("FOOD RECOGNITION MODEL TRAINING")
    print("Custom Indian Food Dataset")
    print("="*60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Step 1: Check dataset
    if not check_dataset_structure():
        print("\n❌ Dataset check failed. Please fix the issues above.")
        return
    
    # Step 2: Create data generators
    train_gen, val_gen = create_data_generators()
    
    # Step 3: Build model
    model, base_model = build_model(train_gen.num_classes)
    
    # Step 4: Train model
    model, history1, history2 = train_model(model, base_model, train_gen, val_gen)
    
    # Step 5: Plot training history
    plot_training_history(history1, history2)
    
    # Step 6: Evaluate model
    evaluate_model(model, val_gen)
    
    # Step 7: Save class mapping
    save_class_mapping(train_gen)
    
    # Final summary
    print("\n" + "="*60)
    print("TRAINING COMPLETE!")
    print("="*60)
    print(f"\n✅ Model saved to: {MODEL_SAVE_PATH}")
    print(f"✅ Class mapping saved")
    print(f"✅ Training plots saved")
    print(f"\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n🎉 Your model is ready to use!")
    print("\nNext steps:")
    print("1. Test the model: python test_food_recognition.py")
    print("2. Start the server: python flask_app.py")
    print("3. Visit: http://localhost:5000/food-recognition")
    print("="*60)


if __name__ == "__main__":
    # Check TensorFlow GPU availability
    print(f"\nTensorFlow version: {tf.__version__}")
    print(f"GPU available: {tf.config.list_physical_devices('GPU')}")
    
    main()
