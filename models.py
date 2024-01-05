from app import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)


class User_details(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    birthday = db.Column(db.Date)
    city = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    user = db.relationship('Users', backref='details', uselist=False)
