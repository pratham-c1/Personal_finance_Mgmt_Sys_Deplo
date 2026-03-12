import os
from dotenv import load_dotenv

load_dotenv()  # loads .env if present locally — ignored on Railway (uses Variables tab)

class Config:
    # Database — Railway injects these via Variables tab
    DB_HOST     = os.getenv('DB_HOST', 'localhost')
    DB_PORT     = int(os.getenv('DB_PORT', 3306))
    DB_USER     = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_NAME     = os.getenv('DB_NAME', 'personal_finance')

    # App
    SECRET_KEY  = os.getenv('SECRET_KEY', 'dev-secret-change-in-production')
    DEBUG       = os.getenv('DEBUG', 'False') == 'True'
    PORT        = int(os.getenv('PORT', 5000))

    # Session cookies
    SESSION_COOKIE_SECURE   = not (os.getenv('DEBUG', 'False') == 'True')
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
