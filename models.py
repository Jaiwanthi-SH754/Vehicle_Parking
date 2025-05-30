from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    pin_code = db.Column(db.String(10), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    role = db.Column(db.String(10), nullable=False, default='user') 

    reservations = db.relationship('Reservation', backref='user', cascade='all, delete-orphan')


class ParkingLot(db.Model):
    __tablename__ = 'parking_lots'

    id = db.Column(db.Integer, primary_key=True)
    prime_location_name = db.Column(db.String(100), nullable=False)
    price_per_hour = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    pin_code = db.Column(db.String(10), nullable=False)
    max_spots = db.Column(db.Integer, nullable=False)

    spots = db.relationship('ParkingSpot', backref='lot', cascade='all, delete-orphan')


class ParkingSpot(db.Model):
    __tablename__ = 'parking_spots'

    id = db.Column(db.Integer, primary_key=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lots.id'), nullable=False)
    status = db.Column(db.String(1), nullable=False, default='A')  

    reservation = db.relationship('Reservation', backref='spot', uselist=False, cascade='all, delete-orphan')


class Reservation(db.Model):
    __tablename__ = 'reservations'

    id = db.Column(db.Integer, primary_key=True)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spots.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    parking_timestamp = db.Column(db.DateTime, server_default=db.func.now())
    leaving_timestamp = db.Column(db.DateTime, server_default=db.func.now())

    cost_per_hour = db.Column(db.Float, db.ForeignKey('parking_lots.price_per_hour'),nullable=False)

    def calculate_total_cost(self):
        if self.leaving_timestamp:
            duration = self.leaving_timestamp - self.parking_timestamp
            total_hours = duration.total_seconds() / 3600
            return round(total_hours * self.cost_per_hour, 2)
        return None
