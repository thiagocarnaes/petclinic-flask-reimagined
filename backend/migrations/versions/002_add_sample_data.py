"""Add sample data

Revision ID: 002
Revises: 001
Create Date: 2024-01-01 10:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime, date

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Insert pet types
    op.execute("""
        INSERT INTO pet_types (name, created_at, updated_at) VALUES
        ('Cat', NOW(), NOW()),
        ('Dog', NOW(), NOW()),
        ('Lizard', NOW(), NOW()),
        ('Snake', NOW(), NOW()),
        ('Bird', NOW(), NOW()),
        ('Hamster', NOW(), NOW())
    """)
    
    # Insert specialties
    op.execute("""
        INSERT INTO specialties (name, created_at, updated_at) VALUES
        ('Radiology', NOW(), NOW()),
        ('Surgery', NOW(), NOW()),
        ('Dentistry', NOW(), NOW()),
        ('Cardiology', NOW(), NOW()),
        ('Dermatology', NOW(), NOW())
    """)
    
    # Insert vets
    op.execute("""
        INSERT INTO vets (first_name, last_name, created_at, updated_at) VALUES
        ('James', 'Carter', NOW(), NOW()),
        ('Helen', 'Leary', NOW(), NOW()),
        ('Linda', 'Douglas', NOW(), NOW()),
        ('Rafael', 'Ortega', NOW(), NOW()),
        ('Henry', 'Stevens', NOW(), NOW()),
        ('Sharon', 'Jenkins', NOW(), NOW())
    """)
    
    # Insert vet specialties relationships
    op.execute("""
        INSERT INTO vet_specialties (vet_id, specialty_id) VALUES
        (1, 1), -- James Carter: Radiology
        (2, 1), -- Helen Leary: Radiology
        (3, 2), -- Linda Douglas: Surgery
        (3, 3), -- Linda Douglas: Dentistry
        (4, 2), -- Rafael Ortega: Surgery
        (5, 1), -- Henry Stevens: Radiology
        (6, 2)  -- Sharon Jenkins: Surgery
    """)
    
    # Insert owners
    op.execute("""
        INSERT INTO owners (first_name, last_name, address, city, telephone, created_at, updated_at) VALUES
        ('George', 'Franklin', '110 W. Liberty St.', 'Madison', '6085551023', NOW(), NOW()),
        ('Betty', 'Davis', '638 Cardinal Ave.', 'Sun Prairie', '6085551749', NOW(), NOW()),
        ('Eduardo', 'Rodriquez', '2693 Commerce St.', 'McFarland', '6085558763', NOW(), NOW()),
        ('Harold', 'Davis', '563 Friendly St.', 'Windsor', '6085553198', NOW(), NOW()),
        ('Peter', 'McTavish', '2387 S. Fair Way', 'Madison', '6085552765', NOW(), NOW()),
        ('Jean', 'Coleman', '105 N. Lake St.', 'Monona', '6085552654', NOW(), NOW()),
        ('Jeff', 'Black', '1450 Oak Blvd.', 'Monona', '6085555387', NOW(), NOW()),
        ('Maria', 'Escobito', '345 Maple St.', 'Madison', '6085557683', NOW(), NOW()),
        ('David', 'Schroeder', '2749 Blackhawk Trail', 'Madison', '6085559435', NOW(), NOW()),
        ('Carlos', 'Estaban', '2335 Independence La.', 'Waunakee', '6085555487', NOW(), NOW())
    """)
    
    # Insert pets
    op.execute("""
        INSERT INTO pets (name, birth_date, owner_id, type_id, created_at, updated_at) VALUES
        ('Leo', '2010-09-07', 1, 1, NOW(), NOW()),
        ('Basil', '2012-08-06', 2, 6, NOW(), NOW()),
        ('Rosy', '2011-04-17', 3, 2, NOW(), NOW()),
        ('Jewel', '2010-03-07', 3, 2, NOW(), NOW()),
        ('Iggy', '2010-11-30', 4, 3, NOW(), NOW()),
        ('George', '2010-01-20', 5, 4, NOW(), NOW()),
        ('Samantha', '2012-09-04', 6, 1, NOW(), NOW()),
        ('Max', '2012-09-04', 6, 1, NOW(), NOW()),
        ('Lucky', '2011-08-06', 7, 5, NOW(), NOW()),
        ('Mulligan', '2007-02-24', 8, 2, NOW(), NOW()),
        ('Freddy', '2010-03-09', 9, 5, NOW(), NOW()),
        ('Lucky', '2010-06-24', 10, 2, NOW(), NOW()),
        ('Sly', '2012-06-08', 10, 1, NOW(), NOW())
    """)
    
    # Insert visits
    op.execute("""
        INSERT INTO visits (visit_date, description, pet_id, created_at, updated_at) VALUES
        ('2013-01-01', 'rabies shot', 7, NOW(), NOW()),
        ('2013-01-02', 'rabies shot', 8, NOW(), NOW()),
        ('2013-01-03', 'neutered', 8, NOW(), NOW()),
        ('2013-01-04', 'spayed', 7, NOW(), NOW()),
        ('2013-01-01', 'rabies shot', 1, NOW(), NOW()),
        ('2013-01-02', 'rabies shot', 2, NOW(), NOW()),
        ('2013-01-03', 'neutered', 3, NOW(), NOW()),
        ('2013-01-04', 'spayed', 4, NOW(), NOW()),
        ('2013-01-01', 'rabies shot', 5, NOW(), NOW()),
        ('2013-01-02', 'rabies shot', 6, NOW(), NOW()),
        ('2013-01-03', 'neutered', 9, NOW(), NOW()),
        ('2013-01-04', 'spayed', 10, NOW(), NOW()),
        ('2013-01-01', 'rabies shot', 11, NOW(), NOW()),
        ('2013-01-02', 'rabies shot', 12, NOW(), NOW()),
        ('2013-01-03', 'neutered', 13, NOW(), NOW())
    """)


def downgrade() -> None:
    # Remove sample data in reverse order due to foreign key constraints
    op.execute("DELETE FROM visits")
    op.execute("DELETE FROM pets")
    op.execute("DELETE FROM owners")
    op.execute("DELETE FROM vet_specialties")
    op.execute("DELETE FROM vets")
    op.execute("DELETE FROM specialties")
    op.execute("DELETE FROM pet_types")