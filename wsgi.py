"""
Root-level WSGI entry point for Railway / Gunicorn.
Place this at the repo root (same level as Procfile).
"""
import sys
import os

# Add backend/ to Python path so all imports work
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))

from app import app

if __name__ == '__main__':
    app.run()
