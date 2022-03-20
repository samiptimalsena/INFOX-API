from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim
import torch
from loguru import logger

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

