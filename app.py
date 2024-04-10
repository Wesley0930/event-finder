import requests
import helpers
import time

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from config import API_TICKETMASTER_KEY
from flask import Flask, jsonify, request, render_template, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Event, RSVP, Likes
from werkzeug.exceptions import Unauthorized

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///event_finder'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app) 
connect_db(app)

# Create scheduler instance
scheduler = BackgroundScheduler()
scheduler.configure(timezone="America/New_York")

# Ticketmaster API functions
def get_ticketmaster_events():
    """Retrieve a list of upcoming events from Ticketmaster API (no search filter)
    - The default quota is 5000 API calls per day and rate limitation of 5 requests per second.
    - Limited to the first 1000 events (50 pages of 20 events, #0-49)
    Returns Python dictionary of 20 extracted event details
    """
    event_list = []
    # for page_num in range(50):
    for page_num in range(1):
    # parse through 50 pages of events
        time.sleep(0.21)
        response = requests.get(f"https://app.ticketmaster.com/discovery/v2/events?apikey={API_TICKETMASTER_KEY}&locale=*&page={page_num}").json()
        events = response["_embedded"]["events"]
        for event in events:
            # loop through 20 events, extract event data
            event_list.append(helpers.extract_event_details(event))
    return event_list

def store_ticketmaster_events():
    """Store fetched events from Ticketmaster API and store them in the Postgresql database.
    - Calls get_ticketmaster_events() and create_event()    
    """
    events = get_ticketmaster_events()
    for event_data in events:
        create_event(event_data)
    return

def create_event(event_data):
    """Create and store SQLAlchemy Event objects for PostgreSQL database"""
    # Check if event already exists in database
    ticketmaster_id = event_data["id"]
    existing_event = Event.query.filter_by(ticketmaster_id=ticketmaster_id).first()
    if not existing_event:
        new_event = Event(
            ticketmaster_id = event_data["id"], 
            event_name = event_data["event_name"],
            event_url = event_data["event_url"],
            info = event_data["info"],
            address = event_data["address"],
            city = event_data["city"],
            venue_name = event_data["venue_name"],
            start_datetime = event_data["start_datetime"],
            end_datetime = event_data["end_datetime"]
        )
        db.session.add(new_event)
        db.session.commit()
    return

def get_and_store_events():
    """Function that scheduler runs to continuously update the database"""
    with app.app_context():
        store_ticketmaster_events()
    return

# get ticketmaster events and save to DB
# upsert (insert and update), if id exists just update it
scheduler.add_job(get_and_store_events, trigger=IntervalTrigger(hours=1))
scheduler.start()

# @app.route("/api/ticketmaster/events", methods=["GET"])

# @app.route("/api/ticketmaster/events/<event_id>", methods=["GET"])
# def get_ticketmaster_event(event_id):
#     """Retrieve details of a specific event from Ticketmaster API
#     returns JSON of {"id", "event_name", "event_url", "info", "address", "venue_name", "start_datetime", "end_datetime"}
#     """
#     response = requests.get(f"https://app.ticketmaster.com/discovery/v2/events/{event_id}?apikey={API_TICKETMASTER_KEY}").json()
#     return helpers.extract_event_details(response)
    
# Homepage routes 

@app.route("/", methods=["GET"])
def homepage():
    """Display homepage"""
    return render_template("/homepage.html")

# Event routes

@app.route("/events", methods=["GET"])
def show_events():
    """Display an all events page"""
    events = Event.query.all()
    serialized = [helpers.serialize_event(event) for event in events]
    return jsonify(events=serialized)

# User profile routes
@app.route("/user/<username>", methods=["GET"])
def user_profile(username):
    """Display user profile details"""
    if "username" not in session or username != session['username']:
        raise Unauthorized()
    
    user = User.query.get_or_404(username)
    return render_template("/user-details.html", user=user)

@app.route("/user/add", methods=["GET", "POST"])
def create_new_user():
    """Handle new user creation form"""

# Internal API routes

@app.route("/api/events", methods=["GET"])
def list_database_events():
    """Fetch list of upcoming events from PostgreSQL database 
    Users can input search filters for events
    """
    events = Event.query
    # query string parameters for filtering
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    city = request.args.get("city")
    # apply filters
    if start_date:
        events = events.filter(Event.start_datetime >= start_date)
    if end_date:
        events = events.filter(Event.end_datetime <= end_date)
    if city:
        events = events.filter(Event.location.ilike(f"%{city}%"))
    filtered_events = events.all()
    events_data = [
            {
                "id": event.id,
                "event_name": event.event_name,
                "start_datetime": event.start_datetime.isoformat(),
                "end_datetime": event.end_datetime.isoformat(),
                "location": event.location,
            }
            for event in filtered_events
    ]
    return render_template("events.html", events=events_data)

@app.route("/api/events", methods=["GET"])
def search_database_events():
    """"""
    return

@app.route("/api/events/<event_id>", methods=["GET"])
def get_database_event(event_id):
    """Retrieve details of a specific event from PostgreSQL database"""
    event = Event.query.get_or_404(event_id)
    return render_template("event.html", event=event)
