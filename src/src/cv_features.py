# src/cv_features.py
import cv2
import numpy as np
from skimage.feature import hog, local_binary_pattern, graycomatrix, graycoprops
from skimage.color import rgb2gray
import torch

def extract_hog_features(image):
    """Histogram of Oriented Gradients - captures edges and shapes"""
    if len(image.shape) == 3 and image.shape[2] == 3:
        gray = rgb2gray(image)
    elif len(image.shape) == 3 and image.shape[0] == 3:
        gray = rgb2gray(np.transpose(image, (1, 2, 0)))
    else:
        gray = image
    
    gray = gray.astype(np.float64)
    
    features = hog(
        gray,
        orientations=9,
        pixels_per_cell=(8, 8),
        cells_per_block=(2, 2),
        visualize=False,
        feature_vector=True
    )
    
    # Reduce dimension
    if len(features) > 200:
        features = features[:200]
    
    return features

def extract_lbp_features(image):
    """Local Binary Patterns - captures texture patterns"""
    if len(image.shape) == 3 and image.shape[2] == 3:
        gray = rgb2gray(image)
    elif len(image.shape) == 3 and image.shape[0] == 3:
        gray = rgb2gray(np.transpose(image, (1, 2, 0)))
    else:
        gray = image
    
    gray = (gray * 255).astype(np.uint8)
    lbp = local_binary_pattern(gray, 8, 1, method='uniform')
    
    n_bins = int(lbp.max() + 1)
    hist, _ = np.histogram(lbp.ravel(), bins=n_bins, range=(0, n_bins))
    hist = hist.astype(np.float32)
    hist /= hist.sum() + 1e-7
    
    return hist

def extract_glcm_features(image):
    """Gray-Level Co-occurrence Matrix - optimized for memory"""
    if len(image.shape) == 3 and image.shape[2] == 3:
        gray = rgb2gray(image)
    elif len(image.shape) == 3 and image.shape[0] == 3:
        gray = rgb2gray(np.transpose(image, (1, 2, 0)))
    else:
        gray = image
    
    # Reduce image size
    gray = cv2.resize(gray, (64, 64))
    gray = (gray * 63).astype(np.uint8)
    
    glcm = graycomatrix(
        gray, 
        distances=[1], 
        angles=[0],
        levels=64,
        symmetric=True, 
        normed=True
    )
    
    features = []
    for prop in ['contrast', 'energy', 'homogeneity']:
        props = graycoprops(glcm, prop)
        features.append(props[0, 0])
    
    return np.array(features)

def extract_all_cv_features(image):
    """Extract all computer vision features and concatenate"""
    if isinstance(image, torch.Tensor):
        image = image.cpu().numpy()
    
    if len(image.shape) == 3 and image.shape[0] in [1, 3]:
        image = np.transpose(image, (1, 2, 0))
    
    if len(image.shape) == 3 and image.shape[2] == 1:
        image = np.repeat(image, 3, axis=2)
    
    if image.max() <= 1 and image.min() >= -1:
        image = (image + 1) / 2
    image = np.clip(image, 0, 1)
    
    hog_feat = extract_hog_features(image)
    lbp_feat = extract_lbp_features(image)
    glcm_feat = extract_glcm_features(image)
    
    all_features = np.concatenate([hog_feat, lbp_feat, glcm_feat])
    
    return all_features