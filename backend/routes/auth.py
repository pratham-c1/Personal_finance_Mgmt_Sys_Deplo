from flask import Blueprint, request, jsonify, session
import hashlib
from database import execute_one, execute_query

auth_bp = Blueprint('auth', __name__)

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def is_admin():
    return session.get('role') == 'admin'

# ── Login ─────────────────────────────────────────────────────────────────────
@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', '').strip().lower()
    password = data.get('password', '')
    hashed = hash_password(password)
    user = execute_one(
        "SELECT * FROM settings WHERE username = %s AND password_hash = %s LIMIT 1",
        (username, hashed)
    )
    if user:
        session['logged_in'] = True
        session['user_id']   = user['id']
        session['username']  = user['username']
        session['role']      = user['role']
        return jsonify({'success': True, 'user_name': user['user_name'], 'role': user['role']})
    return jsonify({'success': False, 'message': 'Invalid username or password'}), 401

# ── Logout ────────────────────────────────────────────────────────────────────
@auth_bp.route('/api/auth/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True})

# ── Session check ─────────────────────────────────────────────────────────────
@auth_bp.route('/api/auth/check', methods=['GET'])
def check_auth():
    return jsonify({
        'logged_in': session.get('logged_in', False),
        'role':      session.get('role', ''),
        'username':  session.get('username', ''),
    })

# ── Change own password ───────────────────────────────────────────────────────
@auth_bp.route('/api/auth/change-password', methods=['POST'])
def change_password():
    data = request.get_json()
    old_hashed = hash_password(data.get('old_password', ''))
    user = execute_one(
        "SELECT * FROM settings WHERE id = %s AND password_hash = %s",
        (session.get('user_id'), old_hashed)
    )
    if not user:
        return jsonify({'success': False, 'message': 'Old password incorrect'}), 400
    new_hashed = hash_password(data.get('new_password', ''))
    execute_query(
        "UPDATE settings SET password_hash = %s WHERE id = %s",
        (new_hashed, session.get('user_id')), fetch=False
    )
    return jsonify({'success': True, 'message': 'Password changed successfully'})

# ── Admin: list all users ─────────────────────────────────────────────────────
@auth_bp.route('/api/auth/users', methods=['GET'])
def list_users():
    if not is_admin():
        return jsonify({'error': 'Admin only'}), 403
    users = execute_query(
        "SELECT id, username, user_name, role, created_at FROM settings ORDER BY id"
    )
    result = []
    for u in users:
        d = dict(u)
        d['created_at'] = str(d['created_at'])
        result.append(d)
    return jsonify(result)

# ── Admin: create user ────────────────────────────────────────────────────────
@auth_bp.route('/api/auth/users', methods=['POST'])
def create_user():
    if not is_admin():
        return jsonify({'error': 'Admin only'}), 403
    data = request.get_json()
    username  = data.get('username', '').strip().lower()
    user_name = data.get('user_name', '').strip()
    password  = data.get('password', '')
    role      = data.get('role', 'user')
    if not username or not password:
        return jsonify({'success': False, 'message': 'Username and password are required'}), 400
    existing = execute_one("SELECT id FROM settings WHERE username = %s", (username,))
    if existing:
        return jsonify({'success': False, 'message': 'Username already exists'}), 400
    hashed = hash_password(password)
    execute_query(
        "INSERT INTO settings (username, user_name, password_hash, role) VALUES (%s, %s, %s, %s)",
        (username, user_name or username, hashed, role), fetch=False
    )
    return jsonify({'success': True, 'message': f'User {username} created'})

# ── Admin: delete user ────────────────────────────────────────────────────────
@auth_bp.route('/api/auth/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if not is_admin():
        return jsonify({'error': 'Admin only'}), 403
    if user_id == session.get('user_id'):
        return jsonify({'success': False, 'message': 'Cannot delete your own account'}), 400
    execute_query("DELETE FROM settings WHERE id = %s", (user_id,), fetch=False)
    return jsonify({'success': True, 'message': 'User deleted'})

# ── Admin: reset user password ────────────────────────────────────────────────
@auth_bp.route('/api/auth/users/<int:user_id>/reset-password', methods=['POST'])
def reset_password(user_id):
    if not is_admin():
        return jsonify({'error': 'Admin only'}), 403
    data = request.get_json()
    new_hashed = hash_password(data.get('new_password', ''))
    execute_query(
        "UPDATE settings SET password_hash = %s WHERE id = %s",
        (new_hashed, user_id), fetch=False
    )
    return jsonify({'success': True, 'message': 'Password reset'})
