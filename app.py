from flask import Flask, request, render_template, jsonify
from flask_debugtoolbar import DebugToolbarExtension 
from models import db, connect_db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
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
def user_profile():
    """Display user profile details"""
    return 

# API routes
@app.route("/api/events", methods=["GET"])
def list_events():
    """List all events based on filter"""