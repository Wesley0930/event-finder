from flask import Flask, request, render_template, jsonify
from flask_debugtoolbar import DebugToolbarExtension 
from models import db, connect_db
from config import API_TICKETMASTER_KEY

import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///event_finder'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app) 
connect_db(app)

# Homepage routes 

@app.route("/", methods=["GET"])
def homepage():
    """Display homepage"""
    
    return render_template("/homepage.html")


# Event routes

@app.route("/events", methods=["GET"])
def show_events():
    """Display events"""

    return

# User profile routes
@app.route("/user/<int:user_id>", methods=["GET"])
def user_profile(user_id):
    """Display user profile details"""

    return 

@app.route("/user/add", methods=["GET", "POST"])
def create_new_user():
    """Handle new user creation form"""

# Internal API routes

@app.route("/api/events", methods=["GET"])
def list_database_events():
    """Retrieve a list of upcoming events from PostgreSQL database"""

    return

@app.route("/api/events/<event_id>", methods=["GET"])
def get_database_event(event_id):
    """Retrieve details of a specific event from PostgreSQL database"""
    
    return

# Ticketmaster API routes

@app.route("/api/ticketmaster/events", methods=["GET"])
def list_ticketmaster_events():
    """Retrieve a list of upcoming events from Ticketmaster API (no search filter)
    - Limited to the first 5000 events 
    """
    
    return 

@app.route("/api/ticketmaster/events/<event_id>", methods=["GET"])
def get_ticketmaster_event(event_id):
    """Retrieve details of a specific event from Ticketmaster API
    
    """
    response = requests.get(f"https://app.ticketmaster.com/discovery/v2/events/{event_id}?apikey={API_TICKETMASTER_KEY}").json()
    id = response["id"]
    event_name = response["name"]
    event_url = response["url"]
    info = response.get("info", "")
    return jsonify(
        {
            "id": id, 
            "event_name": event_name,
            "event_url": event_url,
            "info": info
        }) 
