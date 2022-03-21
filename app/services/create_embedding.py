from app.utils.utils import load_embedding_model
import json
import numpy as np
from typing import Dict
from loguru import logger

def create_embeddings(QA_NAME:str, QA: Dict):
    """
    Saving the embedding of the question in the QA pairs

    Args:
        QA_NAME: name of QA provided 
        QA: A dict containing question-answer

    Returns:
        None
    """
    embedding_model = load_embedding_model()
    logger.info("Embedding model loaded")

    QUESTIONS = [key for key, value in QA.items()]
    QA_embeddings = embedding_model.encode(QUESTIONS)
    logger.info("Embeddings created")

    with open('app/false_database/'+'QA_'+QA_NAME+'.json', 'w') as qa_json_file:       # Saving QA pairs
        json.dump(QA, qa_json_file)
    with open('app/false_database/'+'QA_'+QA_NAME+'.npy', 'wb') as qa_npy_file:       # Saving embeddings
        np.save(qa_npy_file, QA_embeddings)
    logger.info("Embeddings saved")