"""
PyTorch Model Loader and Inference Wrapper for 19-Class Skin Disease Classification
Supports EfficientNet-B4 and DenseNet121 ensemble with confidence-aware fusion
"""

import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image
import numpy as np
from typing import Tuple, Dict
import os

# Import efficientnet-pytorch for EfficientNet-B4
from efficientnet_pytorch import EfficientNet

# Class labels for 19-class merged dataset
CLASS_NAMES = [
    "Acne and Rosacea",
    "Bacterial Infection",
    "Contact Dermatitis",
    "Eczema",
    "Fungal Infection",
    "Hair Loss",
    "Herpes & STDs",
    "Infestations & Bites",
    "Lupus and Connective Tissue Disease",
    "Malignant Lesions",
    "Melanoma & Nevi",
    "Nail Disease",
    "Pigmentation Disorders",
    "Psoriasis & Lichen Planus",
    "Seborrheic Keratoses and other Benign Tumors",
    "Systemic Disease",
    "Urticaria",
    "Vascular Disorders",
    "Viral Infection"
]

NUM_CLASSES = len(CLASS_NAMES)

# Device configuration
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Model paths
MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'model')
EFFICIENTNET_PATH = os.path.join(MODEL_DIR, 'efficientnet_b4_19_best.pth')
DENSENET_PATH = os.path.join(MODEL_DIR, 'densenet121_19_best.pth')

# Image preprocessing transforms (same as training)
TRANSFORM = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Import timm for both EfficientNet and DenseNet
import timm


def create_efficientnet_model(num_classes: int = NUM_CLASSES) -> nn.Module:
    """Create EfficientNet-B4 model architecture using timm (matching Kaggle training)"""
    # Create base model
    model = timm.create_model('efficientnet_b4', pretrained=False)
    
    # CRITICAL: The saved model has classifier as Sequential([Dropout, Linear])
    # Not just Linear. This matches the state_dict keys: classifier.1.weight, classifier.1.bias
    # Replace classifier with Sequential to match saved structure
    in_features = model.classifier.in_features
    model.classifier = nn.Sequential(
        nn.Dropout(p=0.2),  # Index 0
        nn.Linear(in_features, num_classes)  # Index 1 - matches classifier.1.weight
    )
    return model


def create_densenet_model(num_classes: int = NUM_CLASSES) -> nn.Module:
    """Create DenseNet121 model architecture using timm (matching Kaggle training)"""
    # Create model exactly as in Kaggle training
    model = timm.create_model('densenet121', pretrained=False)
    # Replace classifier for 19 classes
    model.classifier = nn.Linear(model.classifier.in_features, num_classes)
    return model


class EnsembleModel:
    """Ensemble wrapper for EfficientNet-B4 and DenseNet121"""
    
    def __init__(self, efficientnet_path: str, densenet_path: str, device: torch.device):
        self.device = device
        
        # Load EfficientNet-B4
        print(f"Loading EfficientNet-B4 from {efficientnet_path}...")
        self.efficientnet = create_efficientnet_model()
        self.efficientnet.load_state_dict(torch.load(efficientnet_path, map_location=device), strict=False)
        self.efficientnet.to(device)
        self.efficientnet.eval()
        
        # Load DenseNet121
        print(f"Loading DenseNet121 from {densenet_path}...")
        self.densenet = create_densenet_model()
        self.densenet.load_state_dict(torch.load(densenet_path, map_location=device), strict=False)
        self.densenet.to(device)
        self.densenet.eval()
        
        print(f"Models loaded successfully on {device}")
    
    def predict(self, img_tensor: torch.Tensor) -> Tuple[np.ndarray, np.ndarray]:
        """
        Predict using ensemble with confidence-aware fusion
        
        Args:
            img_tensor: Preprocessed image tensor [1, 3, 224, 224]
        
        Returns:
            predictions: Array of class probabilities [num_classes]
            confidences: Confidence scores from both models
        """
        with torch.no_grad():
            # Get predictions from both models
            eff_logits = self.efficientnet(img_tensor)
            dense_logits = self.densenet(img_tensor)
            
            # Apply softmax to get probabilities
            eff_probs = torch.softmax(eff_logits, dim=1)
            dense_probs = torch.softmax(dense_logits, dim=1)
            
            # Get max confidences
            eff_conf = torch.max(eff_probs, dim=1)[0].item()
            dense_conf = torch.max(dense_probs, dim=1)[0].item()
            
            # Confidence-aware fusion: weight by confidence
            total_conf = eff_conf + dense_conf
            eff_weight = eff_conf / total_conf if total_conf > 0 else 0.5
            dense_weight = dense_conf / total_conf if total_conf > 0 else 0.5
            
            # Weighted average
            ensemble_probs = (eff_weight * eff_probs + dense_weight * dense_probs)
            
            # Convert to numpy
            predictions = ensemble_probs.cpu().numpy()[0]
            confidences = np.array([eff_conf, dense_conf])
            
            return predictions, confidences


# Global ensemble model (lazy loaded)
_ensemble_model = None


def load_ensemble() -> EnsembleModel:
    """Load ensemble model (singleton pattern)"""
    global _ensemble_model
    
    if _ensemble_model is None:
        if not os.path.exists(EFFICIENTNET_PATH):
            raise FileNotFoundError(f"EfficientNet model not found at {EFFICIENTNET_PATH}")
        if not os.path.exists(DENSENET_PATH):
            raise FileNotFoundError(f"DenseNet model not found at {DENSENET_PATH}")
        
        _ensemble_model = EnsembleModel(EFFICIENTNET_PATH, DENSENET_PATH, DEVICE)
    
    return _ensemble_model


def predict_image(image_path: str) -> Dict[str, any]:
    """
    Predict disease class for a single image
    
    Args:
        image_path: Path to image file
    
    Returns:
        Dictionary with prediction results:
        - disease: Predicted disease name
        - confidence: Confidence percentage
        - class_idx: Class index
        - all_probs: All class probabilities
    """
    # Load and preprocess image
    img = Image.open(image_path).convert('RGB')
    img_tensor = TRANSFORM(img).unsqueeze(0).to(DEVICE)
    
    # Get ensemble model
    model = load_ensemble()
    
    # Predict
    predictions, confidences = model.predict(img_tensor)
    
    # Get top prediction
    class_idx = np.argmax(predictions)
    confidence = float(predictions[class_idx] * 100)
    disease = CLASS_NAMES[class_idx]
    
    return {
        'disease': disease,
        'confidence': confidence,
        'class_idx': int(class_idx),
        'all_probs': predictions.tolist(),
        'model_confidences': confidences.tolist()
    }


def preprocess_image_array(img_array: np.ndarray) -> torch.Tensor:
    """
    Preprocess numpy image array for model input
    
    Args:
        img_array: Numpy array in [H, W, C] format (0-255 range)
    
    Returns:
        Preprocessed tensor [1, 3, 224, 224]
    """
    img = Image.fromarray(img_array.astype('uint8'), 'RGB')
    img_tensor = TRANSFORM(img).unsqueeze(0).to(DEVICE)
    return img_tensor


def get_model_for_gradcam() -> nn.Module:
    """
    Get EfficientNet model for GradCAM visualization
    Returns the primary model (EfficientNet-B4)
    """
    model = load_ensemble()
    return model.efficientnet


if __name__ == "__main__":
    # Test loading
    print("Testing model loading...")
    model = load_ensemble()
    print(f"✓ Models loaded successfully")
    print(f"✓ Device: {DEVICE}")
    print(f"✓ Number of classes: {NUM_CLASSES}")
    print(f"✓ Class names: {CLASS_NAMES[:3]}... (showing first 3)")
