

import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "genomeai_secret_key")

    SQLALCHEMY_DATABASE_URI = "sqlite:///genomeai.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = "uploads"

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024