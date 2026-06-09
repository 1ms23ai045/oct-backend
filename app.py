# app.py
import sys
import os
import io
import numpy as np
import torch
import joblib
from flask import Flask, request, jsonify, render_template
from PIL import Image

# Automatically register current directory and source directories in execution paths
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ROOT_DIR)
sys.path.append(os.path.dirname(ROOT_DIR))

from src.preprocessing import preprocess_image
from src.cv_features import extract_all_cv_features
from src.dl_model import EfficientNetWithCBAM
from config import CLASS_NAMES, DEVICE, MODELS_DIR

# ---------------------------------------------------------
# FLASK CORE INITIALIZATION
# ---------------------------------------------------------
app = Flask(
    __name__,
    static_folder=os.path.join(ROOT_DIR, 'static'),
    template_folder=os.path.join(ROOT_DIR, 'templates')
)

# Runtime safety flag bypass
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

dl_model = None
hybrid_clf = None

def load_models():
    """Pre-loads the PyTorch Attention Backbone and Ensemble Classifier into memory"""
    global dl_model, hybrid_clf
    
    print("="*50)
    print("LOADING CLINICAL INFERENCE SYSTEMS")
    print("="*50)
    
    print("Loading EfficientNet with CBAM...")
    dl_model = EfficientNetWithCBAM()
    model_path = MODELS_DIR / "efficientnet_cbam.pth"
    if model_path.exists():
        dl_model.load_state_dict(torch.load(model_path, map_location=DEVICE))
        print("✓ Deep Learning Attention Model Loaded")
    else:
        print("⚠️ Model file not found, using untrained model")
    
    dl_model = dl_model.to(DEVICE)
    dl_model.eval()
    
    print("Loading Random Forest Classifier...")
    rf_path = MODELS_DIR / "rf_classifier.pkl"
    if rf_path.exists():
        hybrid_clf = joblib.load(rf_path)
        print("✓ Random Forest Fusion Classifier Loaded")
    else:
        print("⚠️ Random Forest file not found")
    
    print("="*50)
    print("✅ All Models Synchronized and Active!")
    print("="*50)

# Load engines upon initialization thread
load_models()

# ---------------------------------------------------------
# CLINICAL EXPLANATIONS
# ---------------------------------------------------------
CLINICAL_EXPLANATIONS = {
    'CNV': '🔴 Choroidal Neovascularization detected. Abnormal blood vessels are growing beneath the retina, characteristic of wet Age-related Macular Degeneration (AMD). Immediate ophthalmologist referral recommended.',
    'DME': '🔴 Diabetic Macular Edema detected. Fluid accumulation in the macula due to diabetic retinopathy. Diabetes management optimization and ophthalmologist referral recommended.',
    'DRUSEN': '🟡 Drusen deposits detected. Yellow deposits beneath the retina - early signs of Age-related Macular Degeneration (AMD). Regular monitoring recommended.',
    'NORMAL': '🟢 Normal retina detected. No significant abnormalities found. Regular routine eye check-ups recommended.'
}

# ---------------------------------------------------------
# HTTP ROUTING ENGINE & API GATEWAY
# ---------------------------------------------------------

@app.route('/')
def serve_index():
    """Serves your index.html frontend interface"""
    try:
        return render_template('index.html')
    except:
        # Fallback if template not found
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>RetinaScan AI</title>
            <style>
                body { font-family: Arial; background: linear-gradient(135deg, #667eea, #764ba2); text-align: center; padding: 50px; }
                .container { background: white; border-radius: 20px; padding: 40px; max-width: 600px; margin: 0 auto; }
                h1 { color: #667eea; }
                .upload-area { border: 2px dashed #ccc; border-radius: 16px; padding: 40px; margin: 20px 0; cursor: pointer; }
                .upload-area:hover { border-color: #667eea; }
                #preview { max-width: 100%; margin-top: 20px; border-radius: 12px; display: none; }
                .btn { background: #667eea; color: white; padding: 12px 30px; border-radius: 30px; border: none; cursor: pointer; }
                .result { margin-top: 20px; padding: 20px; background: #f5f5f5; border-radius: 10px; display: none; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🔬 RetinaScan AI</h1>
                <p>Retinal OCT Image Classification System</p>
                <div class="upload-area" id="uploadArea">
                    <p>📁 Click or Drag & Drop to Upload OCT Image</p>
                    <input type="file" id="fileInput" accept="image/*" style="display:none">
                </div>
                <img id="preview" alt="Preview">
                <button class="btn" id="analyzeBtn" disabled>🔍 Analyze Image</button>
                <div class="result" id="result"></div>
                <p style="margin-top: 20px; font-size: 12px;">⚠️ Educational purposes only. Not for clinical diagnosis.</p>
            </div>
            <script>
                const uploadArea = document.getElementById('uploadArea');
                const fileInput = document.getElementById('fileInput');
                const preview = document.getElementById('preview');
                const analyzeBtn = document.getElementById('analyzeBtn');
                const resultDiv = document.getElementById('result');
                let currentFile = null;
                
                uploadArea.onclick = () => fileInput.click();
                fileInput.onchange = (e) => {
                    if (e.target.files[0]) {
                        currentFile = e.target.files[0];
                        const reader = new FileReader();
                        reader.onload = (event) => {
                            preview.src = event.target.result;
                            preview.style.display = 'block';
                            analyzeBtn.disabled = false;
                        };
                        reader.readAsDataURL(currentFile);
                    }
                };
                
                analyzeBtn.onclick = async () => {
                    if (!currentFile) return;
                    analyzeBtn.disabled = true;
                    analyzeBtn.textContent = '⏳ Analyzing...';
                    const formData = new FormData();
                    formData.append('image', currentFile);
                    try {
                        const response = await fetch('/predict', { method: 'POST', body: formData });
                        const data = await response.json();
                        if (response.ok) {
                            let html = '<h3>📋 Diagnosis Result</h3>';
                            html += `<p><strong>Prediction:</strong> ${data.predicted_class}</p>`;
                            html += `<p><strong>Confidence:</strong> ${data.confidence}%</p>`;
                            html += `<p><strong>Explanation:</strong> ${data.clinical_explanation}</p>`;
                            if (data.top_predictions) {
                                html += '<h4>🎯 Top Predictions</h4><ul>';
                                data.top_predictions.forEach(p => {
                                    html += `<li>${p.class}: ${p.confidence}%</li>`;
                                });
                                html += '</ul>';
                            }
                            resultDiv.innerHTML = html;
                            resultDiv.style.display = 'block';
                        } else {
                            resultDiv.innerHTML = `<p style="color:red">Error: ${data.error}</p>`;
                            resultDiv.style.display = 'block';
                        }
                    } catch (error) {
                        resultDiv.innerHTML = '<p style="color:red">Error: Could not connect to server</p>';
                        resultDiv.style.display = 'block';
                    } finally {
                        analyzeBtn.disabled = false;
                        analyzeBtn.textContent = '🔍 Analyze Image';
                    }
                };
            </script>
        </body>
        </html>
        """

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'models_loaded': dl_model is not None and hybrid_clf is not None,
        'device': DEVICE
    })

@app.route('/predict', methods=['POST'])
def handle_prediction():
    """Handles async fetch requests from your website's Analyze Scan button"""
    global dl_model, hybrid_clf
    
    if 'image' not in request.files:
        return jsonify({'error': 'No image file uploaded'}), 400
        
    uploaded_file = request.files['image']
    
    try:
        # Convert incoming image stream to a NumPy matrix
        in_memory_stream = io.BytesIO(uploaded_file.read())
        pil_image = Image.open(in_memory_stream).convert('RGB')
        numpy_img = np.array(pil_image)
        
        # Execute your custom production processing pipelines
        processed_img = preprocess_image(numpy_img)
        
        # ============================================
        # STEP 1: EXTRACT CV FEATURES (213 dimensions)
        # ============================================
        cv_features = extract_all_cv_features(processed_img)
        
        # ============================================
        # STEP 2: EXTRACT DL FEATURES (1280 dimensions)
        # ============================================
        img_tensor = torch.from_numpy(processed_img).permute(2, 0, 1).unsqueeze(0).float()
        img_tensor = img_tensor.to(DEVICE)
        
        with torch.no_grad():
            dl_features = dl_model.extract_features(img_tensor)
        
        # ============================================
        # STEP 3: FUSE FEATURES (213 + 1280 = 1493 dimensions)
        # ============================================
        cv_features = cv_features.reshape(1, -1)
        dl_features = dl_features.reshape(1, -1)
        fused_features = np.concatenate([cv_features, dl_features], axis=1)
        
        print(f"✅ Feature shape: {fused_features.shape}")  # Should be (1, 1493)
        
        # ============================================
        # STEP 4: CLASSIFY
        # ============================================
        probabilities = hybrid_clf.predict_proba(fused_features)[0]
        predicted_idx = np.argmax(probabilities)
        predicted_class = CLASS_NAMES[predicted_idx]
        top_confidence = round(float(probabilities[predicted_idx]) * 100, 2)
        
        # Format predictions for frontend
        top_predictions = [
            {
                "class": str(CLASS_NAMES[i]), 
                "confidence": round(float(probabilities[i]) * 100, 1)
            }
            for i in range(len(CLASS_NAMES))
        ]
        top_predictions = sorted(top_predictions, key=lambda x: x['confidence'], reverse=True)
        
        return jsonify({
            'predicted_class': predicted_class,
            'confidence': top_confidence,
            'top_predictions': top_predictions[:3],
            'clinical_explanation': CLINICAL_EXPLANATIONS.get(predicted_class, 'Unable to determine diagnosis')
        })
        
    except Exception as e:
        print(f"Prediction Pipeline Crash Event: {str(e)}")
        return jsonify({'error': f"Processing Failure: {str(e)}"}), 500

if __name__ == "__main__":
    print("\n" + "="*50)
    print("🚀 RETINASCAN AI - PRODUCTION SERVER")
    print("="*50)
    print(f"📍 Local URL: http://127.0.0.1:5000")
    print(f"🔬 Health Check: http://127.0.0.1:5000/health")
    print(f"📡 API Endpoint: http://127.0.0.1:5000/predict")
    print("="*50)
    print("\n⚠️  WARNING: Development server. Use a production WSGI server for deployment.")
    print("Press CTRL+C to quit.\n")
    app.run(debug=True, host="127.0.0.1", port=5000)