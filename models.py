from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User in Event Finder system"""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    image_url = db.Column(
        db.Text,
        default="/static/images/default-pic.png" # default user picture
    )

    first_name = db.Column(
        db.Text,
        nullable=False
    )

    last_name = db.Column(
        db.Text,
        nullable=False
    )

    location = db.Column(
        db.Text,
        nullable=False
    )

    rsvps = db.relationship('RSVP', backref='user', cascade="all, delete-orphan")
    likes = db.relationship('Likes', backref='user', cascade="all, delete-orphan")

class Event(db.Model):
    __tablename__ = "events"

    id = db.Column( # id*
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    event_name = db.Column( # name
        db.Text,
        nullable=False
    )

    event_url = db.Column( # url
        db.Text,
        nullable=False
    )

    info = db.Column( # info
        db.Text,
        nullable=True,
        default=""
    )

    venue_name = db.Column( # venue -> location (maybe add venue model)
        db.Text,
        nullable=False
    )

    address = db.Column( # _embedded -> venues -> address
        db.Text,
        nullable=False
    )

    # start and end times in datetime format
    start_time = db.Column( # dates -> start 
        db.DateTime,
        nullable=False
    )

    end_time = db.Column( # dates -> end
        db.DateTime,
        nullable=True
    )

    rsvps = db.relationship('RSVP', backref='event', cascade="all, delete-orphan")
    likes = db.relationship('Likes', backref='event', cascade="all, delete-orphan")
    

class RSVP(db.Model):
    """Let users RSVP an event"""

    __tablename__ = 'rsvps'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id', ondelete='CASCADE'), nullable=False)
    
class Likes(db.Model):
    """Let users like an event"""

    __tablename__ = 'likes'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id', ondelete='CASCADE'), nullable=False)