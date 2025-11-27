from flask import Flask, request, render_template
import requests
import urllib3

app = Flask(__name__)

# Suppress only the single InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Google Maps API key (replace with your real one)
GOOGLE_API_KEY = 'AIzaSyAaTRi7pCAKGljxTYdd_i8hs1xEksOSSVM'

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/chatbot', methods=['POST'])
def chatbot():
    location = request.form.get('location', '')

    if not location:
        return render_template('index.html', message="Please enter a location.")

    # Step 1: Get coordinates from Google Geocoding API
    geocode_url = f'https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={GOOGLE_API_KEY}'
    try:
        geo_response = requests.get(geocode_url, verify=False, timeout=5)
        geo_data = geo_response.json()
    except requests.exceptions.RequestException as e:
        return render_template('index.html', message=f"Network error: {e}")

    if geo_data.get('status') != 'OK':
        error_message = geo_data.get('error_message', 'Unknown error')
        return render_template('index.html', message=f"Error: {error_message} ({geo_data.get('status')})")

    lat = geo_data['results'][0]['geometry']['location']['lat']
    lon = geo_data['results'][0]['geometry']['location']['lng']

    # Step 2: Get nearby places from Google Places API
    places_url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lon}&radius=5000&key={GOOGLE_API_KEY}'
    try:
        places_response = requests.get(places_url, verify=False, timeout=5)
        places_data = places_response.json()
    except requests.exceptions.RequestException as e:
        return render_template('index.html', message=f"Network error: {e}")

    attractions = []

    for place in places_data.get('results', []):
        attraction = {
            'name': place.get('name'),
            'rating': place.get('rating'),
            'lat': place['geometry']['location']['lat'],
            'lng': place['geometry']['location']['lng'],
            'photo_ref': None
        }

        if place.get('photos'):
            attraction['photo_ref'] = place['photos'][0]['photo_reference']

        attractions.append(attraction)

    if attractions:
        return render_template('index.html', location=location.title(), attractions=attractions, api_key=GOOGLE_API_KEY)
    else:
        return render_template('index.html', message=f"No attractions found for '{location.title()}'.")

if __name__ == '__main__':
    app.run(debug=True)
