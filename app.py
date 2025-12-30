import os
from flask import Flask, render_template, send_from_directory

# ------------------------------------------------------
# RADIUS SERVER ORCHESTRATOR
# Role: Inject Secrets & Serve App (Secure Production Mode)
# ------------------------------------------------------

app = Flask(__name__, template_folder='.', static_folder='.')

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

@app.route('/')
def index():
    # 1. Fetch from Environment (Render)
    # CRITICAL: These must be set in Render Dashboard -> Environment
    auth_domain = os.environ.get("FIREBASE_AUTH_DOMAIN", "")
    
    # 2. INTELLIGENT VALIDATION
    # Detect if user accidentally pasted 'appId' into 'authDomain'
    if auth_domain.startswith("1:") or "firebaseapp.com" not in auth_domain:
        print(f"⚠️ CONFIG ERROR: 'FIREBASE_AUTH_DOMAIN' appears invalid ({auth_domain}). Check Render settings.")
        # Set to empty to prevent client-side crash, but auth will fail gracefully until fixed in Dashboard
        auth_domain = ""

    firebase_config = {
        "apiKey": os.environ.get("FIREBASE_API_KEY", ""),
        "authDomain": auth_domain,
        "projectId": os.environ.get("FIREBASE_PROJECT_ID", ""),
        "storageBucket": os.environ.get("FIREBASE_STORAGE_BUCKET", ""),
        "messagingSenderId": os.environ.get("FIREBASE_SENDER_ID", ""),
        "appId": os.environ.get("FIREBASE_APP_ID", "")
    }
    
    # Validation Logging (Server-side)
    if not firebase_config["apiKey"]:
        print("❌ CRITICAL: FIREBASE_API_KEY not found in environment variables.")
    
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
