from flask import Flask, render_template, jsonify
import requests
from dotenv import load_dotenv
import os


app = Flask(__name__)

API_KEY = os.getenv('WEATHER_KEY')
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/weather/<city>')
def get_weather(city):
    try:
        # Construct the full URL with the API key, city, and units
        url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"
        
        # Make the API request
        response = requests.get(url)
        
        # Log the full request URL and the response for debugging
        print(f"Request URL: {url}")
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Data: {response.text}")
        
        # Parse the response
        data = response.json()
        
        # If the response status is OK (200)
        if response.status_code == 200:
            # Extract the required weather information
            weather_data = {
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed'],
                'city': data['name']
            }
            # Return the data as a JSON response to the frontend
            return jsonify(weather_data)
        else:
            # If city is not found or there's another error
            return jsonify({'error': 'City not found or API call failed'}), 400

    except Exception as e:
        # Handle any exceptions or errors during the API request
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
