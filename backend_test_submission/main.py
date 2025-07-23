# app.py
import os
import random
import string
import datetime
from urllib.parse import urlparse
from utils.log import log as Log
from flask import Flask, request, redirect, jsonify, abort
from flask_cors import CORS


# --- Flask App Configuration ---
app = Flask(__name__)
CORS(app)

# --- In-Memory Storage (Replaces Database) ---
# This dictionary will store our URL mappings.
# Format: { shortcode: { 'original_url': '...', 'created_at': '...', 'expires_at': '...', 'click_count': N } }
url_store = {}



# --- Utility Functions ---
def generate_random_shortcode(length=6):
    """Generates a random alphanumeric shortcode."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

def is_valid_url(url):
    """Basic URL validation."""
    try:
        result = urlparse(url)
        return all([result.scheme in ['http', 'https'], result.netloc])
    except ValueError:
        return False

# --- Error Handling ---
class APIError(Exception):
    """Custom exception for API errors with status code and message."""
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

@app.errorhandler(APIError)
def handle_api_error(error):
    """Handles custom APIError exceptions."""
    Log("backend", "warning", "api-error-handler", "")
    response = jsonify({"status": "error", "message": error.message})
    response.status_code = error.status_code
    return response

@app.errorhandler(404)
def not_found_error(error):
    """Handles 404 Not Found errors."""
    Log("backend", "warning", "api-error-handler", f"404 Not Found: {request.path}")
    response = jsonify({"status": "error", "message": "Resource not found."})
    response.status_code = 404
    return response

@app.errorhandler(500)
def internal_server_error(error):
    """Handles 500 Internal Server Errors."""
    Log("backend", "fatal", "api", f"Internal Server Error: {str(error)}")
    response = jsonify({"status": "error", "message": "An unexpected error occurred. Please try again later."})
    response.status_code = 500
    return response

# --- API Endpoints ---

@app.route('/shorturls', methods=['POST'])
def create_short_url():
    """
    Endpoint to create a new shortened URL.
    Expects JSON body: {"url": "...", "shortcode": "...", "validity": N_minutes}
    """
    data = request.get_json()

    if not data or 'url' not in data:
        Log("backend", "error", "api", "Missing 'url' in request body.")
        raise APIError("Missing 'url' in request body.", 400)

    original_url = data['url']
    custom_shortcode = data.get('shortcode')
    validity_minutes = data.get('validity')

    # 1. Validate Original URL
    if not is_valid_url(original_url):
        Log("backend", "error", "api", f"Invalid URL provided: {original_url}")
        raise APIError("Invalid URL format. Must be a valid http or https URL.", 400)

    # 2. Determine Expiration Time
    expires_at = None
    if validity_minutes is not None:
        try:
            validity_minutes = int(validity_minutes)
            if validity_minutes <= 0:
                Log("backend", "error", "api", f"Invalid validity minutes: {validity_minutes}")
                raise APIError("Validity must be a positive integer.", 400)
            expires_at = datetime.datetime.utcnow() + datetime.timedelta(minutes=validity_minutes)
            Log("backend", "debug", "api", f"Set expiration to {expires_at} based on {validity_minutes} minutes.")
        except ValueError:
            Log("backend", "error", "api", f"Invalid validity format: {validity_minutes}")
            raise APIError("Validity must be an integer representing minutes.", 400)
    else:
        # Default validity: 30 minutes
        expires_at = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        Log("backend", "debug", "api", "Defaulted expiration to 30 minutes.")

    # 3. Handle Shortcode Generation (Custom or Auto-generated)
    shortcode_to_use = None
    if custom_shortcode:
        # Validate custom shortcode format (alphanumeric, reasonable length)
        if not isinstance(custom_shortcode, str) or not custom_shortcode.isalnum() or not (3 <= len(custom_shortcode) <= 10):
            Log("backend", "error", "api", f"Invalid custom shortcode format: {custom_shortcode}")
            raise APIError("Custom shortcode must be alphanumeric and between 3-10 characters long.", 400)
        
        # Check for uniqueness in in-memory store
        if custom_shortcode in url_store:
            Log("backend", "warning", "api", f"Custom shortcode '{custom_shortcode}' already exists.")
            raise APIError(f"Custom shortcode '{custom_shortcode}' is already taken.", 409) # 409 Conflict
        shortcode_to_use = custom_shortcode
        Log("backend", "info", "api", f"Using custom shortcode: {shortcode_to_use}")
    else:
        # Auto-generate unique shortcode
        max_attempts = 5 # Prevent infinite loops in case of high collision rate
        for _ in range(max_attempts):
            generated_code = generate_random_shortcode()
            # Check for uniqueness in in-memory store
            if generated_code not in url_store:
                shortcode_to_use = generated_code
                Log("backend", "debug", "api", f"Generated unique shortcode: {shortcode_to_use}")
                break
        if not shortcode_to_use:
            Log("backend", "fatal", "api", "Failed to generate a unique shortcode after multiple attempts.")
            raise APIError("Could not generate a unique shortcode. Please try again.", 500)

    # 4. Save to In-Memory Store
    url_entry = {
        'original_url': original_url,
        'created_at': datetime.datetime.utcnow(),
        'expires_at': expires_at,
        'click_count': 0
    }
    url_store[shortcode_to_use] = url_entry
    Log("backend", "info", "api", f"URL shortened successfully. Shortcode: {shortcode_to_use}, Original: {original_url}")

    # Construct the response as per the image specification
    shortened_url_full = f"{request.url_root}{shortcode_to_use}"
    return jsonify({
        "shortlink": shortened_url_full,
        "expiry": expires_at.isoformat() + "Z" if expires_at else None # Ensure 'Z' for UTC
    }), 201 # 201 Created

@app.route('/<shortcode>', methods=['GET'])
def redirect_to_original(shortcode):
    """
    Endpoint to redirect to the original URL based on the shortcode.
    """
    if not shortcode:
        Log("backend", "warning", "api", "No shortcode provided in URL path.")
        raise APIError("Shortcode not provided.", 400)

    url_entry = url_store.get(shortcode) # Get from in-memory store

    if not url_entry:
        Log("backend", "warning", "api", f"Shortcode '{shortcode}' not found.")
        raise APIError("Shortened URL not found.", 404)

    # Check expiration
    if url_entry['expires_at'] and url_entry['expires_at'] < datetime.datetime.utcnow():
        Log("backend", "warning", "api", f"Shortcode '{shortcode}' has expired.")
        raise APIError("Shortened URL has expired.", 410) # 410 Gone

    # Increment click count in in-memory store
    url_entry['click_count'] += 1
    Log("backend", "info", "api", f"Redirecting shortcode '{shortcode}' to '{url_entry['original_url']}'. Clicks: {url_entry['click_count']}")

    return redirect(url_entry['original_url'], code=302) # 302 Found for temporary redirect

# --- Run the Application ---
if __name__ == '__main__':
    # To run: python app.py
    # IMPORTANT: All data will be lost when the application restarts as it's in-memory.
    app.run(debug=True, port=5000)
