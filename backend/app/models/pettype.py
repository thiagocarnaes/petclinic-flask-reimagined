from app import db
from .base import BaseModel

class PetType(BaseModel):
    __tablename__ = 'pet_types'
    
    name = db.Column(db.String(80), nullable=False, unique=True)
    
    # Relationship with pets
    pets = db.relationship('Pet', backref='pet_type', lazy=True)
    
    def __repr__(self):
        return f'<PetType {self.name}>'
    
    def to_dict(self):
        data = super().to_dict()
        return data