"""
Dataset Preparation Helper
Helps you organize images for training the food recognition model
"""

import os
import shutil
from pathlib import Path
import random

# Food categories (must match INDIAN_FOOD_DATABASE)
FOOD_CATEGORIES = [
    'rice',
    'ragi_ball',
    'dal',
    'egg',
    'banana',
    'chapati',
    'chicken_curry',
    'milk',
    'yogurt',
    'vegetable_curry'
]

def create_folder_structure():
    """Create the required folder structure"""
    print("\n" + "="*60)
    print("CREATING DATASET FOLDER STRUCTURE")
    print("="*60)
    
    base_path = Path('dataset')
    train_path = base_path / 'train'
    val_path = base_path / 'validation'
    
    # Create directories
    for food_category in FOOD_CATEGORIES:
        train_category_path = train_path / food_category
        val_category_path = val_path / food_category
        
        train_category_path.mkdir(parents=True, exist_ok=True)
        val_category_path.mkdir(parents=True, exist_ok=True)
        
        print(f"✅ Created: {train_category_path}")
        print(f"✅ Created: {val_category_path}")
    
    print("\n✅ Folder structure created successfully!")
    print(f"\n📁 Dataset location: {base_path.absolute()}")


def split_dataset(train_ratio=0.8):
    """
    Split existing images in train folder into train/validation
    Useful if you've put all images in train folder
    """
    print("\n" + "="*60)
    print("SPLITTING DATASET (80% Train, 20% Validation)")
    print("="*60)
    
    base_path = Path('dataset')
    train_path = base_path / 'train'
    val_path = base_path / 'validation'
    
    for food_category in FOOD_CATEGORIES:
        train_category_path = train_path / food_category
        val_category_path = val_path / food_category
        
        if not train_category_path.exists():
            print(f"⚠️  Skipping {food_category}: folder not found")
            continue
        
        # Get all images
        images = list(train_category_path.glob('*.jpg')) + \
                 list(train_category_path.glob('*.jpeg')) + \
                 list(train_category_path.glob('*.png'))
        
        if len(images) == 0:
            print(f"⚠️  Skipping {food_category}: no images found")
            continue
        
        # Shuffle images
        random.shuffle(images)
        
        # Calculate split
        split_idx = int(len(images) * train_ratio)
        val_images = images[split_idx:]
        
        # Move validation images
        moved_count = 0
        for img in val_images:
            dest = val_category_path / img.name
            shutil.move(str(img), str(dest))
            moved_count += 1
        
        print(f"✅ {food_category:20s} Total: {len(images):3d}  " + 
              f"Train: {split_idx:3d}  Val: {moved_count:3d}")
    
    print("\n✅ Dataset split complete!")


def validate_dataset():
    """Check dataset and provide statistics"""
    print("\n" + "="*60)
    print("DATASET VALIDATION")
    print("="*60)
    
    base_path = Path('dataset')
    train_path = base_path / 'train'
    val_path = base_path / 'validation'
    
    total_train = 0
    total_val = 0
    issues = []
    
    print("\n📊 Dataset Statistics:")
    print("-" * 60)
    print(f"{'Category':<20} {'Train':<8} {'Val':<8} {'Total':<8} {'Status'}")
    print("-" * 60)
    
    for food_category in FOOD_CATEGORIES:
        train_category_path = train_path / food_category
        val_category_path = val_path / food_category
        
        # Count train images
        train_images = 0
        if train_category_path.exists():
            train_images = len(list(train_category_path.glob('*.jpg'))) + \
                          len(list(train_category_path.glob('*.jpeg'))) + \
                          len(list(train_category_path.glob('*.png')))
        
        # Count validation images
        val_images = 0
        if val_category_path.exists():
            val_images = len(list(val_category_path.glob('*.jpg'))) + \
                        len(list(val_category_path.glob('*.jpeg'))) + \
                        len(list(val_category_path.glob('*.png')))
        
        total = train_images + val_images
        total_train += train_images
        total_val += val_images
        
        # Status
        if total == 0:
            status = "❌ No images"
            issues.append(f"{food_category}: No images found")
        elif total < 20:
            status = "⚠️  Too few"
            issues.append(f"{food_category}: Only {total} images (recommend 50+)")
        elif total < 50:
            status = "⚠️  Small"
        else:
            status = "✅ Good"
        
        print(f"{food_category:<20} {train_images:<8} {val_images:<8} {total:<8} {status}")
    
    print("-" * 60)
    print(f"{'TOTAL':<20} {total_train:<8} {total_val:<8} {total_train + total_val:<8}")
    print("-" * 60)
    
    # Recommendations
    print("\n📝 Recommendations:")
    if total_train + total_val == 0:
        print("❌ No images found! Please add images to dataset/train/<category>/ folders")
    elif total_train + total_val < 200:
        print("⚠️  Small dataset. For better accuracy, aim for 50-100 images per category")
    else:
        print("✅ Dataset looks good! Ready for training")
    
    if issues:
        print("\n⚠️  Issues found:")
        for issue in issues:
            print(f"   - {issue}")
    
    return len(issues) == 0


def show_sample_images():
    """Display sample images from each category"""
    try:
        import matplotlib.pyplot as plt
        from PIL import Image
        
        print("\n" + "="*60)
        print("DISPLAYING SAMPLE IMAGES")
        print("="*60)
        
        base_path = Path('dataset/train')
        
        fig, axes = plt.subplots(2, 5, figsize=(15, 6))
        fig.suptitle('Sample Images from Each Category', fontsize=16)
        
        for idx, food_category in enumerate(FOOD_CATEGORIES):
            category_path = base_path / food_category
            
            # Get first image
            images = list(category_path.glob('*.jpg')) + \
                    list(category_path.glob('*.jpeg')) + \
                    list(category_path.glob('*.png'))
            
            row = idx // 5
            col = idx % 5
            ax = axes[row, col]
            
            if images:
                img = Image.open(images[0])
                ax.imshow(img)
                ax.set_title(food_category.replace('_', ' ').title())
            else:
                ax.text(0.5, 0.5, 'No images', 
                       ha='center', va='center', fontsize=12)
                ax.set_title(food_category.replace('_', ' ').title())
            
            ax.axis('off')
        
        plt.tight_layout()
        plt.savefig('dataset_preview.png')
        print("✅ Sample images saved to: dataset_preview.png")
        plt.show()
        
    except ImportError:
        print("⚠️  matplotlib not available. Skipping image preview.")


def main():
    """Main menu"""
    print("\n" + "="*60)
    print("FOOD RECOGNITION - DATASET PREPARATION")
    print("="*60)
    
    while True:
        print("\nWhat would you like to do?")
        print("1. Create folder structure")
        print("2. Split dataset (train/validation)")
        print("3. Validate dataset")
        print("4. Show sample images")
        print("5. Exit")
        
        choice = input("\nEnter choice (1-5): ").strip()
        
        if choice == '1':
            create_folder_structure()
            print("\n📝 Next steps:")
            print("   1. Add images to dataset/train/<category>/ folders")
            print("   2. Run option 2 to split into train/validation")
            print("   3. Run option 3 to validate")
            print("   4. Run: python train_food_model.py")
            
        elif choice == '2':
            split_dataset()
            
        elif choice == '3':
            is_valid = validate_dataset()
            if is_valid:
                print("\n✅ Dataset is ready for training!")
                print("   Run: python train_food_model.py")
            else:
                print("\n⚠️  Please fix the issues above before training")
                
        elif choice == '4':
            show_sample_images()
            
        elif choice == '5':
            print("\n👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice. Please enter 1-5")


if __name__ == "__main__":
    main()
