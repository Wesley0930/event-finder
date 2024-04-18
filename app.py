import requests
import helpers
import time

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from config import API_TICKETMASTER_KEY
from flask import Flask, abort, jsonify, g, redirect, request, render_template, session
from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate
from forms import LoginForm, RegisterForm
from models import db, connect_db, User, Event, RSVP, Likes
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import Unauthorized

CURR_USER_KEY = "curr_user"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///event_finder'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app) 
connect_db(app)
migrate = Migrate(app, db) # Flask Migrate

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
    for event_data in events: # can zip events and add_all() instead
        upsert_event(event_data)
    db.session.commit()
    return

def upsert_event(event_data):
    """Create and store SQLAlchemy Event objects for PostgreSQL database
    - OR update an existing event (usually start time changes from TBD)
    """
    # Check if event already exists in database
    ticketmaster_id = event_data["id"]
    existing_event = Event.query.filter_by(ticketmaster_id=ticketmaster_id).first()
    if existing_event:
        # Update the existing event's properties
        existing_event.event_name = event_data["event_name"]
        existing_event.event_url = event_data["event_url"]
        existing_event.info = event_data["info"]
        existing_event.image_url = event_data["image_url"]
        existing_event.address = event_data["address"]
        existing_event.city = event_data["city"]
        existing_event.venue_name = event_data["venue_name"]
        existing_event.start_datetime = event_data["start_datetime"]
        existing_event.end_datetime = event_data["end_datetime"]
    else:
        # Create a new event
        new_event = Event(
            ticketmaster_id=ticketmaster_id,
            event_name=event_data["event_name"],
            event_url=event_data["event_url"],
            info=event_data["info"],
            image_url=event_data["image_url"],
            address=event_data["address"],
            city=event_data["city"],
            venue_name=event_data["venue_name"],
            start_datetime=event_data["start_datetime"],
            end_datetime=event_data["end_datetime"]
        )
        db.session.add(new_event)
    return

def get_and_store_events():
    """Function that scheduler runs to continuously update the database"""
    with app.app_context():
        store_ticketmaster_events()
    return

# Create scheduler instance
scheduler = BackgroundScheduler()
scheduler.configure(timezone="America/New_York")

# get ticketmaster events and save to DB
# scheduler.add_job(get_and_store_events, trigger=IntervalTrigger(hours=1))
scheduler.add_job(get_and_store_events, trigger=IntervalTrigger(minutes=20))
scheduler.start()

@app.route("/api/ticketmaster/events/<event_id>", methods=["GET"])
def get_ticketmaster_event(event_id):
    """Retrieve details of a specific event from Ticketmaster API
    returns JSON of {"id", "event_name", "event_url", "info", "address", "venue_name", "start_datetime", "end_datetime"}
    """
    response = requests.get(f"https://app.ticketmaster.com/discovery/v2/events/{event_id}?apikey={API_TICKETMASTER_KEY}").json()
    return jsonify(helpers.extract_event_details(response))
    
# Homepage
@app.route("/", methods=["GET"])
def homepage():
    """Homepage: redirect to /events"""
    return redirect("/events/events.html")

# User login/logout
@app.before_request
def add_user_to_g():
    """If logged in, add curr user to Flask global"""
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None

def do_login(user):
    """Log in user"""
    session[CURR_USER_KEY] = user.id

def do_logout():
    """Logout user"""
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

# User signup
@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup
    - Create new user and add to PostgreSQL DB. Redirect to events page
    - If form not valid, redisplay form (If there already is a user with that username, show error)
    """
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                image_url=form.image_url.data or User.image_url.default.arg,
            )
            db.session.commit()
        except IntegrityError:
            # flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)
        do_login(user)
        return redirect("/")
    else:
        return render_template('users/signup.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)
        if user:
            do_login(user)
            # flash(f"Hello, {user.username}!", "success")
            return redirect("/")
        # flash("Invalid credentials.", 'danger')
    return render_template('users/login.html', form=form)

@app.route('/logout')
def logout():
    """Handle logout of user."""
    do_logout()
    # flash("You have been successfully logged out.", "success")
    return redirect("/login")
# Event routes

@app.route("/events", methods=["GET"])
def show_all_events():
    """Display an all events page"""
    events = Event.query.all()
    return render_template("/events/events.html", events=events)

@app.route("/event/<int:event_id>")
def show_event(event_id):
    """Show details on specific event"""
    event = Event.query.get_or_404(event_id)
    return render_template("/events/event.html", event=event)

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
    """Fetch list of upcoming events from PostgreSQL database"""
    events = Event.query.all()
    serialized = [helpers.serialize_event(event) for event in events]
    return jsonify(events=serialized, rows=len(serialized))

@app.route("/api/events", methods=["GET"])
def search_database_events():
    """Users can input search filters for events"""
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

@app.route("/api/events/<event_id>", methods=["GET"])
def get_database_event(event_id):
    """Retrieve details of a specific event from PostgreSQL database"""
    event = Event.query.get_or_404(event_id)
    serialized = helpers.serialize_event(event)
    return jsonify(events=serialized)
