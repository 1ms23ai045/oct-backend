# src/dl_model.py
import torch
import torch.nn as nn
import torchvision.models as models
from config import NUM_CLASSES, DEVICE

class ChannelAttention(nn.Module):
    """Channel Attention Module for CBAM"""
    def __init__(self, in_channels, reduction=16):
        super().__init__()
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.max_pool = nn.AdaptiveMaxPool2d(1)
        
        self.fc = nn.Sequential(
            nn.Linear(in_channels, in_channels // reduction, bias=False),
            nn.ReLU(inplace=True),
            nn.Linear(in_channels // reduction, in_channels, bias=False)
        )
        self.sigmoid = nn.Sigmoid()
    
    def forward(self, x):
        b, c, _, _ = x.size()
        avg_out = self.fc(self.avg_pool(x).view(b, c))
        max_out = self.fc(self.max_pool(x).view(b, c))
        out = avg_out + max_out
        return self.sigmoid(out).view(b, c, 1, 1)

class SpatialAttention(nn.Module):
    """Spatial Attention Module for CBAM"""
    def __init__(self, kernel_size=7):
        super().__init__()
        self.conv = nn.Conv2d(2, 1, kernel_size, padding=kernel_size//2, bias=False)
        self.sigmoid = nn.Sigmoid()
    
    def forward(self, x):
        avg_out = torch.mean(x, dim=1, keepdim=True)
        max_out, _ = torch.max(x, dim=1, keepdim=True)
        out = torch.cat([avg_out, max_out], dim=1)
        out = self.conv(out)
        return self.sigmoid(out)

class CBAM(nn.Module):
    """Convolutional Block Attention Module"""
    def __init__(self, in_channels, reduction=16, kernel_size=7):
        super().__init__()
        self.channel_attention = ChannelAttention(in_channels, reduction)
        self.spatial_attention = SpatialAttention(kernel_size)
    
    def forward(self, x):
        x = x * self.channel_attention(x)
        x = x * self.spatial_attention(x)
        return x

class EfficientNetWithCBAM(nn.Module):
    """EfficientNet-B0 backbone with CBAM attention"""
    def __init__(self, num_classes=NUM_CLASSES):
        super().__init__()
        self.backbone = models.efficientnet_b0(weights='IMAGENET1K_V1')
        self.feature_dim = self.backbone.classifier[1].in_features
        self.backbone.classifier = nn.Identity()
        self.cbam = CBAM(self.feature_dim)
        self.classifier = nn.Linear(self.feature_dim, num_classes)
    
    def forward(self, x, return_features=False):
        features = self.backbone.features(x)
        features = self.backbone.avgpool(features)
        features = torch.flatten(features, 1)
        features_2d = features.unsqueeze(-1).unsqueeze(-1)
        features_2d = self.cbam(features_2d)
        features = features_2d.flatten(1)
        
        if return_features:
            return features
        
        output = self.classifier(features)
        return output
    
    def extract_features(self, x):
        """Extract features for Random Forest classifier"""
        self.eval()
        with torch.no_grad():
            features = self.backbone.features(x)
            features = self.backbone.avgpool(features)
            features = torch.flatten(features, 1)
            features_2d = features.unsqueeze(-1).unsqueeze(-1)
            features_2d = self.cbam(features_2d)
            features = features_2d.flatten(1)
        return features.cpu().numpy()

def load_model(model_path=None):
    """Load the model from checkpoint"""
    model = EfficientNetWithCBAM()
    model = model.to(DEVICE)
    
    if model_path:
        model.load_state_dict(torch.load(model_path, map_location=DEVICE))
    
    model.eval()
    return model