import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import firebase_admin
from firebase_admin import credentials, auth
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your_default_secret_key')

# Initialize Firebase Admin SDK
cred = credentials.Certificate('firebase-service-account.json')
firebase_admin.initialize_app(cred)

WEATHER_KEY = os.getenv('WEATHER_KEY')
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

# Firebase Authentication REST API endpoint
FIREBASE_AUTH_URL = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=" + os.getenv('FIREBASE_API_KEY')

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.create_user(email=email, password=password)
            flash('Registration successful. Please log in.')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Error: {str(e)}')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        headers = {
            "Content-Type": "application/json"
        }
        
        data = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }

        # Send request to Firebase Authentication REST API
        response = requests.post(FIREBASE_AUTH_URL, json=data, headers=headers)

        # Check the response
        if response.status_code == 200:
            user_info = response.json()
            session['user_id'] = user_info['localId']  # Store user ID in session
            flash('Login successful.')
            return redirect(url_for('index'))
        else:
            flash('Login failed. Please check your credentials.')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)  # This removes the user from the session
    flash('You have been logged out.')
    return jsonify({'success': True})  # Return a success response to JavaScript

@app.route('/api/weather/<city>')
def get_weather(city):
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    try:
        url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

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
            return jsonify({'error': 'City not found or API call failed'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
