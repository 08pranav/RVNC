"""
Vercel serverless function entry point
"""
import sys
import os

# Add the parent directory to Python path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# Export the Flask app for Vercel
def handler(request):
    return app(request.environ, lambda status, headers: None)

# For Vercel, we need to expose the app
application = app