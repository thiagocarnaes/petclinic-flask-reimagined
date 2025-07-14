from app import db
from .base import BaseModel

class Owner(BaseModel):
    __tablename__ = 'owners'
    
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    telephone = db.Column(db.String(20), nullable=False)
    
    # Relationship with pets
    pets = db.relationship('Pet', backref='owner', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Owner {self.first_name} {self.last_name}>'
    
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def to_dict(self):
        data = super().to_dict()
        data['full_name'] = self.full_name()
        data['pets'] = [pet.to_dict() for pet in self.pets]
        return data