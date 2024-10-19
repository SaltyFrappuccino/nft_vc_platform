from .. import db

class Certificate(db.Model):
    __tablename__ = 'certificates'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    issuer = db.Column(db.String(128), nullable=False)
    issued_date = db.Column(db.Date, nullable=False)
    type = db.Column(db.String(50), nullable=False)  # 'VC' или 'NFT'
    owner_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    owner = db.relationship('User', backref='certificates')
