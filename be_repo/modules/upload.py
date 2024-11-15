"""
This module is responsible for upload user's resume and save it in MongoDB
"""
from flask import jsonify
from modules.parser import parse_resume

ALLOWED_EXTENSIONS = {'pdf'}


# PDF format check
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_parse_resume(request, resume_collection, user_state_collection):
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    user_id = request.form.get('user_id')

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        # Convert PDF to text
        resume_text = parse_resume(file)

        new_resume = {
            "user_id": user_id,
            "resume_text": resume_text
        }
        result = resume_collection.replace_one({"user_id": user_id}, new_resume, upsert=True)

        user_state = {
            "user_id": user_id,
            "state": "0",
            "thread_id": "1"
        }
        user_state_collection.replace_one({"user_id": user_id}, user_state, upsert=True)

        if result.upserted_id:
            resume_id = str(result.upserted_id)
            message = "File successfully uploaded and parsed"
        else:
            resume_id = str(resume_collection.find_one({"user_id": user_id})["_id"])
            message = "Existing resume updated successfully"

        return jsonify({
            "message": message,
            "resume_id": resume_id
        }), 200
    else:
        return jsonify({"error": "Invalid file format, only PDF is allowed"}), 400
