from flask import Blueprint, render_template, redirect, url_for, request, flash, session, make_response
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils.db import get_connection
from app.models import User
from app.utils.captcha_gen import generate_captcha_image
import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/captcha')
def captcha():
    """Generates a CAPTCHA image and returns it."""
    image_io, text = generate_captcha_image()
    session['captcha'] = text
    response = make_response(image_io.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response

@auth_bp.route('/login-selection')
def login_selection():
    return render_template('login_selection.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        captcha_input = request.form.get('captcha')
        
        # Verify CAPTCHA first
        stored_captcha = session.get('captcha')
        if not stored_captcha or not captcha_input or stored_captcha.upper() != captcha_input.upper():
            flash('Invalid CAPTCHA code. Please try again.')
            return render_template('auth.html')

        # Clear CAPTCHA from session after attempt to prevent reuse
        session.pop('captcha', None)

        user_data = User.get_user_with_password(username)
        
        if user_data:
            # ACTUAL SCHEMA observed: 
            # 0:id, 1:username, 2:mobile, 3:role, 4:password_hash, 5:is_verified, 6:email
            
            role = user_data[3]
            stored_hash = user_data[4]
            is_verified = user_data[5] if len(user_data) > 5 else 1
            email = user_data[6] if len(user_data) > 6 and user_data[6] else user_data[2]
            
            if role == 'admin':
                 flash('Admins must use the Admin Login page.')
                 return redirect(url_for('auth.admin_login'))

            if stored_hash and check_password_hash(stored_hash, password):
                if not is_verified:
                    flash('Your account is pending verification. Please wait for admin approval.')
                    return render_template('auth.html')

                # Authentication Successful -> Login Directly (No OTP)
                user = User(id=user_data[0], username=user_data[1], role=role, email=email, is_verified=is_verified)
                login_user(user)
                
                # Log login history
                conn = get_connection()
                cur = conn.cursor()
                cur.execute("INSERT INTO login_history (username, login_time) VALUES (?, ?)", 
                           (username, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                conn.commit()
                conn.close()
                
                return redirect(url_for('main.home'))
            else:
                flash('Invalid password')
        else:
            flash('User not found')
            
    return render_template('auth.html')

# Removed /verify-otp and /validate-otp routes as they are no longer needed.

@auth_bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user_data = User.get_user_with_password(username)
        
        if user_data:
            # Schema: 0:id, 1:username, 2:mobile, 3:role, 4:pass, 5:is_verified, 6:email
            role = user_data[3] 
            stored_hash = user_data[4]
            is_verified = user_data[5] if len(user_data) > 5 else 1
            
            if role != 'admin':
                flash('Access Denied. Admins only.')
                return render_template('admin/login.html')
            
            if stored_hash and check_password_hash(stored_hash, password):
                # Admin login directly
                # User model handles indices now because we updated it?
                # Actually User __init__ takes args. We need to pass them correctly.
                # User(id, username, role, email, is_verified)
                
                email = user_data[6] if len(user_data) > 6 else user_data[2]
                user = User(id=user_data[0], username=user_data[1], role=role, email=email, is_verified=is_verified)
                login_user(user)
                return redirect(url_for('admin.dashboard'))
            else:
                flash('Invalid password')
        else:
            flash('Admin user not found')
            
    return render_template('admin/login.html')

@auth_bp.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    
    conn = get_connection()
    cur = conn.cursor()
    
    hashed_password = generate_password_hash(password)
    
    try:
        # DB schema has MOBILE as NOT NULL at index 2.
        # We must supply it. We'll supply a dummy value because we are transitioning to Email.
        # Schema: username, mobile, password_hash, role, is_verified, email
        # No, INSERT requires column names usually to be safe.
        cur.execute("INSERT INTO users (username, mobile, email, password_hash, role, is_verified) VALUES (?, ?, ?, ?, ?, ?)",
                   (username, '0000000000', email, hashed_password, 'user', 1))
        conn.commit()
        flash('Registration successful! Please login.')
    except Exception as e:
        print(f"Error: {e}")
        # Improve error message handling
        err_msg = str(e)
        if "UNIQUE constraint failed: users.username" in err_msg:
             flash('Username already exists.')
        elif "UNIQUE constraint failed" in err_msg:
             flash('User already exists.')
        else:
             flash(f'Registration failed: {e}')
    finally:
        conn.close()
        
    return redirect(url_for('auth.login'))

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
