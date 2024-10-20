from datetime import date
from flask_sqlalchemy import SQLAlchemy
from database import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    nft_wallet_address = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<User {self.email}>"


class Company(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    address = db.Column(db.String(255), nullable=True)

    employees = db.relationship('CompanyEmployee', backref='company', cascade="all, delete", lazy=True)


class CompanyEmployee(db.Model):
    __tablename__ = 'company_employees'
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    user = db.relationship('User', backref='employment')


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
