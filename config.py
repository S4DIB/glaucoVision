"""
Configuration file for Glaucoma Detection System
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# Model paths
MODEL_DIR = BASE_DIR / "models"
DENSENET_MODEL_PATH = MODEL_DIR / "densenet121.pth"
LATE_FUSION_MODEL_PATH = MODEL_DIR / "late_fusion_model.pkl"

# API Configuration
API_HOST = "0.0.0.0"
API_PORT = 5000
API_DEBUG = True

# CORS Configuration
CORS_ORIGINS = [
    "http://localhost:3000",  # Next.js dev server
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
]

# Image Processing
IMAGE_SIZE = (299, 299)
IMAGE_NORMALIZATION_MEAN = [0.5, 0.5, 0.5]
IMAGE_NORMALIZATION_STD = [0.5, 0.5, 0.5]

# Clinical Data Configuration
CLINICAL_PARAMETERS = {
    'age': {'min': 0, 'max': 120, 'default': 50},
    'gender': {'options': [0, 1], 'labels': ['Male', 'Female'], 'default': 0},
    'dioptre_1': {'min': -20, 'max': 20, 'default': 0.0, 'step': 0.1},
    'astigmatism': {'min': -10, 'max': 10, 'default': 0.0, 'step': 0.1},
    'phakic': {'options': [0, 1], 'labels': ['Phakic', 'Pseudophakic'], 'default': 0},
    'pneumatic': {'min': 0, 'max': 100, 'default': 0.0, 'step': 0.1},
    'perkins': {'min': 0, 'max': 100, 'default': 0.0, 'step': 0.1},
    'pachymetry': {'min': 200, 'max': 800, 'default': 0.0, 'step': 0.1},
    'axial_length': {'min': 20, 'max': 35, 'default': 0.0, 'step': 0.1},
    'vf_md': {'min': -30, 'max': 5, 'default': 0.0, 'step': 0.1},
}

# AI Model Configuration
MODEL_CONFIG = {
    'device': 'cpu',  # Use 'cuda' if GPU is available
    'num_classes': 2,
    'confidence_threshold': 0.5,
    'clinical_adjustment_factor': 0.05,
}

# File Upload Configuration
UPLOAD_CONFIG = {
    'max_file_size': 10 * 1024 * 1024,  # 10MB
    'allowed_extensions': ['.jpg', '.jpeg', '.png', '.bmp', '.tiff'],
    'upload_folder': BASE_DIR / "uploads",
}

# Logging Configuration
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': BASE_DIR / "logs" / "app.log",
}

# Security Configuration
SECURITY_CONFIG = {
    'max_requests_per_minute': 60,
    'enable_rate_limiting': True,
    'enable_cors': True,
}

# Performance Configuration
PERFORMANCE_CONFIG = {
    'enable_caching': True,
    'cache_ttl': 300,  # 5 minutes
    'max_workers': 4,
}

def create_directories():
    """Create necessary directories if they don't exist."""
    directories = [
        UPLOAD_CONFIG['upload_folder'],
        LOGGING_CONFIG['file'].parent,
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

def validate_config():
    """Validate configuration settings."""
    errors = []
    
    # Check if model files exist
    if not DENSENET_MODEL_PATH.exists():
        errors.append(f"DenseNet model not found at {DENSENET_MODEL_PATH}")
    
    # Check if upload directory is writable
    upload_dir = UPLOAD_CONFIG['upload_folder']
    if not upload_dir.exists():
        try:
            upload_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            errors.append(f"Cannot create upload directory: {e}")
    
    return errors

# Create directories on import
create_directories()
