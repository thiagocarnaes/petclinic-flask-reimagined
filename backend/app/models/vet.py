from app import db
from .base import BaseModel
from .specialty import vet_specialties

class Vet(BaseModel):
    __tablename__ = 'vets'
    
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    
    # Many-to-many relationship with specialties
    specialties = db.relationship('Specialty', secondary=vet_specialties, lazy='subquery',
                                backref=db.backref('vets', lazy=True))
    
    def __repr__(self):
        return f'<Vet {self.first_name} {self.last_name}>'
    
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def to_dict(self):
        data = super().to_dict()
        data['full_name'] = self.full_name()
        data['specialties'] = [specialty.to_dict() for specialty in self.specialties]
        return data