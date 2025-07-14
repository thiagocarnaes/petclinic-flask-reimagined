from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from config import config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
jwt = JWTManager()
swagger = Swagger()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    jwt.init_app(app)
    swagger.init_app(app)
    
    # Register blueprints
    from app.controllers.owner_controller import owner_bp
    from app.controllers.pet_controller import pet_bp
    from app.controllers.visit_controller import visit_bp
    from app.controllers.vet_controller import vet_bp
    from app.controllers.specialty_controller import specialty_bp
    from app.controllers.pettype_controller import pettype_bp
    from app.controllers.auth_controller import auth_bp
    
    app.register_blueprint(owner_bp, url_prefix='/api/owners')
    app.register_blueprint(pet_bp, url_prefix='/api/pets')
    app.register_blueprint(visit_bp, url_prefix='/api/visits')
    app.register_blueprint(vet_bp, url_prefix='/api/vets')
    app.register_blueprint(specialty_bp, url_prefix='/api/specialties')
    app.register_blueprint(pettype_bp, url_prefix='/api/pet-types')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return {'status': 'OK', 'message': 'PetClinic API is running'}, 200
    
    return app