import json
import os

from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo.mongo_client import MongoClient

from modules.evaluator import evaluate_resume
from modules.upload import upload_parse_resume

app = Flask(__name__)
CORS(app)

config_path = os.path.join('configs', 'config.json')
with open(config_path, 'r') as file:
    config = json.load(file)

# MongoDB
client = MongoClient(config['MONGO_URI'])
try:
    database = client.get_database("resume_db")
    resume_collection = database.get_collection("resumes")
    query = {"user_id": "333"}
    resume = resume_collection.find_one(query)
    print(resume)
except Exception as e:
    raise Exception("Unable to find the document due to the following error: ", e)


@app.route('/upload', methods=['POST'])
def upload_resume():
    user_id = request.form.get('user_id')
    if not user_id:
        return jsonify({"error": "No user ID provided."}), 400
    # Vector the resume text
    return upload_parse_resume(request, resume_collection)


@app.route('/resume_evaluate', methods=['POST'])
def resume_evaluate():
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


if __name__ == '__main__':
    app.run(debug=True)