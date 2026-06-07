import os
import numpy as np
import torch
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt
import seaborn as sns

from app.pytorch_model import load_ensemble, CLASS_NAMES, TRANSFORM, DEVICE
from PIL import Image

# ================= SETTINGS =================
TEST_DIR = "dataset/test"  # Root test folder (19 class subfolders)

# ================= LOAD MODEL =================
print("Loading Ensemble Model...")
model = load_ensemble()
print("Model Loaded Successfully.\n")

y_true = []
y_pred = []

# ================= EVALUATE =================
print("Evaluating test dataset...\n")

for class_idx, class_name in enumerate(CLASS_NAMES):
    class_path = os.path.join(TEST_DIR, class_name)

    if not os.path.exists(class_path):
        print(f"Warning: Folder not found -> {class_path}")
        continue

    for img_name in os.listdir(class_path):
        img_path = os.path.join(class_path, img_name)

        try:
            img = Image.open(img_path).convert("RGB")
            img_tensor = TRANSFORM(img).unsqueeze(0).to(DEVICE)

            with torch.no_grad():
                predictions, _ = model.predict(img_tensor)

            pred_class = np.argmax(predictions)

            y_true.append(class_idx)
            y_pred.append(pred_class)

        except Exception as e:
            print(f"Error processing {img_path}: {e}")

# ================= METRICS =================
print("\n================= 19-CLASS CLASSIFICATION REPORT =================\n")

print(classification_report(y_true, y_pred, target_names=CLASS_NAMES))

accuracy = accuracy_score(y_true, y_pred)
precision_macro = precision_score(y_true, y_pred, average="macro")
recall_macro = recall_score(y_true, y_pred, average="macro")
f1_macro = f1_score(y_true, y_pred, average="macro")

print("------------------------------------------------------------------")
print("Accuracy           :", round(accuracy, 4))
print("Precision (macro)  :", round(precision_macro, 4))
print("Recall (macro)     :", round(recall_macro, 4))
print("F1-score (macro)   :", round(f1_macro, 4))
print("------------------------------------------------------------------")

# ================= CONFUSION MATRIX =================
cm = confusion_matrix(y_true, y_pred)

plt.figure(figsize=(14, 12))
sns.heatmap(cm, annot=False, cmap="Blues")

plt.title("Confusion Matrix - 19 Class Ensemble Model", fontsize=16)
plt.xlabel("Predicted Label")
plt.ylabel("True Label")

plt.xticks(np.arange(len(CLASS_NAMES)) + 0.5, CLASS_NAMES, rotation=90)
plt.yticks(np.arange(len(CLASS_NAMES)) + 0.5, CLASS_NAMES, rotation=0)

plt.tight_layout()
plt.show()

print("\nEvaluation Completed Successfully.")