from flask import Flask, request, render_template, jsonify
from flask_debugtoolbar import DebugToolbarExtension 
from models import db, connect_db
import requests

from config import API_TICKETMASTER_KEY



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
    return JSON of { "id", "event_name", "event_url", "info", "address"}

    """
    response = requests.get(f"https://app.ticketmaster.com/discovery/v2/events/{event_id}?apikey={API_TICKETMASTER_KEY}").json()
    id = response["id"]
    event_name = response["name"]
    event_url = response["url"]
    info = response.get("info", "")
    venue_data = response["_embedded"]["venues"][0] # list a single object element
    address = venue_data.get("address", {})
    line1 = address.get("line1", "") # combining 3 potential lines of address
    line2 = address.get("line2", "")
    line3 = address.get("line3", "") 
    joined_address = ', '.join(filter(None, [line1, line2, line3]))
    venue_name = venue_data.get("name", "")
    start_dates = response["dates"].get("start", None)
    end_dates = response["dates"].get("end", None)
    # start_date = start_dates.get("localDate", None)
    # end_date = end_dates.get("localDate", None)
    # start_time = start_dates.get("localTime", None)
    # end_time = end_dates.get("localTime", None)
    start_datetime = start_dates.get("dateTime", None) if start_dates else ""
    end_datetime = end_dates.get("dateTime", None) if end_dates else ""
    return jsonify(
        {
            "id": id, 
            "event_name": event_name,
            "event_url": event_url,
            "info": info,
            "address" : joined_address,
            "venue_name": venue_name, 
            "start_datetime": start_datetime,
            "end_datetime": end_datetime
        }) 
