from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):
    """User in Event Finder system"""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True
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

class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.Text,
        nullable=False
    )

    event_url = db.Column(
        db.Text,
        nullable=False
    )

    event_info = db.Column(
        db.Text,
        nullable=True,
        default=""
    )

    # event_venue = db.Column( # venue -> location
    #     db.Text,
    #     nullable=False
    # )


class RSVP(db.Model):
    """Let users RSVP an event"""

    __tablename__ = 'rsvp'


class Likes(db.Model):
    """Let users like an event"""

    __tablename__ = 'likes'
