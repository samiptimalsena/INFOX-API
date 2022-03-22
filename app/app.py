from flask import Flask, after_this_request, jsonify, request
from .services.create_embedding import create_embeddings
from .services.infox import infox
import os

app = Flask(__name__)

@app.route("/api/healthz/")
def health():
    """Health check for the api"""

    return "INFOX-api is up and running"

@app.route("/api/createEmbeddings/", methods=["POST"])
def create_embedding():
    """Create and save the embeddings for the QA provided"""

    QA_NAME = request.json.get('qa_name')
    QA = request.json.get("QA")
    create_embeddings(QA_NAME, QA)
    return jsonify({"message": "Embeddings created successfully"})
    
@app.route("/api/app/<string:qa_name>/", methods=['POST'])
def main(qa_name):
    """End2End infox application"""
    
    wav_file = request.files.get("audio_file")
    file_path = "app/false_database/wav_file.wav"
    wav_file.save(file_path)

    @after_this_request
    def remove_wavfile(response):
        os.remove(file_path)
        return response

    output_text = infox(file_path, qa_name)
    return output_text