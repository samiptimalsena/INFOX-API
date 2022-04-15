import os

class Config:
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER')
    MONGO_URI = os.environ.get('MONGO_URI')
    SECRET_KEY = os.environ.get('SECRET_KEY')
