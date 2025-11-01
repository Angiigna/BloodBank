from.import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    first_name = db.Column(db.String(150))
    password = db.Column(db.String(150))
    is_donor = db.Column(db.Boolean, default=False)
    requests = db.relationship('Request', backref='requester')
    donor_profile = db.relationship('Donor', backref='user', uselist=False) 

class Donor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    blood_type = db.Column(db.String(10))
    age = db.Column(db.Integer)
    contact_number = db.Column(db.String(15))

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    requester_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    patient_name = db.Column(db.String(150))
    blood_type_needed = db.Column(db.String(10))
    units_needed = db.Column(db.Integer)
    contact_number = db.Column(db.String(15))
    status = db.Column(db.String(50), default='Pending')