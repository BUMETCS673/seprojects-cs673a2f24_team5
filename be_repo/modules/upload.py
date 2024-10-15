"""
This module is responsible for upload user's resume and save it in MongoDB
"""
from flask import jsonify
from modules.parser import parse_resume

ALLOWED_EXTENSIONS = {'pdf'}


# PDF format check
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_parse_resume(request, resume_collection):
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
        result = resume_collection.insert_one(new_resume)

        return jsonify({
            "message": "File successfully uploaded and parsed",
            "resume_id": str(result.inserted_id)
        }), 200
    else:
        return jsonify({"error": "Invalid file format, only PDF is allowed"}), 400
