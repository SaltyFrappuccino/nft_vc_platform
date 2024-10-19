from .. import db

class Company(db.Model):
    __tablename__ = 'companies'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    address = db.Column(db.String(128))
    employees = db.relationship('User', backref='company', lazy=True)
