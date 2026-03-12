import sys, os, logging

# ── Resolve paths absolutely — works locally AND on Railway ───────────────────
BACKEND_DIR  = os.path.dirname(os.path.abspath(__file__))        # .../backend/
ROOT_DIR     = os.path.abspath(os.path.join(BACKEND_DIR, '..')) # repo root
FRONTEND_DIR = os.path.join(ROOT_DIR, 'frontend')

if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from flask import Flask, jsonify, send_from_directory, session, redirect
from flask_cors import CORS
from config import Config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

logger.info(f"ROOT_DIR     : {ROOT_DIR}")
logger.info(f"BACKEND_DIR  : {BACKEND_DIR}")
logger.info(f"FRONTEND_DIR : {FRONTEND_DIR}")
logger.info(f"frontend exists: {os.path.exists(FRONTEND_DIR)}")

# ── Flask app ─────────────────────────────────────────────────────────────────
app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path='')
app.secret_key = Config.SECRET_KEY
app.config['SESSION_COOKIE_SECURE']   = Config.SESSION_COOKIE_SECURE
app.config['SESSION_COOKIE_HTTPONLY'] = Config.SESSION_COOKIE_HTTPONLY
app.config['SESSION_COOKIE_SAMESITE'] = Config.SESSION_COOKIE_SAMESITE

CORS(app, supports_credentials=True,
     origins=['http://localhost:5000', 'http://127.0.0.1:5000',
              os.getenv('ALLOWED_ORIGIN', '')])

# ── Blueprints ────────────────────────────────────────────────────────────────
from routes.auth      import auth_bp
from routes.dashboard import dashboard_bp
from routes.income    import income_bp
from routes.expense   import expense_bp
from routes.networth  import networth_bp
from routes.loan      import loan_bp
from routes.share     import share_bp
from routes.bike      import bike_bp
from routes.petrol    import petrol_bp
from routes.baby      import baby_bp
from routes.reports   import reports_bp

for bp in [auth_bp, dashboard_bp, income_bp, expense_bp, networth_bp,
           loan_bp, share_bp, bike_bp, petrol_bp, baby_bp, reports_bp]:
    app.register_blueprint(bp)

# ── Auth middleware ───────────────────────────────────────────────────────────
PUBLIC = {'/api/auth/login', '/api/auth/check', '/api/health', '/api/debug'}

@app.before_request
def require_login():
    from flask import request
    p = request.path
    if (p.startswith('/css/') or p.startswith('/js/')
            or p.endswith('.html') or p in PUBLIC):
        return
    if p.startswith('/api/') and not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401

# ── Page routes ───────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return send_from_directory(FRONTEND_DIR, 'login.html')

@app.route('/<page>.html')
def serve_page(page):
    f = os.path.join(FRONTEND_DIR, f'{page}.html')
    if os.path.exists(f):
        return send_from_directory(FRONTEND_DIR, f'{page}.html')
    return redirect('/')

# ── Health ────────────────────────────────────────────────────────────────────
@app.route('/api/health')
def health():
    return jsonify({'status': 'ok'})

# ── Debug (remove after confirming everything works) ─────────────────────────
@app.route('/api/debug')
def debug():
    info = {
        'root_dir':        ROOT_DIR,
        'frontend_dir':    FRONTEND_DIR,
        'frontend_exists': os.path.exists(FRONTEND_DIR),
        'DB_HOST':         Config.DB_HOST,
        'DB_PORT':         Config.DB_PORT,
        'DB_USER':         Config.DB_USER,
        'DB_NAME':         Config.DB_NAME,
        'DB_PASSWORD_set': bool(Config.DB_PASSWORD),
        'SECRET_KEY_set':  bool(Config.SECRET_KEY),
        'DEBUG':           Config.DEBUG,
    }
    try:
        from database import get_connection
        conn = get_connection()
        conn.cursor().execute('SELECT 1')
        conn.close()
        info['db_connection'] = 'OK'
    except Exception as e:
        info['db_connection'] = f'FAILED: {str(e)}'
    return jsonify(info)

# ── Error handlers ────────────────────────────────────────────────────────────
@app.errorhandler(404)
def not_found(e):
    try:
        return send_from_directory(FRONTEND_DIR, 'login.html')
    except Exception:
        return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(e):
    logger.error(f'500: {e}')
    return jsonify({'error': str(e)}), 500

# ── Local dev only ────────────────────────────────────────────────────────────
if __name__ == '__main__':
    from database import init_pool
    init_pool()
    app.run(host='0.0.0.0', port=Config.PORT, debug=Config.DEBUG)
