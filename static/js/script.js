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
    const city = document.getElementById('city-input').value.trim();
    const errorMessageElement = document.getElementById('error-message');
    const weatherIconElement = document.getElementById('weather-icon');

    // Set default weather icon while loading
    weatherIconElement.src = '/static/images/sun.png';
    
    // Check if city is provided
    if (city) {
        // Fetch weather data from the backend API
        fetch(`/api/weather/${encodeURIComponent(city)}`, {
            method: 'GET',
            credentials: 'same-origin' // Ensure cookies are sent
        })
            .then(response => response.json().then(data => ({ status: response.status, body: data })))
            .then(({ status, body }) => {
                if (status === 200 && !body.error) {
                    // Update weather data on the page
                    document.getElementById('city').innerText = `${body.city}, ${body.country}`;
                    document.getElementById('temp').innerText = `${body.temperature}°C`;
                    document.getElementById('description').innerText = body.description;
                    document.getElementById('feels-like').innerText = `${body.feels_like}°C`;
                    document.getElementById('temp-min').innerText = `${body.temp_min}°C`;
                    document.getElementById('temp-max').innerText = `${body.temp_max}°C`;
                    document.getElementById('humidity').innerText = `${body.humidity}%`;
                    document.getElementById('wind-speed').innerText = `${body.wind_speed} m/s`;
                    document.getElementById('cloud-coverage').innerText = `${body.cloud_coverage}%`;

                    // Update weather icon with data from the API
                    weatherIconElement.src = `http://openweathermap.org/img/wn/${body.icon}.png`;

                    // Optional: Display sunrise and sunset time
                    const sunrise = new Date(body.sunrise * 1000); // Convert to milliseconds
                    const sunset = new Date(body.sunset * 1000);
                    document.getElementById('sunrise').innerText = `Sunrise: ${sunrise.getHours()}:${String(sunrise.getMinutes()).padStart(2, '0')}`;
                    document.getElementById('sunset').innerText = `Sunset: ${sunset.getHours()}:${String(sunset.getMinutes()).padStart(2, '0')}`;

                    // Hide error message if successful
                    errorMessageElement.classList.remove('show-error');
                } else {
                    // Handle different error statuses
                    if (status === 401) {
                        // Unauthorized access, redirect to login
                        window.location.href = '/login';
                    } else {
                        // For other errors, reload the page to display flash message
                        window.location.href = '/';
                    }
                }
            })
            .catch(error => {
                // On fetch error, reload the page to display a generic error message
                console.error('Error fetching weather data:', error);
                window.location.href = '/';
            });
    } else {
        window.location.href = '/';
    }
});
