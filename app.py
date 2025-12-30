import os
from flask import Flask, render_template, send_from_directory, make_response

# ------------------------------------------------------
# CAMPUSVIBE SERVER ORCHESTRATOR
# Framework: Flask (Python)
# Role: Static Asset Server & SPA Router
# ------------------------------------------------------

# Initialize Flask Application
# template_folder='.': Looks for index.html in the root directory
# static_folder='.': Serves static assets (images, css) from root if needed
app = Flask(__name__, template_folder='.', static_folder='.')

# Security & Performance Headers
@app.after_request
def add_header(response):
    """
    Add headers to both force latest content and ensure security.
    """
    # Prevent caching of the main index file to ensure users always get the latest version
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    
    # Basic Security Headers
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    
    return response

# Main Route
@app.route('/')
def index():
    """
    Serves the main Single Page Application (SPA).
    """
    try:
        # We assume the file is named 'index.html' as per the previous step
        return render_template('index.html')
    except Exception as e:
        # Fallback for debugging if file is missing
        return f"<h1>System Error</h1><p>Critical: index.html not found in server root.</p><p>Error: {str(e)}</p>", 500

# Static File & Fallback Route
@app.route('/<path:path>')
def serve_static(path):
    """
    1. Tries to serve the requested file if it exists physically (e.g., /robots.txt).
    2. If not found, falls back to index.html (essential for SPA routing if you add URL rewriting later).
    """
    if os.path.exists(path):
        return send_from_directory('.', path)
    
    # Fallback to index.html for any unknown paths (Client-side routing handling)
    return render_template('index.html')

# Error Handlers
@app.errorhandler(404)
def not_found(e):
    return render_template('index.html')

@app.errorhandler(500)
def server_error(e):
    return "<h1>500 Internal Server Error</h1>", 500

# Server Entry Point
if __name__ == '__main__':
    # Use PORT environment variable if available (required for deployment like Render/Heroku)
    port = int(os.environ.get('PORT', 5000))
    
    print("------------------------------------------------")
    print(f"🚀 CampusVibe System Online")
    print(f"📡 Listening on http://localhost:{port}")
    print("------------------------------------------------")
    
    # Run the server
    # host='0.0.0.0' makes the server accessible externally
    app.run(host='0.0.0.0', port=port, debug=True)