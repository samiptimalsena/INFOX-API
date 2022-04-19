from flask import Flask, after_this_request, jsonify, request, make_response
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from bson import json_util
import json
import jwt
from loguru import logger

import os

from .services.db import mongo
from .services.create_embedding import create_embeddings
from .services.infox import infox
from .utils.utils import convert, token_required
from .config import Config

app = Flask(__name__)
app.config.from_object(Config)
bcrypt = Bcrypt(app)
CORS(app)
mongo.init_app(app)

@app.route("/api/register/", methods=['POST'])
def register():
    """Register a user"""

    first_name = request.json.get('firstname')
    last_name = request.json.get('lastname')
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')

    user_in_db = mongo.db.users.find_one({'username': username}) or mongo.db.users.find_one({'email': email})
    if user_in_db:
        return jsonify({"message": "User with provided username/email already exists, please try with another one."})

    mongo.db.users.insert_one({'first_name': first_name, 'last_name': last_name, 'username': username, 'email': email, 'password': password})
    return jsonify({"message": "User created"})


@app.route("/api/login/", methods=['POST'])
def login():
    """LogIn the user"""

    username = request.json.get('username')
    user_in_db = mongo.db.users.find_one({'username': username})
    logger.info(user_in_db['password'])

    if not user_in_db:
        return make_response('No user with this username', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

    if user_in_db['password'] == request.json.get("password"):
        token = jwt.encode({'username' : user_in_db['username'], 'email' : user_in_db['email']}, app.config['SECRET_KEY'])
        return jsonify({"Token": token.decode('UTF-8')})

    else:
        return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

@app.route("/api/getUser/", methods=["GET"])
@token_required
def get_user(current_user):
    """Get all the embeddings for the QA provided"""

    data = mongo.db.users.find({"username": current_user['username']})
    list_data = list(data)
    json_data = json_util.dumps(list_data)
    return jsonify({"User Details": json_data})

@app.route("/api/createEmbeddings/", methods=["POST"])
@token_required
def create_embedding(current_user):
    """Create and save the embeddings for the QA provided"""

    username = current_user['username']
    QA_NAME = request.json.get('qa_name')
    QA = request.json.get("QA")
    TITLE = request.json.get("title")
    DESCRIPTION = request.json.get("description")
    IMAGE = request.json.get("image")   

    create_embeddings(username, QA_NAME, QA, TITLE, DESCRIPTION, IMAGE)
    return jsonify({"message": "Embeddings created successfully"})

@app.route("/api/deleteEmbeddings/<string:qa_name>", methods=["POST"])
@token_required
def delete_embedding(current_user, qa_name):
    """Deleting the embedding for chatbot"""
    logger.info(qa_name)
    embedding = mongo.db.embeddings.find({"username": current_user["username"], "QA_NAME": qa_name})
    mongo.db.embeddings.delete_one({"username": current_user["username"], "QA_NAME": qa_name})
    return {"message": "Chatbot successfully deleted"}



@app.route("/api/getEmbeddings/<string:qa_name>/", methods=["GET"])
@token_required
def get_embedding(current_user, qa_name):
    """Get all the embeddings for the QA provided"""

    data = mongo.db.embeddings.find({"username": current_user['username'], "QA_NAME": qa_name})
    list_data = list(data)
    json_data = json_util.dumps(list_data)
    return jsonify({"Embedding data": json_data})

@app.route("/api/getQAs/", methods=["GET"])
@token_required
def get_all_questions(current_user):
    """Get all the embeddings for the users"""

    data = mongo.db.embeddings.find({"username": current_user['username']})
    list_data = list(data)
    json_data = json_util.dumps(list_data)
    return jsonify({"Questions": json_data})

@app.route("/api/app/get_all/")
@token_required
def get_all(current_user):
    data = mongo.db.embeddings.find({"username": current_user['username']})
    list_data = list(data)
    json_data = json_util.dumps(list_data)
    return jsonify(json_data)

@app.route("/api/app/usermode/<string:username>")
def get_all_usermode(username):
    data = mongo.db.embeddings.find({"username": username})
    list_data = list(data)
    json_data = json_util.dumps(list_data)
    return jsonify(json_data)


@app.route("/api/app/<string:qa_name>/", methods=['POST'])
def main(qa_name):
    """End2End infox application"""

    wav_file = request.files.get("audio_file")
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'wav_file.wav')
    wav_file.save(file_path)
    convert(file_path)

    @after_this_request
    def remove_wavfile(response):
        os.remove(file_path)
        return response

    output_text = infox(file_path, qa_name)
    return {"output": output_text}


@app.route("/healthz/")
def health():
    """Health check for the api"""

    return "INFOX-api is up and running"
