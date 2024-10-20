from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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
