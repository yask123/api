lat = ''
lon = ''
import json
import webbrowser
from geopy.geocoders import Nominatim
geolocator = Nominatim()
location = geolocator.geocode('Delhi')
location = str(location.latitude)+','+str(location.longitude)
name = 'Haldiram'
url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='+location+'&radius=5000&name='+name+'&key=AIzaSyDAERlVmOrLWdq0pHF5fK3c2cHmCSvy55I'

print url
import requests
r = requests.get(url)
google_result = json.loads(r.text)
print google_result	
