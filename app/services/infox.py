import numpy as np
import json
from .speech2text import speech2text
from app.utils.utils import cosine_sim
from loguru import logger

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

    file_path = 'app/false_database/QA_'
    with open(file_path+qa_name+'.json') as QA_json:
        QA = json.load(QA_json)

    QA_EMBEDDINGS = np.load(file_path+qa_name+'.npy')
    QUESTIONS = [key for key, value in QA.items()]
    idx = cosine_sim(QA_EMBEDDINGS, transcribed_text)

    question = QUESTIONS[idx]
    logger.info(f"The most matched question is: {question}")
    text = QA[question]
    return text
