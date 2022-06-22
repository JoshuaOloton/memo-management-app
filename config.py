import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:next23rd@localhost/memo_management_db'
    DEBUG = True
    UPLOAD_FOLDER = r'static\uploads'
    MEMOS_PER_PAGE = 2

config = {
    'development': DevelopmentConfig,

    'default': DevelopmentConfig
}