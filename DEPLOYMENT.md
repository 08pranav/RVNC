# Deployment Guide for RVNC

This Flask application can be deployed on multiple platforms. Here are the configuration files and instructions:

## Files Added for Deployment

- `vercel.json` - Configuration for Vercel deployment
- `Procfile` - Configuration for Heroku deployment  
- `runtime.txt` - Python version specification
- `api/index.py` - Vercel serverless function entry point

## Platform-Specific Instructions

### 1. Vercel (Recommended)
1. Go to [vercel.com](https://vercel.com)
2. Sign in with GitHub
3. Click "New Project"
4. Import your `RVNC` repository
5. Vercel will auto-detect it as a Python project
6. Deploy!

### 2. Heroku
1. Go to [heroku.com](https://heroku.com)
2. Create a new app
3. Connect to your GitHub repository
4. Enable automatic deploys
5. Deploy!

### 3. Railway
1. Go to [railway.app](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your `RVNC` repository
5. Railway will auto-detect and deploy

### 4. Render
1. Go to [render.com](https://render.com)
2. Click "New Web Service"
3. Connect your GitHub repository
4. Use these settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`

## Troubleshooting Common Issues

### 404 Errors
- Make sure all files are committed and pushed to GitHub
- Check that the deployment platform is looking at the right branch (main)
- Verify that `app.py` is in the root directory

### Import Errors
- Ensure all dependencies are listed in `requirements.txt`
- Check that Python version is compatible (3.11.9 specified in runtime.txt)

### Port Issues
- The app is now configured to use environment PORT variable
- Default fallback is port 5000 for local development

## Local Testing
To test locally before deployment:
```bash
python app.py
```
Then visit http://localhost:5000

## Production vs Development
- Debug mode is disabled in production
- App binds to 0.0.0.0 to accept external connections
- Uses PORT environment variable for platform compatibility