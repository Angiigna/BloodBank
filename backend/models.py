from app import db

class Donor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    blood_type = db.Column(db.String(3), nullable=False) 
    contact = db.Column(db.String(100))
    date_donated = db.Column(db.Date)
    volume_donated = db.Column(db.Integer)

    def __repr__(self):
        return f'<Donor {self.name} - {self.blood_type}>'
    
    from flask_marshmallow import Marshmallow
ma = Marshmallow() 

class DonorSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'blood_type', 'contact', 'date_donated', 'volume_ml')

donor_schema = DonorSchema()
donors_schema = DonorSchema(many=True)