import requests
from django.contrib.gis.geos import Point
from map.models import WorldBorder
import json
from shapely.geometry import Point, shape

def get_client_ip(request):
    """Extract client IP from request"""
    print("GETTING IP START")
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    print("GETTING IP DONE: ", ip)
    return ip

def get_location_from_ip(ip_address):
    """
    Get lat/long from IP address using ip-api
    Returns dict with 'latitude', 'longitude', or None if failed
    """
    print("GETTING LAT/LONG START")
    try:
        # For testing locally, you might get 127.0.0.1
        if ip_address == '127.0.0.1' or ip_address.startswith('192.168'):
            # Use a default location for local testing (e.g., Houston)
            return {'latitude': 29.7604, 'longitude': -95.3698}

        response = requests.get(f'http://ip-api.com/json/{ip_address}', timeout=5)
        data = response.json()
        print(data)
        print("lat: ", data['lat'], " and long: ", data['lon'], " and type=", type(data['lat']))
        if 'lat' in data and 'lon' in data:
            return {
                'latitude': data['lat'],
                'longitude': data['lon']
            }
    except Exception as e:
        print(f"Error getting location: {e}")


    return None
def get_world_border_from_coordinates(latitude, longitude):
    """
    Find which country contains the given coordinates (accurate)
    """
    point = Point(longitude, latitude)  # Shapely uses (lon, lat) order
    for border in WorldBorder.objects.all():
        try:
            # Load the polygon geometry from stored JSON
            geometry = json.loads(border.mpoly_json)
            polygon = shape(geometry)

            # Check if point is inside this country's borders
            if polygon.contains(point):
                return border
        except:
            continue

    return None  # Not found in any country

def set_user_location_from_ip(user, request):
    """
    Complete function: Get user's location from IP and set their WorldBorder
    """
    ip = get_client_ip(request)
    location = get_location_from_ip(ip)

    if location:
        border = get_world_border_from_coordinates(
            location['latitude'],
            location['longitude']
        )
        if border:
            user.profile.world_border = border
            user.profile.save()
            return True
    return False