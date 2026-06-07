from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory, current_app
from flask_login import login_required, current_user
import os
import numpy as np
from datetime import datetime
# PyTorch imports
import torch
from PIL import Image
from app.utils.db import get_connection
# Gradient CAM import might need adjustment based on where it is. 
# Assuming I moved it to app.utils.gradcam
# But wait, gradcam.py might rely on other things. I will check imports inside gradcam.py if it fails.
from app.utils.gradcam import make_gradcam_heatmap, save_and_overlay_gradcam
from fpdf import FPDF
import uuid
from app.utils.report_gen import ReportGenerator

main_bp = Blueprint('main', __name__)

# Import PyTorch model loader
from app.utils.pytorch_model import predict_image, load_ensemble

# Load PyTorch ensemble model at startup
try:
    model = load_ensemble()
    print("[SUCCESS] PyTorch ensemble models loaded successfully (EfficientNet-B4 + DenseNet121)")
except Exception as e:
    print(f"Warning: Could not load PyTorch models")
    print(e)
    model = None

# Check if user has completed profile before accessing protected pages
@main_bp.before_request
def check_profile_completion():
    """Redirect to profile completion if user hasn't filled their details"""
    if current_user.is_authenticated:
        # Skip check for these endpoints
        exempt_endpoints = ['main.complete_profile', 'auth.logout', 'static']
        if request.endpoint and any(request.endpoint.startswith(ep) for ep in exempt_endpoints):
            return None
        
        # Check if profile is complete
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT profile_completed FROM users WHERE username = ?", (current_user.username,))
        result = cur.fetchone()
        conn.close()
        
        if result and result[0] == 0:
            return redirect(url_for('main.complete_profile'))
    return None

@main_bp.route('/complete-profile', methods=['GET', 'POST'])
@login_required
def complete_profile():
    """Handle user profile completion"""
    if request.method == 'POST':
        patient_name = request.form.get('patient_name', '').strip()
        gender = request.form.get('gender')
        location = request.form.get('location', '').strip()
        state = request.form.get('state', '').strip()
        country = request.form.get('country', '').strip()
        
        # Validate required fields
        if not all([patient_name, gender, location, state, country]):
            return render_template('user/complete_profile.html', error="All fields are required")
        
        # Update user profile
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE users 
            SET patient_name = ?, gender = ?, location = ?, state = ?, country = ?, profile_completed = 1
            WHERE username = ?
        """, (patient_name, gender, location, state, country, current_user.username))
        conn.commit()
        conn.close()
        
        flash("Profile completed successfully!", "success")
        return redirect(url_for('main.diagnose'))
    
    return render_template('user/complete_profile.html')

# Import disease information for 19-class merged dataset
from app.disease_info import LABELS, DESCRIPTIONS, FIRST_AID

def get_severity(conf):
    if conf >= 85: return "High Risk"
    elif conf >= 60: return "Moderate Risk"
    return "Low Risk"

@main_bp.route('/set_language/<lang>')
def set_language(lang):
    from flask import session
    session['lang'] = lang
    return redirect(request.referrer or url_for('main.index'))

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/home')
@login_required
def home():
    return render_template('user/home.html')

@main_bp.route('/diagnose', methods=['GET', 'POST'])
@login_required
def diagnose():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and model:
            # Save file
            filename = str(uuid.uuid4()) + ".jpg"
            upload_path = os.path.join(current_app.root_path, 'static', 'uploads', filename)
            file.save(upload_path)
            
            # Predict using PyTorch ensemble
            result = predict_image(upload_path)
            disease_pre = result['disease']
            confidence = result['confidence']
            
            # Determine severity based on confidence
            if confidence < 30.0:
                disease = "Uncertain Diagnosis"
                severity = "Low Confidence"
                desc = "The uploaded image does not match any skin condition in our database with sufficient confidence. This could be normal skin or a condition not in our dataset."
                first_aid = "Please consult a certified dermatologist for a proper diagnosis and evaluation."
            else:
                # Valid match
                disease = disease_pre
                if confidence > 85:
                    severity = "High Confidence"
                elif confidence > 60:
                    severity = "Moderate Confidence"
                else:
                    severity = "Low to Moderate Confidence"
                    
                desc = DESCRIPTIONS.get(disease, "No description available.")
                first_aid = FIRST_AID.get(disease, "Consult a dermatologist for specific advice.")
            
            # GradCAM - need to preprocess image for PyTorch
            from app.utils.pytorch_model import TRANSFORM, DEVICE
            img_pil = Image.open(upload_path).convert('RGB')
            img_tensor = TRANSFORM(img_pil).unsqueeze(0).to(DEVICE)
            heatmap = make_gradcam_heatmap(img_tensor, model)
            
            # save_and_overlay_gradcam saves as {original}_gradcam.jpg
            gradcam_full_path = save_and_overlay_gradcam(upload_path, heatmap)
            gradcam_filename = os.path.basename(gradcam_full_path)

            
            # Save DB
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO predictions (username, disease, confidence, timestamp, original_img, gradcam_img) VALUES (?, ?, ?, ?, ?, ?)",
                (current_user.username, disease, confidence, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), filename, gradcam_filename)
            )
            conn.commit()
            conn.close()
            
            return render_template('user/result.html', 
                                   disease=disease, 
                                   confidence=confidence, 
                                   severity=severity,
                                   desc=DESCRIPTIONS.get(disease, "No description available."),
                                   first_aid=FIRST_AID.get(disease, "Consult a dermatologist for specific advice."),
                                   original_img=filename,
                                   gradcam_img=gradcam_filename)

    return render_template('user/diagnose.html')

@main_bp.route('/history')
@login_required
def history():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM predictions WHERE username = ? ORDER BY id DESC", (current_user.username,))
    rows = cur.fetchall()
    conn.close()
    return render_template('user/history.html', history=rows)

@main_bp.route('/report/<filename>')
@login_required
def download_report(filename):
    # Re-generate PDF on the fly or serve if saved.
    # For simplicity, let's just implement a route that triggers PDF gen or serve existing.
    # The original app generated it on the fly. 
    # We can pass params to this route to regenerate? Or save it during diagnosis.
    """Generate and download PDF report for a diagnosis"""
    # Get diagnosis details from database
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.disease, p.confidence, p.original_img, p.gradcam_img,
               u.patient_name, u.gender, u.location, u.state, u.country
        FROM predictions p
        JOIN users u ON p.username = u.username
        WHERE p.username = ? AND (p.original_img = ? OR p.gradcam_img = ?)
        ORDER BY p.id DESC LIMIT 1
    """, (current_user.username, filename, filename))
    result = cur.fetchone()
    conn.close()
    
    if not result:
        flash("Report not found", "error")
        return redirect(url_for('main.history'))
    
    disease, confidence, original_img, gradcam_img, patient_name, gender, location, state, country = result
    
    # Determine severity
    severity = get_severity(confidence)
    
    # Paths to images
    original_path = os.path.join(current_app.root_path, 'static', 'uploads', original_img) if original_img else None
    gradcam_path = os.path.join(current_app.root_path, 'static', 'uploads', gradcam_img) if gradcam_img else None
    
    # Generate PDF
    try:
        report_gen = ReportGenerator(current_app.root_path)
        pdf_filename = f"Skin_Report_{current_user.username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        # Determine output directory
        output_dir = os.path.join(current_app.root_path, 'static', 'reports')
        
        full_pdf_path = report_gen.generate(
            username=current_user.username,
            disease=disease,
            confidence=confidence,
            severity=severity,
            original_img_path=original_path,
            gradcam_img_path=gradcam_path,
            output_filename=pdf_filename,
            patient_name=patient_name,
            gender=gender,
            location=location,
            state=state,
            country=country
        )
        
        return send_from_directory(
            output_dir,
            pdf_filename,
            as_attachment=True
        )
    except Exception as e:
        print(f"Error generating PDF: {e}")
        flash(f"An error occurred while generating the report: {str(e)}", "error")
        return redirect(url_for('main.history'))

@main_bp.route('/generate_pdf', methods=['POST'])
@login_required
def generate_pdf_route():
    # Receive data from form
    disease = request.form.get('disease')
    confidence = float(request.form.get('confidence'))
    severity = request.form.get('severity')
    original_img = request.form.get('original_img')
    gradcam_img = request.form.get('gradcam_img')
    
    # Get user profile data
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT patient_name, gender, location, state, country FROM users WHERE username = ?", 
                (current_user.username,))
    profile = cur.fetchone()
    conn.close()
    
    patient_name, gender, location, state, country = profile if profile else (None, None, None, None, None)
    
    # Paths
    base_path = os.path.join(current_app.root_path, 'static', 'uploads')
    orig_path = os.path.join(base_path, original_img)
    grad_path = os.path.join(base_path, gradcam_img)
    
    # Generate ID
    report_filename = f"report_{uuid.uuid4()}.pdf"
    
    # Generate Report
    try:
        generator = ReportGenerator(current_app.root_path)
        generator.generate(
            username=current_user.username,
            disease=disease,
            confidence=confidence,
            severity=severity,
            original_img_path=orig_path,
            gradcam_img_path=grad_path,
            output_filename=report_filename,
            patient_name=patient_name,
            gender=gender,
            location=location,
            state=state,
            country=country
        )
        
        report_dir = os.path.join(current_app.root_path, 'static', 'reports')
        if not os.path.exists(os.path.join(report_dir, report_filename)):
            flash('Error: Report generation failed (file not found).')
            return redirect(request.referrer or url_for('main.home'))
            
        return send_from_directory(report_dir, report_filename, as_attachment=True)
        
    except Exception as e:
        print(f"PDF Generation Error: {e}")
        flash('An error occurred while generating the report.')
        return redirect(request.referrer or url_for('main.home'))
