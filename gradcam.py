"""
PyTorch GradCAM Implementation for Skin Disease Model Visualization
Supports EfficientNet-B4 architecture
"""

import torch
import torch.nn.functional as F
import numpy as np
import cv2
from PIL import Image


class GradCAM:
    """Grad-CAM implementation for PyTorch models"""
    
    def __init__(self, model, target_layer):
        self.model = model
        self.target_layer = target_layer
        self.gradients = None
        self.activations = None
        
        # Register hooks
        target_layer.register_forward_hook(self.save_activation)
        target_layer.register_full_backward_hook(self.save_gradient)
    
    def save_activation(self, module, input, output):
        """Hook to save forward pass activations"""
        self.activations = output.detach()
    
    def save_gradient(self, module, grad_input, grad_output):
        """Hook to save backward pass gradients"""
        self.gradients = grad_output[0].detach()
    
    def generate_heatmap(self, input_tensor, class_idx=None):
        """
        Generate GradCAM heatmap for given input
        
        Args:
            input_tensor: Input image tensor [1, 3, H, W]
            class_idx: Target class index (None = use predicted class)
        
        Returns:
            heatmap: Numpy array [H, W] with values in [0, 1]
        """
        self.model.eval()
        
        # Forward pass
        output = self.model(input_tensor)
        
        if class_idx is None:
            class_idx = output.argmax(dim=1).item()
        
        # Backward pass
        self.model.zero_grad()
        class_score = output[:, class_idx]
        class_score.backward()
        
        # Generate heatmap
        gradients = self.gradients
        activations = self.activations
        
        # Global average pooling of gradients
        weights = torch.mean(gradients, dim=(2, 3), keepdim=True)
        
        # Weighted combination of activation maps
        cam = torch.sum(weights * activations, dim=1, keepdim=True)
        cam = F.relu(cam)  # Apply ReLU to focus on positive influence
        
        # Normalize to [0, 1]
        cam = cam.squeeze().cpu().numpy()
        cam = (cam - cam.min()) / (cam.max() - cam.min() + 1e-8)
        
        return cam


def make_gradcam_heatmap(img_tensor, model, target_layer_name='default'):
    """
    Generate GradCAM heatmap for EfficientNet-B4
    
    Args:
        img_tensor: Preprocessed image tensor [1, 3, 224, 224]
        model: EfficientNet-B4 model (from ensemble)
        target_layer_name: Name of target layer (default: last conv layer)
    
    Returns:
        heatmap: Numpy array [H, W] normalized to [0, 1]
    """
    # Get the primary model (EfficientNet-B4) for GradCAM
    from app.utils.pytorch_model import get_model_for_gradcam
    eff_model = get_model_for_gradcam()
    
    # Get the last convolutional layer for timm's efficientnet_b4
    # The structure is: blocks -> conv_head -> (bn2, act2) -> classifier
    # We want conv_head for the last meaningful convolutional features
    if hasattr(eff_model, 'conv_head'):
        target_layer = eff_model.conv_head
    elif hasattr(eff_model, 'blocks'):
        # Fallback: use last block
        target_layer = list(eff_model.blocks)[-1]
    else:
        # Last resort: find last Conv2d layer
        conv_layers = [module for module in eff_model.modules() if isinstance(module, torch.nn.Conv2d)]
        target_layer = conv_layers[-1]
    
    # Create GradCAM
    gradcam = GradCAM(eff_model, target_layer)
    
    # Generate heatmap
    heatmap = gradcam.generate_heatmap(img_tensor)
    
    return heatmap


def save_and_overlay_gradcam(img_path, heatmap):
    """
    Save GradCAM heatmap overlaid on original image
    
    Args:
        img_path: Path to original image
        heatmap: GradCAM heatmap [H, W] in [0, 1] range
    
    Returns:
        out_path: Path to saved overlay image
    """
    # Load original image
    img = cv2.imread(img_path)
    
    # Resize heatmap to match image size
    heatmap_resized = cv2.resize(heatmap, (img.shape[1], img.shape[0]))
    
    # Convert heatmap to uint8 and apply colormap
    heatmap_uint8 = np.uint8(255 * heatmap_resized)
    heatmap_colored = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)
    
    # Overlay heatmap on image
    superimposed = cv2.addWeighted(img, 0.6, heatmap_colored, 0.4, 0)
    
    # Save result
    out_path = img_path.replace(".jpg", "_gradcam.jpg")
    cv2.imwrite(out_path, superimposed)
    
    return out_path
