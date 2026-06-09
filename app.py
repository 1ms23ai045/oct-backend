from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import os
import base64
from PIL import Image
import io
import numpy as np
from patient_explanations import get_patient_report  # ← ADD THIS

app = Flask(__name__)
CORS(app)

# Clinical explanations dictionary
CLINICAL_EXPLANATIONS = {
    'CNV': 'Choroidal Neovascularization detected...',
    'DME': 'Diabetic Macular Edema detected...',
    'DRUSEN': 'Drusen deposits detected...',
    'NORMAL': 'Normal retina detected...'
}

# Image analysis function (your existing code)
def analyze_image(image_bytes):
    # ... your existing code ...
    pass

# Health check endpoint
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"})

# Prediction endpoint
@app.route('/predict', methods=['POST'])
def predict():
    # ... your existing code ...
    pass

# NEW: Patient report endpoint
@app.route('/report/<diagnosis>', methods=['GET'])
def get_patient_report_endpoint(diagnosis):
    """Get patient-friendly explanation for a diagnosis"""
    confidence = request.args.get('confidence', 85, type=float)
    report = get_patient_report(diagnosis, confidence)
    return jsonify({
        "diagnosis": diagnosis,
        "confidence": confidence,
        "patient_report": report,
        "report_text": report
    })

# Run the app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)