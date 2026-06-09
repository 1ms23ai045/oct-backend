# config.py
import os
from pathlib import Path
import torch

BASE_DIR = Path(__file__).parent

# ============================================
# DATASET CONFIGURATION
# ============================================
# Set USE_OCTMNIST = True for quick start (50MB, auto-download)
# Set USE_OCTMNIST = False for full OCT2017 dataset from Google Drive
USE_OCTMNIST = True

# Google Drive path (only used if USE_OCTMNIST = False)
GOOGLE_DRIVE_PATH = Path("G:/My Drive")
DATASET_PATH = GOOGLE_DRIVE_PATH / "OCT2017" / "OCT2017"

# ============================================
# IMAGE PARAMETERS
# ============================================
IMG_SIZE = 224
BATCH_SIZE = 4  # Reduced for CPU training
NUM_CLASSES = 4
CLASS_NAMES = ['CNV', 'DME', 'DRUSEN', 'NORMAL']

# ============================================
# TRAINING PARAMETERS
# ============================================
RANDOM_SEED = 42

# ============================================
# PATHS
# ============================================
MODELS_DIR = BASE_DIR / "models"
os.makedirs(MODELS_DIR, exist_ok=True)

# ============================================
# DEVICE CONFIGURATION
# ============================================
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

# ============================================
# PRINT CONFIGURATION
# ============================================
print("="*50)
print("CONFIGURATION SUMMARY")
print("="*50)
print(f"Using OCTMNIST: {USE_OCTMNIST}")
print(f"Device: {DEVICE}")
print(f"Batch size: {BATCH_SIZE}")
print(f"Image size: {IMG_SIZE}x{IMG_SIZE}")
print(f"Classes: {CLASS_NAMES}")
print("="*50)