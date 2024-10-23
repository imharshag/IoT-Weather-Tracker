import os
from flask import Flask, render_template, jsonify
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Load the API key from .env file
API_KEY = os.getenv('WEATHER_KEY')
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/weather/<city>')
def get_weather(city):
    try:
        # Debugging: Print the API key to check if it is loaded
        print(f"API_KEY: {API_KEY}")

        url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        # Debugging: Print the raw API response
        print(f"API Response: {data}")

        if response.status_code == 200:
            weather_data = {
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'temp_min': data['main']['temp_min'],
                'temp_max': data['main']['temp_max'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'wind_speed': data['wind']['speed'],
                'wind_deg': data['wind']['deg'],
                'city': data['name'],
                'country': data['sys']['country'],
                'description': data['weather'][0]['description'],
                'cloud_coverage': data['clouds']['all'],
                'icon': data['weather'][0]['icon'],
                'sunrise': data['sys']['sunrise'],
                'sunset': data['sys']['sunset'],
            }
            return jsonify(weather_data)
        else:
            # If the city is not found or there is an error
            return jsonify({'error': 'City not found or API call failed'}), 400

    except Exception as e:
        # Catching general exceptions and returning them for debugging
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
