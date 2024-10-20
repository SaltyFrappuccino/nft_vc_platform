from datetime import date

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Certificate(db.Model):
    __tablename__ = 'certificates'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    issuer = db.Column(db.String(255), nullable=False)
    issued_date = db.Column(db.Date, default=date.today, nullable=False)
    type = db.Column(db.Enum('VC', 'NFT'), default='VC')
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    owner = db.relationship('User', backref='certificates')


class NFTToken(db.Model):
    __tablename__ = 'nft_tokens'

    id = db.Column(db.Integer, primary_key=True)
    certificate_id = db.Column(db.Integer, db.ForeignKey('certificates.id', ondelete='CASCADE'))
    token_hash = db.Column(db.String(255), unique=True, nullable=True)
    abi = db.Column(db.String, nullable=True)  # Новое поле для хранения ABI
    certificate = db.relationship('Certificate', backref='nft_token')
