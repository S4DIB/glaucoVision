from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
import numpy as np
from PIL import Image
import torch.nn.functional as F
from torchvision import transforms
from torchvision.models import densenet121
import base64
import io
import os
import logging
from config import *

app = Flask(__name__)
CORS(app, origins=CORS_ORIGINS)

# ========================
# 1. Load Image Model (CPU only)
# ========================
def get_densenet121_model():
    model = densenet121(pretrained=False)
    num_ftrs = model.classifier.in_features
    model.classifier = torch.nn.Linear(num_ftrs, 2)
    return model

device = torch.device(MODEL_CONFIG['device'])
img_model = get_densenet121_model()
img_model.load_state_dict(torch.load(DENSENET_MODEL_PATH, map_location=device))
img_model.to(device)
img_model.eval()

# Image Transform
transform_val = transforms.Compose([
    transforms.Resize(IMAGE_SIZE),
    transforms.ToTensor(),
    transforms.Normalize(IMAGE_NORMALIZATION_MEAN, IMAGE_NORMALIZATION_STD)
])

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        # Get image data (base64 encoded)
        image_data = data.get('image')
        if not image_data:
            return jsonify({'error': 'No image provided'}), 400
        
        # Decode base64 image
        image_data = image_data.split(',')[1] if ',' in image_data else image_data
        image_bytes = base64.b64decode(image_data)
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        
        # Get clinical data
        clinical_data = data.get('clinicalData', {})
        age = float(clinical_data.get('age', 50))
        gender = int(clinical_data.get('gender', 0))
        dioptre_1 = float(clinical_data.get('dioptre_1', 0.0))
        astigmatism = float(clinical_data.get('astigmatism', 0.0))
        phakic = int(clinical_data.get('phakic', 0))
        pneumatic = float(clinical_data.get('pneumatic', 0.0))
        perkins = float(clinical_data.get('perkins', 0.0))
        pachymetry = float(clinical_data.get('pachymetry', 0.0))
        axial_length = float(clinical_data.get('axial_length', 0.0))
        vf_md = float(clinical_data.get('vf_md', 0.0))
        
        # Image prediction
        img_tensor = transform_val(img).unsqueeze(0)
        
        with torch.no_grad():
            img_probs = F.softmax(img_model(img_tensor), dim=1).numpy()
            img_pos = img_probs[:, 1]  # positive class (Glaucoma)
        
        # Clinical data processing
        clin_values = np.array([age, gender, dioptre_1, astigmatism, phakic,
                                pneumatic, perkins, pachymetry, axial_length, vf_md], dtype=np.float32)
        clin_norm = (clin_values - clin_values.min()) / (clin_values.max() - clin_values.min() + 1e-6)
        clin_adjust = MODEL_CONFIG['clinical_adjustment_factor'] * (np.sum(clin_norm) / len(clin_norm) - 0.5)
        
        # Late fusion
        fused_prob = np.clip(img_pos + clin_adjust, 0, 1)
        pred_class = int(fused_prob >= MODEL_CONFIG['confidence_threshold'])
        
        # Convert image to base64 for response
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='PNG')
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        
        return jsonify({
            'success': True,
            'prediction': {
                'class': pred_class,
                'class_label': 'Glaucoma' if pred_class == 1 else 'Healthy',
                'probability': float(fused_prob[0]),
                'confidence': float(fused_prob[0]) if pred_class == 1 else float(1 - fused_prob[0])
            },
            'image': f"data:image/png;base64,{img_base64}",
            'clinical_data': clinical_data
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Glaucoma Detection API is running'})

if __name__ == '__main__':
    # Setup logging
    logging.basicConfig(
        level=getattr(logging, LOGGING_CONFIG['level']),
        format=LOGGING_CONFIG['format'],
        handlers=[
            logging.FileHandler(LOGGING_CONFIG['file']),
            logging.StreamHandler()
        ]
    )
    
    # Validate configuration
    config_errors = validate_config()
    if config_errors:
        logging.error("Configuration errors found:")
        for error in config_errors:
            logging.error(f"  - {error}")
        exit(1)
    
    logging.info("Starting Glaucoma Detection API Server...")
    app.run(debug=API_DEBUG, host=API_HOST, port=API_PORT)
