import os
from flask import Flask, render_template, send_from_directory

# ------------------------------------------------------
# RADIUS SERVER ORCHESTRATOR
# Role: Inject Secrets & Serve App (With Safety Fallbacks)
# ------------------------------------------------------

app = Flask(__name__, template_folder='.', static_folder='.')

# FALLBACK CREDENTIALS
# These allow the app to run immediately if Render Env Vars are missing
DEFAULTS = {
    "apiKey": "AIzaSyBI_kfml4u-GdGhRt-DHCX33eWfGeBJej8",
    "authDomain": "campus-vibe-51471.firebaseapp.com",
    "projectId": "campus-vibe-51471",
    "storageBucket": "campus-vibe-51471.firebasestorage.app",
    "messagingSenderId": "204091164414",
    "appId": "1:204091164414:web:7c1d7dbd7eac501f13c7af"
}

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

@app.route('/')
def index():
    # Senior Logic: Try Environment Variables first, fallback to DEFAULTS if missing
    firebase_config = {
        "apiKey": os.environ.get("FIREBASE_API_KEY", DEFAULTS["apiKey"]),
        "authDomain": os.environ.get("FIREBASE_AUTH_DOMAIN", DEFAULTS["authDomain"]),
        "projectId": os.environ.get("FIREBASE_PROJECT_ID", DEFAULTS["projectId"]),
        "storageBucket": os.environ.get("FIREBASE_STORAGE_BUCKET", DEFAULTS["storageBucket"]),
        "messagingSenderId": os.environ.get("FIREBASE_SENDER_ID", DEFAULTS["messagingSenderId"]),
        "appId": os.environ.get("FIREBASE_APP_ID", DEFAULTS["appId"])
    }
    
    return render_template('index.html', config=firebase_config)

@app.route('/<path:path>')
def serve_static(path):
    if os.path.exists(path):
        return send_from_directory('.', path)
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Radius Server Running on Port {port}")
    app.run(host='0.0.0.0', port=port)
