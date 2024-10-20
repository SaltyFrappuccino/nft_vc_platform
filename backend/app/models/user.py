from database import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    skills = db.Column(db.JSON, nullable=True)

    def __repr__(self):
        return f"<User {self.email}>"
