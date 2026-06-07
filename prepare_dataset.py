import os
import shutil
import pandas as pd

# Paths (EDIT ONLY IF NEEDED)
CSV_PATH = r"C:\Users\Joels\Downloads\archive (4)\HAM10000_metadata.csv"
IMAGES_DIR = r"D:/Downloads/archive (4)/processed_images_dataset/processed_images"
OUTPUT_DIR = r"D:/Smart_Dermatology_AI/dataset"

# Load CSV
df = pd.read_csv(CSV_PATH)

# Create class folders
for label in df['dx'].unique():
    os.makedirs(os.path.join(OUTPUT_DIR, label), exist_ok=True)

# Move images
for _, row in df.iterrows():
    img_name = row['image_id'] + ".jpg"
    label = row['dx']

    src = os.path.join(IMAGES_DIR, img_name)
    dst = os.path.join(OUTPUT_DIR, label, img_name)

    if os.path.exists(src):
        shutil.copy(src, dst)

print("✅ Dataset organized successfully!")
