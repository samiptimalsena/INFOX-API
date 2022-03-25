import numpy as np
import json
from .db import mongo
from .speech2text import speech2text
from app.utils.utils import cosine_sim
from loguru import logger

def infox( wav_filepath: str, username: str, qa_name: str) -> str:
    """
    Converts the audio file to text and returns the corresponding answer to the most matched question

    Args:
        wav_filepath: filepath of the saved audio file
        username: username of the user
        qa_name: name of QA stored in the database

    Returns:
        Answer of the most matched question
    """
    transcribed_text = speech2text(wav_filepath)
    logger.info(f"Transcribed text: {transcribed_text}")

    data = mongo.db.embeddings.find_one({"username": username, "QA_NAME": qa_name})
    QA = data['QA']
    QA_EMBEDDINGS = np.array(data['QA_embeddings'], dtype=np.float32)

    QUESTIONS = [key for key, value in QA.items()]
    idx = cosine_sim(QA_EMBEDDINGS, transcribed_text)

    question = QUESTIONS[idx]
    logger.info(f"The most matched question is: {question}")
    text = QA[question]
    return text

