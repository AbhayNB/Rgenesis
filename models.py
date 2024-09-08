from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    # Additional fields as necessary

    def __repr__(self):
        return f'<User {self.username}>'

class Shop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    # Additional fields as necessary

    def __repr__(self):
        return f'<Shop {self.name}>'

class Ewaste(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    condition = db.Column(db.String(50), nullable=False)
    year_of_manufacture = db.Column(db.Integer, nullable=False)
    estimated_price = db.Column(db.Float, nullable=False)
    # Additional fields as necessary

    def __repr__(self):
        return f'<Ewaste {self.model}>'
