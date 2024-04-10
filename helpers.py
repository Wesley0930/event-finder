# Helper logic and functions
import time
import requests

from flask import Flask, jsonify, request
from models import db, User, Event, RSVP, Likes
from datetime import datetime

def serialize_event(event):
    """Serialize an Event SQLAlchemy obj to dictionary"""
    return {
        "id": event.id,
        "event_name": event.event_name,
        "event_url": event.event_url,
        "info": event.info,
        "address": event.address,
        "city": event.city,
        "venue_name": event.venue_name,
        "start_datetime": event.start_datetime.isoformat() if event.start_datetime else None,
        "end_datetime": event.end_datetime.isoformat() if event.end_datetime else None
    }

    
def extract_event_details(response):
    """Extracts event data from JSON object provided by the Ticketmaster API
    Parameters:
    ----------
    Response : JSON object
        The complete JSON object offered by Ticketmaster API
    Returns:
    ----------
    JSON
        A simplified version with extracted details for internal database usage
    """
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
    city = venue_data.get("city")
    city_name = city["name"] if city else ""
    venue_name = venue_data.get("name", "")
    start_dates = response["dates"].get("start")
    end_dates = response["dates"].get("end")
    # start_date = start_dates.get("localDate", None)
    # end_date = end_dates.get("localDate", None)
    # start_time = start_dates.get("localTime", None)
    # end_time = end_dates.get("localTime", None)
    start_datetime_str = start_dates.get("dateTime", "")
    end_datetime_str = end_dates.get("dateTime", "") if end_dates else None
    if start_datetime_str and end_datetime_str:
        start_datetime = datetime.strptime(start_datetime_str, '%Y-%m-%dT%H:%M:%SZ')
        end_datetime = datetime.strptime(end_datetime_str, '%Y-%m-%dT%H:%M:%SZ')
    else:
        start_datetime = None
        end_datetime = None # set to None in case there is no end_datetime (not going to be an issue for start_datetime probably)
    return {
            "id": id, 
            "event_name": event_name,
            "event_url": event_url,
            "info": info,
            "address" : joined_address,
            "city" : city_name, 
            "venue_name": venue_name,
            "start_datetime": start_datetime,
            "end_datetime": end_datetime
        }
