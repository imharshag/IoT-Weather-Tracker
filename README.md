# Weather Dashboard 🌤️

This project is a **Weather App** built using `Flask` and integrated with `Firebase` for authentication and `Google Apps` for email notification services. The app is deployed on **Vercel**, offering a seamless and live weather experience.

### 🚀 Features
- 🔒 **User Authentication** with Firebase.
- 📧 **Email Notifications** for weather alerts via Google Apps.
- 🌍 **Live Weather Updates** fetched dynamically.
- 🎨 **Responsive UI** for a modern user experience.
- 🌐 **Hosted on Vercel** for global availability.

### 🛠️ Tech Stack
- **Backend**: Flask
- **Authentication**: Firebase
- **Email Service**: Google Apps
- **Weather Data**: OpenWeather API
- **Hosting**: Vercel

### ⚠️ Setup Reminder
- Obtain an API key from **[OpenWeather](https://openweathermap.org/api)**.
- Set up your **Firebase project** and obtain your API credentials.
- Add these keys to your environment variables or `config.py` file.

### 📸 Live View
👉 **[Check it out here!](https://cloudish.vercel.app/)**


### ⚙️ Setup Instructions

Clone the repository
  
        git clone https://github.com/imharshag/IoT-Weather-Tracker.git

 Navigate to the project directory
    
        cd IoT-Weather-Tracker

Create a .env file in the project root and add the following:
    
    WEATHER_KEY=your_openweather_api_key
    FIREBASE_API_KEY=your_firebase_api_key
    SENDER_EMAIL=your_email@example.com
    SENDER_PASSWORD=your_email_password

    
 This ensures all API keys and sensitive information are securely stored in the `.env` file.

Install dependencies
    
    pip install -r requirements.txt

Run the Flask app
    
    python app.py

### 🌟 Contributions are Welcome!
Feel free to fork this repository, open issues, or submit pull requests to improve the app!

### License
This project is licensed under the MIT License.

### Contact 📬
For any inquiries, reach out via email [**Harsha G** ](mailto:harshag3103@gmail.com)  


---

Enjoy using the Weather Dashboard! 🌦️
