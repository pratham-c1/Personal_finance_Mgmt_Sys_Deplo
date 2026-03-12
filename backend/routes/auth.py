from flask import Blueprint, request, jsonify, session
import hashlib
from database import execute_one, execute_query

auth_bp = Blueprint('auth', __name__)

def hash_password(password):
    # Must match MySQL's SHA2(password, 256) output exactly
    # MySQL SHA2 returns lowercase hex — Python hashlib also returns lowercase hex
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    password = data.get('password', '')
    hashed = hash_password(password)
    
    # Debug log to see what we're comparing
    import logging
    logging.getLogger(__name__).info(f"Login attempt — hash: {hashed}")
    
    user = execute_one(
        "SELECT * FROM settings WHERE password_hash = %s LIMIT 1",
        (hashed,)
    )
    if user:
        session['logged_in'] = True
        session['user_id'] = user['id']
        return jsonify({'success': True, 'user_name': user['user_name']})
    return jsonify({'success': False, 'message': 'Invalid password'}), 401

@auth_bp.route('/api/auth/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True})

@auth_bp.route('/api/auth/check', methods=['GET'])
def check_auth():
    return jsonify({'logged_in': session.get('logged_in', False)})

@auth_bp.route('/api/auth/change-password', methods=['POST'])
def change_password():
    data = request.get_json()
    old_pw = data.get('old_password', '')
    new_pw = data.get('new_password', '')
    old_hashed = hash_password(old_pw)
    user = execute_one(
        "SELECT * FROM settings WHERE password_hash = %s",
        (old_hashed,)
    )
    if not user:
        return jsonify({'success': False, 'message': 'Old password incorrect'}), 400
    new_hashed = hash_password(new_pw)
    execute_query(
        "UPDATE settings SET password_hash = %s",
        (new_hashed,), fetch=False
    )
    return jsonify({'success': True, 'message': 'Password changed successfully'})
