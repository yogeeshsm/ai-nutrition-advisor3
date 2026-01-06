"""
Model Training Accuracy Visualization
Generates comprehensive graphs showing training accuracy, validation accuracy, and model performance
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, learning_curve, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_curve, auc
from sklearn.preprocessing import LabelEncoder, label_binarize
import os
from datetime import datetime

# Set style for better-looking plots
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
    print(f"Classes: {df['nutrition_status'].value_counts()}")
    
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

def plot_learning_curves(X, y, output_dir):
    """Generate learning curves showing training and validation accuracy over different training set sizes"""
    print("\n📊 Generating learning curves...")
    
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        min_samples_split=10,
        min_samples_leaf=4,
        max_features='sqrt',
        random_state=42,
        n_jobs=-1,
        class_weight='balanced'
    )
    
    # Calculate learning curves
    train_sizes, train_scores, val_scores = learning_curve(
        model, X, y, 
        cv=5,
        n_jobs=-1,
        train_sizes=np.linspace(0.1, 1.0, 10),
        scoring='accuracy',
        random_state=42
    )
    
    # Calculate mean and std
    train_mean = np.mean(train_scores, axis=1)
    train_std = np.std(train_scores, axis=1)
    val_mean = np.mean(val_scores, axis=1)
    val_std = np.std(val_scores, axis=1)
    
    # Plot learning curves
    plt.figure(figsize=(12, 6))
    plt.plot(train_sizes, train_mean, 'o-', color='#2E86AB', linewidth=2.5, label='Training Accuracy')
    plt.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, alpha=0.2, color='#2E86AB')
    
    plt.plot(train_sizes, val_mean, 'o-', color='#A23B72', linewidth=2.5, label='Validation Accuracy')
    plt.fill_between(train_sizes, val_mean - val_std, val_mean + val_std, alpha=0.2, color='#A23B72')
    
    plt.xlabel('Training Set Size', fontsize=12, fontweight='bold')
    plt.ylabel('Accuracy Score', fontsize=12, fontweight='bold')
    plt.title('Learning Curves - Model Accuracy vs Training Size', fontsize=14, fontweight='bold', pad=20)
    plt.legend(loc='lower right', fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Save plot
    filename = os.path.join(output_dir, 'learning_curves.png')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"   ✅ Saved: {filename}")
    plt.close()
    
    return val_mean[-1]  # Return final validation accuracy

def plot_cross_validation_scores(X, y, output_dir):
    """Generate cross-validation accuracy scores"""
    print("\n📊 Generating cross-validation scores...")
    
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        min_samples_split=10,
        min_samples_leaf=4,
        max_features='sqrt',
        random_state=42,
        n_jobs=-1,
        class_weight='balanced'
    )
    
    # Perform cross-validation
    cv_scores = cross_val_score(model, X, y, cv=10, scoring='accuracy', n_jobs=-1)
    
    # Plot cross-validation scores
    plt.figure(figsize=(10, 6))
    
    folds = range(1, len(cv_scores) + 1)
    plt.bar(folds, cv_scores, color='#06A77D', alpha=0.8, edgecolor='black', linewidth=1.2)
    plt.axhline(y=cv_scores.mean(), color='#D62828', linestyle='--', linewidth=2, label=f'Mean: {cv_scores.mean():.4f}')
    
    plt.xlabel('Fold Number', fontsize=12, fontweight='bold')
    plt.ylabel('Accuracy Score', fontsize=12, fontweight='bold')
    plt.title('10-Fold Cross-Validation Accuracy Scores', fontsize=14, fontweight='bold', pad=20)
    plt.legend(fontsize=11)
    plt.ylim([0.7, 1.0])
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    
    # Save plot
    filename = os.path.join(output_dir, 'cross_validation_scores.png')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"   ✅ Saved: {filename}")
    plt.close()
    
    return cv_scores.mean(), cv_scores.std()

def plot_confusion_matrix(X, y, le, output_dir):
    """Generate confusion matrix heatmap"""
    print("\n📊 Generating confusion matrix...")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Train model
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        min_samples_split=10,
        min_samples_leaf=4,
        max_features='sqrt',
        random_state=42,
        n_jobs=-1,
        class_weight='balanced'
    )
    
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    # Calculate confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    
    # Plot confusion matrix
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='YlGnBu', 
                xticklabels=le.classes_, 
                yticklabels=le.classes_,
                cbar_kws={'label': 'Count'},
                linewidths=0.5,
                linecolor='gray')
    
    plt.xlabel('Predicted Label', fontsize=12, fontweight='bold')
    plt.ylabel('True Label', fontsize=12, fontweight='bold')
    plt.title('Confusion Matrix - Model Predictions', fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    
    # Save plot
    filename = os.path.join(output_dir, 'confusion_matrix.png')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"   ✅ Saved: {filename}")
    plt.close()
    
    # Calculate test accuracy
    test_accuracy = accuracy_score(y_test, y_pred)
    return test_accuracy

def plot_feature_importance(X, y, feature_columns, output_dir):
    """Generate feature importance plot"""
    print("\n📊 Generating feature importance plot...")
    
    # Train model
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        min_samples_split=10,
        min_samples_leaf=4,
        max_features='sqrt',
        random_state=42,
        n_jobs=-1,
        class_weight='balanced'
    )
    
    model.fit(X, y)
    
    # Get feature importances
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]
    
    # Plot feature importance
    plt.figure(figsize=(10, 6))
    colors = plt.cm.viridis(np.linspace(0, 1, len(feature_columns)))
    
    plt.bar(range(len(importances)), importances[indices], color=colors, alpha=0.8, edgecolor='black', linewidth=1.2)
    plt.xticks(range(len(importances)), [feature_columns[i] for i in indices], rotation=45, ha='right')
    
    plt.xlabel('Features', fontsize=12, fontweight='bold')
    plt.ylabel('Importance Score', fontsize=12, fontweight='bold')
    plt.title('Feature Importance - Random Forest Model', fontsize=14, fontweight='bold', pad=20)
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    
    # Save plot
    filename = os.path.join(output_dir, 'feature_importance.png')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"   ✅ Saved: {filename}")
    plt.close()

def plot_roc_curves(X, y, le, output_dir):
    """Generate ROC curves for multi-class classification"""
    print("\n📊 Generating ROC curves...")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Train model
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        min_samples_split=10,
        min_samples_leaf=4,
        max_features='sqrt',
        random_state=42,
        n_jobs=-1,
        class_weight='balanced'
    )
    
    model.fit(X_train, y_train)
    
    # Get probability predictions
    y_score = model.predict_proba(X_test)
    
    # Binarize the output for ROC curve
    n_classes = len(le.classes_)
    y_test_bin = label_binarize(y_test, classes=range(n_classes))
    
    # Compute ROC curve and ROC area for each class
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    
    plt.figure(figsize=(10, 8))
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
    
    for i in range(n_classes):
        fpr[i], tpr[i], _ = roc_curve(y_test_bin[:, i], y_score[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])
        
        plt.plot(fpr[i], tpr[i], color=colors[i % len(colors)], linewidth=2.5,
                label=f'{le.classes_[i]} (AUC = {roc_auc[i]:.3f})')
    
    # Plot diagonal
    plt.plot([0, 1], [0, 1], 'k--', linewidth=2, label='Random Classifier')
    
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate', fontsize=12, fontweight='bold')
    plt.ylabel('True Positive Rate', fontsize=12, fontweight='bold')
    plt.title('ROC Curves - Multi-Class Classification', fontsize=14, fontweight='bold', pad=20)
    plt.legend(loc='lower right', fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Save plot
    filename = os.path.join(output_dir, 'roc_curves.png')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"   ✅ Saved: {filename}")
    plt.close()

def plot_accuracy_summary(metrics, output_dir):
    """Generate summary bar chart of all accuracy metrics"""
    print("\n📊 Generating accuracy summary chart...")
    
    metric_names = list(metrics.keys())
    metric_values = list(metrics.values())
    
    plt.figure(figsize=(12, 6))
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
    
    bars = plt.bar(metric_names, metric_values, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.4f}\n({height*100:.2f}%)',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.ylabel('Accuracy Score', fontsize=12, fontweight='bold')
    plt.title('Model Accuracy Metrics Summary', fontsize=14, fontweight='bold', pad=20)
    plt.ylim([0.7, 1.0])
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    
    # Save plot
    filename = os.path.join(output_dir, 'accuracy_summary.png')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"   ✅ Saved: {filename}")
    plt.close()

def plot_training_validation_comparison(X, y, output_dir):
    """Plot comparison of training vs validation accuracy over different tree counts"""
    print("\n📊 Generating training vs validation comparison...")
    
    tree_counts = [10, 25, 50, 100, 150, 200, 250, 300]
    train_accs = []
    val_accs = []
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    for n_trees in tree_counts:
        model = RandomForestClassifier(
            n_estimators=n_trees,
            max_depth=15,
            random_state=42,
            n_jobs=-1,
            class_weight='balanced'
        )
        model.fit(X_train, y_train)
        
        train_acc = model.score(X_train, y_train)
        val_acc = model.score(X_test, y_test)
        
        train_accs.append(train_acc)
        val_accs.append(val_acc)
    
    plt.figure(figsize=(12, 6))
    plt.plot(tree_counts, train_accs, 'o-', color='#2E86AB', linewidth=2.5, markersize=8, label='Training Accuracy')
    plt.plot(tree_counts, val_accs, 's-', color='#A23B72', linewidth=2.5, markersize=8, label='Validation Accuracy')
    
    plt.xlabel('Number of Trees', fontsize=12, fontweight='bold')
    plt.ylabel('Accuracy Score', fontsize=12, fontweight='bold')
    plt.title('Training vs Validation Accuracy - Effect of Model Complexity', fontsize=14, fontweight='bold', pad=20)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Save plot
    filename = os.path.join(output_dir, 'train_val_comparison.png')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"   ✅ Saved: {filename}")
    plt.close()

def generate_report(metrics, output_dir):
    """Generate text report with all metrics"""
    print("\n📝 Generating text report...")
    
    report_path = os.path.join(output_dir, 'accuracy_report.txt')
    
    with open(report_path, 'w') as f:
        f.write("="*80 + "\n")
        f.write("   MALNUTRITION PREDICTION MODEL - ACCURACY REPORT\n")
        f.write("="*80 + "\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("="*80 + "\n")
        f.write("   ACCURACY METRICS\n")
        f.write("="*80 + "\n\n")
        
        for metric_name, metric_value in metrics.items():
            f.write(f"{metric_name:30s}: {metric_value:.4f} ({metric_value*100:.2f}%)\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("   GRAPHS GENERATED\n")
        f.write("="*80 + "\n\n")
        f.write("1. learning_curves.png - Training and validation accuracy over training size\n")
        f.write("2. cross_validation_scores.png - 10-fold cross-validation results\n")
        f.write("3. confusion_matrix.png - Prediction accuracy matrix\n")
        f.write("4. feature_importance.png - Feature contribution to predictions\n")
        f.write("5. roc_curves.png - ROC curves for each class\n")
        f.write("6. accuracy_summary.png - Summary of all accuracy metrics\n")
        f.write("7. train_val_comparison.png - Training vs validation accuracy\n")
        f.write("\n" + "="*80 + "\n")
    
    print(f"   ✅ Saved: {report_path}")

def main():
    """Main function to generate all graphs"""
    print("="*80)
    print("   MODEL TRAINING ACCURACY VISUALIZATION")
    print("="*80)
    
    # Create output directory
    output_dir = create_output_directory()
    print(f"\n📁 Output directory: {output_dir}")
    
    # Load data
    X, y, le, feature_columns = load_malnutrition_data()
    
    # Generate all visualizations
    metrics = {}
    
    # 1. Learning curves
    val_acc = plot_learning_curves(X, y, output_dir)
    metrics['Learning Curve Val Accuracy'] = val_acc
    
    # 2. Cross-validation scores
    cv_mean, cv_std = plot_cross_validation_scores(X, y, output_dir)
    metrics['Cross-Validation Mean'] = cv_mean
    metrics['Cross-Validation Std'] = cv_std
    
    # 3. Confusion matrix
    test_acc = plot_confusion_matrix(X, y, le, output_dir)
    metrics['Test Set Accuracy'] = test_acc
    
    # 4. Feature importance
    plot_feature_importance(X, y, feature_columns, output_dir)
    
    # 5. ROC curves
    plot_roc_curves(X, y, le, output_dir)
    
    # 6. Accuracy summary
    plot_accuracy_summary(metrics, output_dir)
    
    # 7. Training vs validation comparison
    plot_training_validation_comparison(X, y, output_dir)
    
    # 8. Generate text report
    generate_report(metrics, output_dir)
    
    print("\n" + "="*80)
    print("   ✅ ALL GRAPHS GENERATED SUCCESSFULLY!")
    print("="*80)
    print(f"\n📊 Graphs saved in: {output_dir}/")
    print("\nGenerated files:")
    print("  1. learning_curves.png")
    print("  2. cross_validation_scores.png")
    print("  3. confusion_matrix.png")
    print("  4. feature_importance.png")
    print("  5. roc_curves.png")
    print("  6. accuracy_summary.png")
    print("  7. train_val_comparison.png")
    print("  8. accuracy_report.txt")
    print("\n" + "="*80)

if __name__ == '__main__':
    main()
