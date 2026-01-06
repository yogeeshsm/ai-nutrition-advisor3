"""
Quick Model Accuracy Visualization - Optimized for Speed
Generates essential accuracy graphs without time-consuming computations
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import LabelEncoder
import os
from datetime import datetime

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

def create_output_directory():
    """Create directory for saving graphs"""
    output_dir = 'model_accuracy_graphs'
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def load_malnutrition_data():
    """Load and preprocess malnutrition data"""
    print("📂 Loading malnutrition data...")
    
    csv_path = 'malnutrition_data _ad.csv'
    df = pd.read_csv(csv_path)
    
    print(f"✅ Loaded {len(df)} samples")
    print(f"Classes:\n{df['nutrition_status'].value_counts()}\n")
    
    # Recalculate BMI
    df['height_m'] = df['height_cm'] / 100.0
    df['bmi'] = df['weight_kg'] / (df['height_m'] ** 2)
    
    # Prepare features and target
    feature_columns = ['age_months', 'weight_kg', 'height_cm', 'muac_cm', 'bmi']
    X = df[feature_columns].values
    
    # Encode target labels
    le = LabelEncoder()
    y = le.fit_transform(df['nutrition_status'])
    
    return X, y, le, feature_columns

def train_and_evaluate_model(X_train, X_test, y_train, y_test):
    """Train model and return predictions"""
    print("🔧 Training Random Forest model...")
    
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        min_samples_split=10,
        min_samples_leaf=4,
        max_features='sqrt',
        random_state=42,
        n_jobs=-1,
        class_weight='balanced',
        verbose=0
    )
    
    model.fit(X_train, y_train)
    
    # Predictions
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)
    
    # Calculate accuracies
    train_acc = accuracy_score(y_train, y_train_pred)
    test_acc = accuracy_score(y_test, y_test_pred)
    
    print(f"✅ Training Accuracy: {train_acc*100:.2f}%")
    print(f"✅ Test Accuracy: {test_acc*100:.2f}%\n")
    
    return model, y_train_pred, y_test_pred, train_acc, test_acc

def plot_train_test_accuracy(train_acc, test_acc, output_dir):
    """Plot training vs test accuracy comparison"""
    print("📊 Generating accuracy comparison...")
    
    plt.figure(figsize=(10, 6))
    
    metrics = ['Training Accuracy', 'Test Accuracy']
    values = [train_acc, test_acc]
    colors = ['#2E86AB', '#A23B72']
    
    bars = plt.bar(metrics, values, color=colors, alpha=0.8, edgecolor='black', linewidth=2)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.4f}\n({height*100:.2f}%)',
                ha='center', va='bottom', fontsize=14, fontweight='bold')
    
    plt.ylabel('Accuracy Score', fontsize=13, fontweight='bold')
    plt.title('Model Accuracy: Training vs Test Set', fontsize=15, fontweight='bold', pad=20)
    plt.ylim([0.7, 1.0])
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    
    filename = os.path.join(output_dir, '1_accuracy_comparison.png')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"   ✅ Saved: {filename}")
    plt.close()

def plot_confusion_matrix(y_test, y_test_pred, le, output_dir):
    """Generate confusion matrix heatmap"""
    print("📊 Generating confusion matrix...")
    
    cm = confusion_matrix(y_test, y_test_pred)
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=le.classes_, 
                yticklabels=le.classes_,
                cbar_kws={'label': 'Count'},
                linewidths=1,
                linecolor='white',
                annot_kws={'fontsize': 14, 'fontweight': 'bold'})
    
    plt.xlabel('Predicted Label', fontsize=13, fontweight='bold')
    plt.ylabel('True Label', fontsize=13, fontweight='bold')
    plt.title('Confusion Matrix - Prediction Accuracy by Class', fontsize=15, fontweight='bold', pad=20)
    plt.tight_layout()
    
    filename = os.path.join(output_dir, '2_confusion_matrix.png')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"   ✅ Saved: {filename}")
    plt.close()

def plot_class_wise_accuracy(y_test, y_test_pred, le, output_dir):
    """Plot accuracy for each class"""
    print("📊 Generating class-wise accuracy...")
    
    class_accuracies = []
    for i, class_name in enumerate(le.classes_):
        # Get samples of this class
        mask = (y_test == i)
        if mask.sum() > 0:
            acc = (y_test[mask] == y_test_pred[mask]).sum() / mask.sum()
            class_accuracies.append(acc)
        else:
            class_accuracies.append(0)
    
    plt.figure(figsize=(10, 6))
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    
    bars = plt.bar(le.classes_, class_accuracies, color=colors, alpha=0.8, edgecolor='black', linewidth=2)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f}\n({height*100:.1f}%)',
                ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    plt.ylabel('Accuracy Score', fontsize=13, fontweight='bold')
    plt.xlabel('Nutrition Status', fontsize=13, fontweight='bold')
    plt.title('Class-Wise Prediction Accuracy', fontsize=15, fontweight='bold', pad=20)
    plt.ylim([0, 1.1])
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    
    filename = os.path.join(output_dir, '3_class_wise_accuracy.png')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"   ✅ Saved: {filename}")
    plt.close()

def plot_feature_importance(model, feature_columns, output_dir):
    """Generate feature importance plot"""
    print("📊 Generating feature importance...")
    
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]
    
    plt.figure(figsize=(10, 6))
    colors = plt.cm.viridis(np.linspace(0, 1, len(feature_columns)))
    
    bars = plt.bar(range(len(importances)), importances[indices], color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    
    # Add value labels
    for i, bar in enumerate(bars):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f}',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.xticks(range(len(importances)), [feature_columns[i] for i in indices], fontsize=11)
    plt.ylabel('Importance Score', fontsize=13, fontweight='bold')
    plt.xlabel('Features', fontsize=13, fontweight='bold')
    plt.title('Feature Importance - Impact on Predictions', fontsize=15, fontweight='bold', pad=20)
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    
    filename = os.path.join(output_dir, '4_feature_importance.png')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"   ✅ Saved: {filename}")
    plt.close()

def plot_accuracy_by_tree_count(X_train, X_test, y_train, y_test, output_dir):
    """Plot how accuracy changes with number of trees"""
    print("📊 Generating accuracy vs tree count...")
    
    tree_counts = [10, 25, 50, 100, 150, 200]
    train_accs = []
    test_accs = []
    
    for n_trees in tree_counts:
        model = RandomForestClassifier(
            n_estimators=n_trees,
            max_depth=15,
            random_state=42,
            n_jobs=-1,
            class_weight='balanced',
            verbose=0
        )
        model.fit(X_train, y_train)
        
        train_acc = model.score(X_train, y_train)
        test_acc = model.score(X_test, y_test)
        
        train_accs.append(train_acc)
        test_accs.append(test_acc)
    
    plt.figure(figsize=(12, 6))
    plt.plot(tree_counts, train_accs, 'o-', color='#2E86AB', linewidth=2.5, markersize=10, 
             label='Training Accuracy', markeredgecolor='black', markeredgewidth=1.5)
    plt.plot(tree_counts, test_accs, 's-', color='#A23B72', linewidth=2.5, markersize=10, 
             label='Test Accuracy', markeredgecolor='black', markeredgewidth=1.5)
    
    # Add value labels
    for i, (tc, tr_acc, te_acc) in enumerate(zip(tree_counts, train_accs, test_accs)):
        plt.text(tc, tr_acc + 0.01, f'{tr_acc:.3f}', ha='center', fontsize=9)
        plt.text(tc, te_acc - 0.015, f'{te_acc:.3f}', ha='center', fontsize=9)
    
    plt.xlabel('Number of Trees', fontsize=13, fontweight='bold')
    plt.ylabel('Accuracy Score', fontsize=13, fontweight='bold')
    plt.title('Model Accuracy vs Number of Trees', fontsize=15, fontweight='bold', pad=20)
    plt.legend(fontsize=12, loc='lower right')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    filename = os.path.join(output_dir, '5_accuracy_vs_trees.png')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"   ✅ Saved: {filename}")
    plt.close()

def plot_prediction_distribution(y_test, y_test_pred, le, output_dir):
    """Plot distribution of predictions vs actual"""
    print("📊 Generating prediction distribution...")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Actual distribution
    actual_counts = np.bincount(y_test)
    ax1.bar(le.classes_, actual_counts, color='#4ECDC4', alpha=0.8, edgecolor='black', linewidth=2)
    ax1.set_title('Actual Distribution', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Count', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Nutrition Status', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Add value labels
    for i, v in enumerate(actual_counts):
        ax1.text(i, v, str(v), ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    # Predicted distribution
    pred_counts = np.bincount(y_test_pred, minlength=len(le.classes_))
    ax2.bar(le.classes_, pred_counts, color='#FF6B6B', alpha=0.8, edgecolor='black', linewidth=2)
    ax2.set_title('Predicted Distribution', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Count', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Nutrition Status', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Add value labels
    for i, v in enumerate(pred_counts):
        ax2.text(i, v, str(v), ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.suptitle('Test Set: Actual vs Predicted Distribution', fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    
    filename = os.path.join(output_dir, '6_prediction_distribution.png')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"   ✅ Saved: {filename}")
    plt.close()

def generate_report(train_acc, test_acc, le, y_test, y_test_pred, output_dir):
    """Generate text report"""
    print("📝 Generating text report...")
    
    report_path = os.path.join(output_dir, 'accuracy_report.txt')
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("   MALNUTRITION PREDICTION MODEL - ACCURACY REPORT\n")
        f.write("="*80 + "\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("="*80 + "\n")
        f.write("   OVERALL ACCURACY\n")
        f.write("="*80 + "\n\n")
        f.write(f"Training Accuracy:     {train_acc:.4f} ({train_acc*100:.2f}%)\n")
        f.write(f"Test Accuracy:         {test_acc:.4f} ({test_acc*100:.2f}%)\n\n")
        
        f.write("="*80 + "\n")
        f.write("   CLASS-WISE ACCURACY\n")
        f.write("="*80 + "\n\n")
        
        for i, class_name in enumerate(le.classes_):
            mask = (y_test == i)
            if mask.sum() > 0:
                acc = (y_test[mask] == y_test_pred[mask]).sum() / mask.sum()
                f.write(f"{class_name:15s}: {acc:.4f} ({acc*100:.2f}%)\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("   CLASSIFICATION REPORT\n")
        f.write("="*80 + "\n\n")
        f.write(classification_report(y_test, y_test_pred, target_names=le.classes_))
        
        f.write("\n" + "="*80 + "\n")
        f.write("   GENERATED GRAPHS\n")
        f.write("="*80 + "\n\n")
        f.write("1. 1_accuracy_comparison.png - Training vs Test accuracy\n")
        f.write("2. 2_confusion_matrix.png - Prediction matrix by class\n")
        f.write("3. 3_class_wise_accuracy.png - Accuracy for each class\n")
        f.write("4. 4_feature_importance.png - Feature contributions\n")
        f.write("5. 5_accuracy_vs_trees.png - Accuracy vs model complexity\n")
        f.write("6. 6_prediction_distribution.png - Actual vs predicted distribution\n")
        f.write("\n" + "="*80 + "\n")
    
    print(f"   ✅ Saved: {report_path}")

def main():
    """Main function"""
    print("="*80)
    print("   MODEL TRAINING ACCURACY VISUALIZATION")
    print("="*80 + "\n")
    
    # Create output directory
    output_dir = create_output_directory()
    print(f"📁 Output directory: {output_dir}\n")
    
    # Load data
    X, y, le, feature_columns = load_malnutrition_data()
    
    # Split data
    print("📊 Splitting data: 80% train, 20% test")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"   Training samples: {len(X_train)}")
    print(f"   Test samples: {len(X_test)}\n")
    
    # Train model
    model, y_train_pred, y_test_pred, train_acc, test_acc = train_and_evaluate_model(
        X_train, X_test, y_train, y_test
    )
    
    # Generate all visualizations
    print("="*80)
    print("   GENERATING VISUALIZATIONS")
    print("="*80 + "\n")
    
    plot_train_test_accuracy(train_acc, test_acc, output_dir)
    plot_confusion_matrix(y_test, y_test_pred, le, output_dir)
    plot_class_wise_accuracy(y_test, y_test_pred, le, output_dir)
    plot_feature_importance(model, feature_columns, output_dir)
    plot_accuracy_by_tree_count(X_train, X_test, y_train, y_test, output_dir)
    plot_prediction_distribution(y_test, y_test_pred, le, output_dir)
    
    # Generate text report
    generate_report(train_acc, test_acc, le, y_test, y_test_pred, output_dir)
    
    print("\n" + "="*80)
    print("   ✅ ALL GRAPHS GENERATED SUCCESSFULLY!")
    print("="*80)
    print(f"\n📊 Location: {os.path.abspath(output_dir)}")
    print(f"\n📈 Final Test Accuracy: {test_acc*100:.2f}%")
    print("\n" + "="*80)

if __name__ == '__main__':
    main()
