// Logout button click event listener
document.getElementById('logout-btn').addEventListener('click', function() {
    fetch('/logout', {
        method: 'GET',
        credentials: 'same-origin' // This ensures the session cookie is sent with the request
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = '/login'; // Redirect to login page after logout
        } else {
            console.error('Logout failed');
        }
    })
    .catch(error => {
        console.error('Error logging out:', error);
    });
});

// Fetch weather data when the user clicks the 'Get Weather' button
document.getElementById('fetch-weather').addEventListener('click', function() {
    const city = document.getElementById('city-input').value;
    const errorMessageElement = document.getElementById('error-message');
    const weatherIconElement = document.getElementById('weather-icon');

    // Set default weather icon while loading
    weatherIconElement.src = '/static/images/sun.png';

    // Check if city is provided
    if (city) {
        // Fetch weather data from the backend API
        fetch(`/api/weather/${city}`)
            .then(response => response.json())
            .then(data => {
                if (!data.error) {
                    // Update weather data on the page
                    document.getElementById('city').innerText = `${data.city}, ${data.country}`;
                    document.getElementById('temp').innerText = `${data.temperature}°C`;
                    document.getElementById('description').innerText = data.description;
                    document.getElementById('feels-like').innerText = `${data.feels_like}°C`;
                    document.getElementById('temp-min').innerText = `${data.temp_min}°C`;
                    document.getElementById('temp-max').innerText = `${data.temp_max}°C`;
                    document.getElementById('humidity').innerText = `${data.humidity}%`;
                    document.getElementById('wind-speed').innerText = `${data.wind_speed} m/s`;
                    document.getElementById('cloud-coverage').innerText = `${data.cloud_coverage}%`;

                    // Update weather icon with data from the API
                    weatherIconElement.src = `http://openweathermap.org/img/wn/${data.icon}.png`;

                    // Optional: Display sunrise and sunset time
                    const sunrise = new Date(data.sunrise * 1000); // Convert to milliseconds
                    const sunset = new Date(data.sunset * 1000);
                    document.getElementById('sunrise').innerText = `Sunrise: ${sunrise.getHours()}:${sunrise.getMinutes()}`;
                    document.getElementById('sunset').innerText = `Sunset: ${sunset.getHours()}:${sunset.getMinutes()}`;

                    // Hide error message if successful
                    errorMessageElement.classList.remove('show-error');
                } else {
                    // Show error message if city is not found or API call failed
                    errorMessageElement.innerText = 'City not found or API call failed';
                    errorMessageElement.classList.add('show-error');
                }
            })
            .catch(error => {
                // Show error message on API error
                errorMessageElement.innerText = 'Error fetching weather data';
                errorMessageElement.classList.add('show-error');
                console.error('Error fetching weather data:', error);
            });
    } else {
        // Show error message if city input is empty
        errorMessageElement.innerText = 'Please enter a city name';
        errorMessageElement.classList.add('show-error');
    }
});
