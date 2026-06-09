# src/dataset_loader.py
import torch
import numpy as np
from torch.utils.data import DataLoader, random_split
from torchvision import transforms

from config import BATCH_SIZE, IMG_SIZE, USE_OCTMNIST, CLASS_NAMES, RANDOM_SEED

if USE_OCTMNIST:
    import medmnist
    from medmnist import OCTMNIST

def load_datasets():
    """Load datasets (OCTMNIST or custom Google Drive)"""
    
    if USE_OCTMNIST:
        return load_octmnist_datasets()
    else:
        return load_googledrive_datasets()

def load_octmnist_datasets():
    """Load OCTMNIST dataset (auto-downloads first time)"""
    
    print("\n" + "="*50)
    print("LOADING OCTMNIST DATASET")
    print("="*50)
    print("Downloading OCTMNIST (50MB)... First time may take a minute")
    
    # Convert grayscale (1-channel) to RGB (3-channel) for EfficientNet
    transform = transforms.Compose([
        transforms.Resize((IMG_SIZE, IMG_SIZE)),
        transforms.Lambda(lambda x: x.convert('RGB')),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
    ])
    
    # Download datasets
    train_dataset = OCTMNIST(split='train', transform=transform, download=True)
    test_dataset = OCTMNIST(split='test', transform=transform, download=True)
    
    # Test the shape
    sample_image, sample_label = train_dataset[0]
    print(f"\n✓ Training samples: {len(train_dataset):,}")
    print(f"✓ Test samples: {len(test_dataset):,}")
    print(f"✓ Image shape: {sample_image.shape}")
    print(f"✓ Classes: {CLASS_NAMES}")
    
    return train_dataset, test_dataset

def load_googledrive_datasets():
    """Load full OCT2017 dataset from Google Drive"""
    
    from pathlib import Path
    from PIL import Image
    from torch.utils.data import Dataset
    from config import DATASET_PATH
    
    class OCT2017Dataset(Dataset):
        def __init__(self, root_dir, split='train', transform=None):
            self.root_dir = Path(root_dir) / split
            self.transform = transform
            self.image_paths = []
            self.labels = []
            
            print(f"Loading {split} set...")
            for label_idx, class_name in enumerate(CLASS_NAMES):
                class_dir = self.root_dir / class_name
                if class_dir.exists():
                    images = list(class_dir.glob("*.jpeg")) + list(class_dir.glob("*.jpg"))
                    self.image_paths.extend(images)
                    self.labels.extend([label_idx] * len(images))
                    print(f"  {class_name}: {len(images)} images")
            
            print(f"Total {split} images: {len(self.image_paths)}")
        
        def __len__(self):
            return len(self.image_paths)
        
        def __getitem__(self, idx):
            img_path = self.image_paths[idx]
            label = self.labels[idx]
            image = Image.open(img_path).convert('RGB')
            if self.transform:
                image = self.transform(image)
            return image, label
    
    print("\n" + "="*50)
    print("LOADING OCT2017 FROM GOOGLE DRIVE")
    print("="*50)
    
    train_transform = transforms.Compose([
        transforms.Resize((IMG_SIZE, IMG_SIZE)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomRotation(10),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                           std=[0.229, 0.224, 0.225])
    ])
    
    val_transform = transforms.Compose([
        transforms.Resize((IMG_SIZE, IMG_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                           std=[0.229, 0.224, 0.225])
    ])
    
    train_dataset = OCT2017Dataset(DATASET_PATH, split='train', transform=train_transform)
    test_dataset = OCT2017Dataset(DATASET_PATH, split='test', transform=val_transform)
    
    return train_dataset, test_dataset

def create_dataloaders(train_dataset, test_dataset, batch_size=BATCH_SIZE):
    """Create train, validation, and test data loaders"""
    
    print("\n" + "="*50)
    print("CREATING DATA LOADERS")
    print("="*50)
    
    # Split training into train/val (80/20)
    train_size = int(0.8 * len(train_dataset))
    val_size = len(train_dataset) - train_size
    
    train_subset, val_subset = random_split(
        train_dataset, 
        [train_size, val_size],
        generator=torch.Generator().manual_seed(RANDOM_SEED)
    )
    
    # Create data loaders
    train_loader = DataLoader(
        train_subset, 
        batch_size=batch_size, 
        shuffle=True, 
        num_workers=0
    )
    
    val_loader = DataLoader(
        val_subset, 
        batch_size=batch_size, 
        shuffle=False, 
        num_workers=0
    )
    
    test_loader = DataLoader(
        test_dataset, 
        batch_size=batch_size, 
        shuffle=False, 
        num_workers=0
    )
    
    print(f"Training batches: {len(train_loader)}")
    print(f"Validation batches: {len(val_loader)}")
    print(f"Test batches: {len(test_loader)}")
    
    return train_loader, val_loader, test_loader

def get_dataset_info():
    """Print dataset information"""
    print("\n" + "="*50)
    print("DATASET INFORMATION")
    print("="*50)
    
    if USE_OCTMNIST:
        print("Dataset: OCTMNIST (MedMNIST)")
        print("Source: Auto-downloads from MedMNIST repository")
        print("Classes: CNV, DME, DRUSEN, NORMAL")
        print("Original size: 28x28 pixels (grayscale)")
        print("Converted to: 224x224 pixels (RGB) for EfficientNet")
        print("Total images: ~109,000")
        print("Storage required: ~50MB")
    else:
        print("Dataset: OCT2017 (Full Dataset)")
        print("Source: Google Drive")
        print("Classes: CNV, DME, DRUSEN, NORMAL")
        print("Total images: ~84,000")
        print("Storage required: ~5.7GB")
    
    print("="*50)