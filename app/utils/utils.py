import os
from flask import request, jsonify
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim
import torch
import librosa
import soundfile as sf
from functools import wraps
import jwt
from loguru import logger
from ..services.db import mongo

device = torch.device('cpu')

def load_embedding_model(model_name='all-MiniLM-L6-v2'):
    """Loading embedding model from sentence-transformers"""

    return SentenceTransformer(model_name)

def load_S2T(repo_dir='snakers4/silero-models', model_name='silero_stt'):
    """Loading speech2text model"""

    model, decoder, utils = torch.hub.load(repo_or_dir=repo_dir,
                                       model=model_name,
                                       language='en',
                                       device=device)

    (read_batch, split_into_batches, read_audio, prepare_model_input) = utils
    return model, decoder, read_batch, split_into_batches, prepare_model_input

def cosine_sim(QA_embeddings, text):
    """Finding the cosine similarity between the provided arrays"""

    text_emb = load_embedding_model().encode(text)
    return torch.argmax(cos_sim(QA_embeddings, text_emb))

def convert(inputfile):
    """Converting the sample rate of uploaded audio file"""

    y, sr = librosa.load(inputfile, sr=16000)
    sf.write(inputfile, y, sr)


#decorator for token authorization
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message':'Token is missing'}), 401

        try:
            logger.info('decoding--------------')
            data = jwt.decode(token, os.environ.get('SECRET_KEY'))
            current_user = mongo.db.users.find_one({'username': data['username']})
        except:
            return jsonify({'message': 'Token is invalid'}), 401

        return f(current_user, *args, **kwargs)

    return decorated
