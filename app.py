import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mail import Mail, Message
import firebase_admin
from firebase_admin import credentials, auth
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your_default_secret_key')

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('SENDER_EMAIL')  # Your email
app.config['MAIL_PASSWORD'] = os.getenv('SENDER_PASSWORD')  # Your email password or app-specific password
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('SENDER_EMAIL')

# Initialize Flask-Mail
mail = Mail(app)

# Initialize Firebase Admin SDK
cred = credentials.Certificate('firebase-service-account.json')
firebase_admin.initialize_app(cred)

# Weather API configuration
WEATHER_KEY = os.getenv('WEATHER_KEY')
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

# Firebase Authentication REST API endpoint
FIREBASE_AUTH_URL = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=" + os.getenv('FIREBASE_API_KEY')

@app.route('/')
def index():
    success_message = session.pop('success_message', None)
    return render_template('index.html', success_message=success_message)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            auth.create_user(email=email, password=password)
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
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

        if response.status_code == 200:
            user_info = response.json()
            session['user_id'] = user_info['localId']
            session['user_email'] = email  # Store the user's email in the session
            flash('Login successful.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login failed. Please check your credentials.', 'danger')
    
    return render_template('login.html')

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user_id', None)  # Clear the session data
    flash('You have been logged out.', 'info')  # Optionally add a flash message
    return jsonify({'success': True})  # Respond with success to trigger the front-end action

@app.route('/api/weather/<city>')
def get_weather(city):
    if 'user_id' not in session:
        flash('You need to log in to access weather data.', 'danger')
        return jsonify({'error': 'Unauthorized'}), 401
       
    try:
        url = f"{BASE_URL}?q={city}&appid={WEATHER_KEY}&units=metric"
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

            # Send email with weather details
            user_email = session.get('user_email')
            send_weather_email(user_email, weather_data)

            return jsonify(weather_data)
        else:
            # Flash message for invalid city or API failure
            flash('City not found or API call failed.', 'warning')
            return jsonify({'error': 'City not found or API call failed.'}), 400
        
    except Exception as e:
        # Flash message for unexpected errors
        flash(f'An unexpected error occurred: {str(e)}', 'warning')
        return jsonify({'error': str(e)}), 500

def send_weather_email(to_email, weather_data):
    subject = f"🌤️ Weather Update for {weather_data['city']}"
    body = f"""
    <html>
        <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f0f2f5; margin: 0; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 12px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); overflow: hidden;">
                <header style="background-color: #007BFF; padding: 20px; text-align: center; color: #ffffff;">
                    <h1 style="margin: 0; font-size: 24px;">Weather Update for {weather_data['city']}</h1>
                </header>
                <div style="padding: 30px; text-align: center; color: #333;">
                    <p style="font-size: 18px; margin-bottom: 10px;">🌡️ <strong>{weather_data['temperature']}°C</strong></p>
                    <p style="font-size: 14px; color: #555; margin-bottom: 20px;">For more details, click below:</p>
                    <a href="https://atmoslot.vercel.app/" 
                       style="display: inline-block; background-color: #007BFF; color: #ffffff; padding: 10px 20px; font-size: 16px; text-decoration: none; border-radius: 6px; margin-top: 10px;">
                        View Full Weather Report
                    </a>
                </div>
                <footer style="background-color: #f1f1f1; padding: 15px; text-align: center; font-size: 12px; color: #777;">
                    <p style="margin: 0;">Stay informed. Stay prepared. 🌦️</p>
                </footer>
            </div>
        </body>
    </html>
    """

    msg = Message(subject, recipients=[to_email])
    msg.html = body  # Send HTML email

    try:
        mail.send(msg)
        print(f"Weather details sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == '__main__':
    app.run(debug=True)
