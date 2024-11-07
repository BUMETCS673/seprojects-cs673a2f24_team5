from flask import Flask, request, jsonify, session
from flask_cors import CORS
from datetime import timedelta

from configs.database import get_resume_database
from modules.evaluator import evaluate_resume, evaluate_resume_with_jd
from modules.upload import upload_parse_resume
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import secrets

# Generate a secure random secret key
secret_key = secrets.token_hex(32)  # Generates a 64-character hexadecimal string

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = secret_key

app.config.update(
    SESSION_COOKIE_SECURE=False,  # Set to True if using HTTPS
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION_LIFETIME=timedelta(minutes=30),
)

GOOGLE_CLIENT_ID = '120137358324-l62fq2hlj9r31evvitg55rcl4rf21udd.apps.googleusercontent.com'

# Test MongoDB connection
try:
    database = get_resume_database()
    resume_collection = database.get_collection("resumes")
    query = {"user_id": "333"}
    resume = resume_collection.find_one(query)
except Exception as e:
    raise Exception("Unable to find the document due to the following error: ", e)


@app.route('/upload', methods=['POST', 'OPTIONS'])
def upload_resume(): 
    if request.method == 'OPTIONS':
        # Allows the preflight request to succeed
        return jsonify({'status': 'OK'}), 200
   
    user_id = request.form.get('user_id')
    if not user_id:
        return jsonify({"error": "No user ID provided."}), 400
    # Vector the resume text
    return upload_parse_resume(request, resume_collection)

@app.route('/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        # Allows the preflight request to succeed
        return jsonify({'status': 'OK'}), 200
    
    token = request.form.get('access_token')
    if not token:
        return jsonify({'status': 'error', 'message': 'ID token is missing'}), 400
    
    try:
        # Verify the token with Google
        idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), GOOGLE_CLIENT_ID)
        
        if idinfo['aud'] != GOOGLE_CLIENT_ID:
            return jsonify({'status': 'error', 'message': 'Token audience mismatch'}), 400

        # Token is valid, extract user information
        userid = idinfo['sub']
        email = idinfo['email']
        name = idinfo.get('name', 'No name available')

        # Create a session or JWT for the user
        session.permanent = True 
        session['user'] = {'userid': userid, 'email': email, 'name': name}

        # Respond with success and optional user data
        return jsonify({'status': 'success', 'email': email, 'name': name}), 200
 
    except ValueError as e:
        # Token verification failed
        print(f"Error verifying token: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Invalid ID token'}), 400

@app.route('/resume_evaluate', methods=['POST', 'OPTIONS'])
def resume_evaluate():
    if request.method == 'OPTIONS':
        # Allows the preflight request to succeed
        return jsonify({'status': 'OK'}), 200
    
    user_id = request.form.get('user_id')
    if not user_id:
        return jsonify({"error": "No user ID provided."}), 400
    
    # Load resume from database
    resume = resume_collection.find_one({"user_id": user_id})
    if not resume:
        return jsonify({"error": "No resume found for this user."}), 404

    resume_text = resume.get('resume_text', '')
    if not resume_text:
        return jsonify({"error": "Resume text is empty."}), 400

    analysis_result = evaluate_resume(resume_text)

    return jsonify({"analysis": analysis_result}), 200


@app.route('/resume_evaluate_with_JD', methods=['POST', 'OPTIONS'])
def resume_evaluate_with_JD():
    if request.method == 'OPTIONS':
        # Allows the preflight request to succeed
        return jsonify({'status': 'OK'}), 200
    
    user_id = request.form.get('user_id')
    jd_text = request.form.get('jd_text')
    if not user_id:
        return jsonify({"error": "No user ID provided."}), 400
    if not jd_text:
        return jsonify({"error": "No job description text provided."}), 400

    # Load resume from database
    resume = resume_collection.find_one({"user_id": user_id})
    if not resume:
        return jsonify({"error": "No resume found for this user."}), 404

    resume_text = resume.get('resume_text', '')
    if not resume_text:
        return jsonify({"error": "Resume text is empty."}), 400

    analysis_result = evaluate_resume_with_jd(resume_text, jd_text)

    return jsonify({"analysis": analysis_result}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
