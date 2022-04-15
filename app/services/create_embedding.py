from app.utils.utils import load_embedding_model
from app.services.db import mongo
from typing import Dict
from loguru import logger
import numpy as np

def create_embeddings(username:str, QA_NAME:str, QA: Dict, TITLE:str, DESCRIPTION:str, IMAGE):
    """
    Saving the embedding of the question in the QA pairs

    Args:
        username: username of the user
        QA_NAME: name of QA provided
        QA: A dict containing question-answer
        TITLE: Title for QA
        DESCRIPTION: Description of the chatbot

    Returns:
        None
    """
    embedding_model = load_embedding_model()
    logger.info("Embedding model loaded")

    QUESTIONS = [key for key, value in QA.items()]
    QA_embeddings = embedding_model.encode(QUESTIONS).tolist()
    
    logger.info("Embeddings created")

    mongo.db.embeddings.insert_one({"username": username,
                                    "QA_NAME": QA_NAME,
                                    "QA": QA,
                                    "QA_embeddings": QA_embeddings,
                                    "Title": TITLE,
                                    "Description": DESCRIPTION,
                                    "Image": IMAGE})

    logger.info("Embeddings saved")
