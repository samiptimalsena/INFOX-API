from dataclasses import dataclass
import numpy as np
import json
from .speech2text import speech2text
from app.utils.utils import cosine_sim
from loguru import logger
from app.extensions import mongo


def infox(wav_filepath: str, qa_name: str) -> str:
    """
    Converts the audio file to text and returns the corresponding answer to the most matched question

    Args:
        wav_filepath: filepath of the saved audio file
        qa_name: name of QA stored in the database

    Returns:
        Answer of the most matched question
    """
    transcribed_text = speech2text(wav_filepath)
    logger.info(f"Transcribed text: {transcribed_text}")

    #Initialise the database
    QA_collection = mongo.db.infox 

    #retrieve from database
    data = QA_collection.find_one({'Name' : qa_name})
    QA = data['QAs']
    logger.info(QA)
    QA_EMBEDDINGS = data['QA_embeddings']

    #Converting nested list retrieved from database to numpy array
    QA_EMBEDDINGS_NP = np.array(QA_EMBEDDINGS, np.float32)
 

    QUESTIONS = [key for key, value in QA.items()]
    idx = cosine_sim(QA_EMBEDDINGS_NP, transcribed_text)

    question = QUESTIONS[idx]
    logger.info(f"The most matched question is: {question}")
    text = QA[question]
    return text

