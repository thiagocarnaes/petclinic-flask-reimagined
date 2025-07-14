from app import db
from .base import BaseModel

# Association table for many-to-many relationship between vets and specialties
vet_specialties = db.Table('vet_specialties',
    db.Column('vet_id', db.Integer, db.ForeignKey('vets.id'), primary_key=True),
    db.Column('specialty_id', db.Integer, db.ForeignKey('specialties.id'), primary_key=True)
)

class Specialty(BaseModel):
    __tablename__ = 'specialties'
    
    name = db.Column(db.String(80), nullable=False, unique=True)
    
    def __repr__(self):
        return f'<Specialty {self.name}>'
    
    def to_dict(self):
        data = super().to_dict()
        return data