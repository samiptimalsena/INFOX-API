from flask import Flask, after_this_request, jsonify, request
from flask_cors import CORS
from flask_bcrypt import Bcrypt

import os

from .services.db import mongo
from .services.create_embedding import create_embeddings
from .services.infox import infox
from .utils.utils import convert
from .config import Config

app = Flask(__name__)
app.config.from_object(Config)
bcrypt = Bcrypt(app)
CORS(app)
mongo.init_app(app)


@app.route("/api/register/", methods=['POST'])
def register():
    """Register a user"""

    first_name = request.json.get("firstname")
    last_name = request.json.get('lastname')
    username = request.json.get('username')
    email = request.json.get('email')
    password = bcrypt.generate_password_hash(request.json.get('password'))

    user_in_db = mongo.db.users.find_one({'username': username}) or mongo.db.users.find_one({'email': email})
    if user_in_db:
        return jsonify({"message": "User with provided username/email already exists, please try with another one."})

    mongo.db.users.insert_one({'first_name': first_name, 'last_name': last_name, 'username': username, 'password': password})
    return jsonify({"message": "User created"})


@app.route("/api/login/", methods=['POST'])
def login():
    """LogIn the user"""

    username = request.json.get('username')
    user_in_db = mongo.db.users.find_one({'username': username})

    if not user_in_db:
        return jsonify({"message": "No user with that username exists"})

    if bcrypt.check_password_hash(user_in_db['password'], request.json.get("password")):
        return jsonify({"Authentication": True})
    else:
        return jsonify({"message": "username and password didn't match"})  


@app.route("/api/createEmbeddings/", methods=["POST"])
def create_embedding():
    """Create and save the embeddings for the QA provided"""

    username = request.json.get("username")
    QA_NAME = request.json.get('qa_name')
    QA = request.json.get("QA")
    create_embeddings(username, QA_NAME, QA)
    return jsonify({"message": "Embeddings created successfully"})
    
@app.route("/api/app/<string:username>/<string:qa_name>/", methods=['POST'])
def main(username, qa_name):
    """End2End infox application"""
    
    wav_file = request.files.get("audio_file")
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'wav_file.wav')
    wav_file.save(file_path)
    convert(file_path)

    @after_this_request
    def remove_wavfile(response):
        os.remove(file_path)
        return response

    output_text = infox(file_path, username,  qa_name)
    return {"output": output_text}
    

@app.route("/healthz/")
def health():
    """Health check for the api"""

    return "INFOX-api is up and running"
