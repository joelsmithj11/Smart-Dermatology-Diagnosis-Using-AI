from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.utils.db import get_connection
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
@login_required
def dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('main.home'))
        
    conn = get_connection()
    cur = conn.cursor()
    
    # Get stats
    cur.execute("SELECT COUNT(*) FROM users")
    total_users = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM predictions")
    total_predictions = cur.fetchone()[0]
    
    # Disease Breakdown
    cur.execute("SELECT disease, COUNT(*) as count FROM predictions GROUP BY disease ORDER BY count DESC")
    disease_stats = cur.fetchall()
    total_diseases = len(disease_stats)

    # Gender Breakdown
    cur.execute("""
        SELECT u.gender, COUNT(*) as count 
        FROM predictions p 
        JOIN users u ON p.username = u.username 
        GROUP BY u.gender
    """)
    gender_stats = cur.fetchall()
    
    # Enhanced Recent Logins (Username, Patient Name, Latest Disease)
    cur.execute("""
        SELECT l.username, l.login_time, u.patient_name,
        (SELECT disease FROM predictions p WHERE p.username = l.username ORDER BY id DESC LIMIT 1) as latest_disease
        FROM login_history l
        JOIN users u ON l.username = u.username
        ORDER BY l.id DESC LIMIT 10
    """)
    recent_logins = cur.fetchall()

    # Search Functionality
    search_query = request.args.get('search', '')
    if search_query:
        # If searching, find users matching name or username and get their history
        cur.execute("""
            SELECT p.*, u.patient_name, u.gender
            FROM predictions p
            JOIN users u ON p.username = u.username
            WHERE u.patient_name LIKE ? OR u.username LIKE ?
            ORDER BY p.timestamp DESC
        """, (f'%{search_query}%', f'%{search_query}%'))
        search_results = cur.fetchall()
    else:
        search_results = None

    # Get unverified users
    cur.execute("SELECT * FROM users WHERE is_verified = 0")
    unverified_users = cur.fetchall()

    # Get All Users
    cur.execute("SELECT * FROM users")
    all_users = cur.fetchall()
    
    # Recent Predictions (General)
    cur.execute("SELECT * FROM predictions ORDER BY id DESC LIMIT 50")
    recent_predictions = cur.fetchall()
    
    conn.close()
    
    return render_template('admin/dashboard.html', 
                          admin_mode=True, 
                          total_users=total_users, 
                          total_predictions=total_predictions,
                          total_diseases=total_diseases,
                          disease_stats=disease_stats,
                          gender_stats=gender_stats,
                          recent_logins=recent_logins,
                          search_results=search_results,
                          search_query=search_query,
                          unverified_users=unverified_users,
                          all_users=all_users,
                          recent_predictions=recent_predictions)

@admin_bp.route('/admin/verify/<int:user_id>')
@login_required
def verify_user(user_id):
    if current_user.role != 'admin':
        return redirect(url_for('main.home'))
        
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET is_verified = 1 WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    
    flash('User verified successfully.')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/admin/analytics')
@login_required
def analytics():
    """Admin analytics dashboard with filtering"""
    if current_user.role != 'admin':
        return redirect(url_for('main.home'))
    
    # Get filter parameters from query string
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    country_filter = request.args.get('country', '')
    state_filter = request.args.get('state', '')
    disease_filter = request.args.get('disease', '')
    year_filter = request.args.get('year', '')
    
    conn = get_connection()
    cur = conn.cursor()
    
    # Build dynamic query with filters
    query = """
        SELECT p.*, u.patient_name, u.gender, u.location, u.state, u.country
        FROM predictions p
        JOIN users u ON p.username = u.username
        WHERE 1=1
    """
    params = []
    
    if date_from:
        query += " AND DATE(p.timestamp) >= ?"
        params.append(date_from)
    
    if date_to:
        query += " AND DATE(p.timestamp) <= ?"
        params.append(date_to)
    
    if year_filter:
        query += " AND strftime('%Y', p.timestamp) = ?"
        params.append(year_filter)
    
    if country_filter:
        query += " AND u.country = ?"
        params.append(country_filter)
    
    if state_filter:
        query += " AND u.state = ?"
        params.append(state_filter)
    
    if disease_filter:
        query += " AND p.disease = ?"
        params.append(disease_filter)
    
    query += " ORDER BY p.timestamp DESC"
    
    cur.execute(query, params)
    filtered_predictions = cur.fetchall()
    
    # Get unique values for filter dropdowns
    cur.execute("SELECT DISTINCT country FROM users WHERE country IS NOT NULL ORDER BY country")
    countries = [row[0] for row in cur.fetchall()]
    
    cur.execute("SELECT DISTINCT state FROM users WHERE state IS NOT NULL ORDER BY state")
    states = [row[0] for row in cur.fetchall()]
    
    cur.execute("SELECT DISTINCT disease FROM predictions ORDER BY disease")
    diseases = [row[0] for row in cur.fetchall()]
    
    cur.execute("SELECT DISTINCT strftime('%Y', timestamp) as year FROM predictions ORDER BY year DESC")
    years = [row[0] for row in cur.fetchall()]
    
    # Statistics
    total_filtered = len(filtered_predictions)
    
    conn.close()
    
    return render_template('admin/analytics.html',
                          predictions=filtered_predictions,
                          countries=countries,
                          states=states,
                          diseases=diseases,
                          years=years,
                          total_filtered=total_filtered,
                          filters={
                              'date_from': date_from,
                              'date_to': date_to,
                              'country': country_filter,
                              'state': state_filter,
                              'disease': disease_filter,
                              'year': year_filter
                          })
