import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://petclinic_user:petclinic_password123@localhost:3306/petclinic'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = os.environ.get('FLASK_DEBUG', '0') == '1'
    
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-string'
    JWT_ACCESS_TOKEN_EXPIRES = 86400  # 24 hours
    
    # CORS Configuration
    CORS_HEADERS = 'Content-Type'
    
    # Swagger Configuration
    SWAGGER = {
        'title': 'PetClinic API',
        'uiversion': 3,
        'version': '1.0.0',
        'description': 'A REST API for PetClinic application',
        'termsOfService': '',
        'contact': {
            'name': 'PetClinic Team',
            'email': 'contact@petclinic.com'
        }
    }

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_ECHO = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}