from geopy.geocoders import Nominatim

def reverse_geocode(latitude, longitude):
    """Convert latitude and longitude to conventional address."""
    geolocator = Nominatim(user_agent="event-finder")
    location = geolocator.reverse((latitude, longitude))
    return location.address

