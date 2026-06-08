# Smart-Dermatology-Diagnosis-Using-AI
An AI-powered web application for automated skin disease classification using an ensemble of EfficientNet-B4 and DenseNet-121 with Grad-CAM explainability.

## Project Overview

Smart Dermatology Diagnosis Using AI is a web-based clinical decision support system that assists in identifying skin diseases from clinical images.

The system combines EfficientNet-B4 and DenseNet-121 using ensemble learning to classify skin diseases into 19 categories. It also integrates Grad-CAM visualizations to provide explainable AI predictions and automatically generates diagnostic PDF reports.

## Features

✔ 19-Class Skin Disease Classification

✔ Ensemble Learning (EfficientNet-B4 + DenseNet-121)

✔ Grad-CAM Explainability

✔ Test-Time Augmentation (TTA)

✔ Automated PDF Report Generation

✔ User Authentication System

✔ SQLite Database Integration

✔ Admin Dashboard

✔ Responsive Web Interface

## System Architecture

<img width="6250" height="4419" alt="Architecture Diagram - Dermatology Project" src="https://github.com/user-attachments/assets/6e99c7bf-83a4-4d92-909c-c0a40ab40f66" />

## Workflow

1. User Login / Registration
2. Upload Skin Image
3. Image Preprocessing
4. Ensemble Model Prediction
5. Grad-CAM Heatmap Generation
6. Disease Classification
7. PDF Report Generation
8. Record Storage in Database

## Technology Stack

### Frontend
- HTML
- CSS
- JavaScript

### Backend
- Flask

### Deep Learning
- PyTorch
- EfficientNet-B4
- DenseNet-121

### Database
- SQLite

### Tools
- VS Code
- Kaggle
- Google Colab

## Dataset

Dataset: DermNet Dataset

Total Classes: 19

Total Test Images: 3,657

Disease Categories:
- Acne and Rosacea
- Bacterial Infection
- Contact Dermatitis
- Eczema
- Fungal Infection
- Hair Loss
- Herpes & STDs
- Infestations & Bites
- Lupus and Connective Tissue Disease
- Malignant Lesions
- Melanoma & Nevi
- Nail Disease
- Pigmentation Disorders
- Psoriasis & Lichen Planus
- Seborrheic Keratoses & Benign Tumors
- Systemic Disease
- Urticaria
- Vascular Disorders
- Viral Infection

## Model Performance

| Metric | Score |
|----------|----------|
| Accuracy | 58.98% |
| Precision | 54.65% |
| Recall | 52.74% |
| F1 Score | 53.17% |

## Detailed Evaluation

The complete classification report, testing results, architecture diagrams, Grad-CAM visualizations, and implementation details are available in the project report.

📄 Project Report: [Project Report - Smart Dermatology Diagnosis Using AI.pdf](Project%20Report%20-%20Smart%20Dermatology%20Diagnosis%20Using%20AI.pdf)

## Screenshots
Home Page
<img width="1920" height="1011" alt="Screenshot 1" src="https://github.com/user-attachments/assets/6dfaf958-f99e-4a90-954f-55bd11e46818" />
<img width="1920" height="1014" alt="Screenshot 2" src="https://github.com/user-attachments/assets/0dfbaa5c-daf3-4757-a175-46a0d5594a68" />

Admin Page
<img width="1920" height="1011" alt="Screenshot 3" src="https://github.com/user-attachments/assets/47ffa729-1d9f-4be9-8aaf-2ac01d0a200b" />

Admin Dashboard
<img width="1920" height="1011" alt="Screenshot 4" src="https://github.com/user-attachments/assets/8b934d09-f12d-4b42-97ea-2a643b18bbed" />
<img width="1920" height="1014" alt="Screenshot 5" src="https://github.com/user-attachments/assets/ffec771e-57bd-40a5-ac73-e80576b659c5" />
<img width="1920" height="1011" alt="Screenshot 6" src="https://github.com/user-attachments/assets/b2cced65-90fc-494c-9a12-8bae607cea23" />

Patient Sign in Page
<img width="1920" height="1014" alt="Screenshot 7" src="https://github.com/user-attachments/assets/ca838457-b3e9-49e3-9578-e80a7ea6a3b1" />

Patient Profile Entry
<img width="1920" height="1014" alt="Screenshot 8" src="https://github.com/user-attachments/assets/50ba6239-5b22-4120-bdc4-8df1f19e5f93" />

Disease Image Upload
<img width="1920" height="1014" alt="Screenshot 9" src="https://github.com/user-attachments/assets/7e43ff5d-c694-4dfd-9bda-a7e74e5bee87" />

Generated Result
<img width="1920" height="1014" alt="Screenshot 10" src="https://github.com/user-attachments/assets/c8d4d4d6-7574-49a9-b0bb-52fd2af579b8" />

Diagnosis Report
<img width="1920" height="1080" alt="Screenshot 11" src="https://github.com/user-attachments/assets/5e5ebb0b-b905-4438-9d2f-d35f65ac2377" />

## Model Files

The trained model files are available through Google Drive:

[[Google Drive Model Files]](https://drive.google.com/drive/folders/1QIDNDT5-LHy5BJYHq3pNqR__PdQ1WWyJ?usp=drive_link
)

## Installation

git clone <repository-url>

cd Smart_Dermatology_AI

pip install -r requirements.txt

python app.py

## Future Enhancements
- Mobile Application Integration
- Real-Time Camera Diagnosis
- Cloud Deployment
- Additional Skin Disease Categories
- Advanced Explainable AI Features

## Author
Joel Smith J
MCA
