document.getElementById('fetch-weather').addEventListener('click', function() {
    const city = document.getElementById('city-input').value;
    const errorMessageElement = document.getElementById('error-message');
    const weatherIconElement = document.getElementById('weather-icon'); // Weather icon element

    // Show the default placeholder image initially
    weatherIconElement.src = '/static/images/sun.png';

    if (city) {
        fetch(`/api/weather/${city}`)
            .then(response => response.json())
            .then(data => {
                if (!data.error) {
                    document.getElementById('city').innerText = data.city;
                    document.getElementById('country').innerText = data.country;
                    document.getElementById('temp').innerText = `${data.temperature}°C`;
                    document.getElementById('feels-like').innerText = `${data.feels_like}°C`;
                    document.getElementById('temp-min').innerText = `${data.temp_min}°C`;
                    document.getElementById('temp-max').innerText = `${data.temp_max}°C`;
                    document.getElementById('humidity').innerText = `${data.humidity}%`;
                    document.getElementById('wind-speed').innerText = `${data.wind_speed} m/s`;
                    document.getElementById('cloud-coverage').innerText = `${data.cloud_coverage}%`;
                    document.getElementById('description').innerText = data.description;

                    // Update weather icon with data from the API
                    weatherIconElement.src = `http://openweathermap.org/img/wn/${data.icon}.png`;

                    errorMessageElement.classList.remove('show-error'); // Hide error message
                } else {
                    errorMessageElement.innerText = 'City not found or API call failed';
                    errorMessageElement.classList.add('show-error'); // Show error message
                }
            })
            .catch(error => {
                errorMessageElement.innerText = 'Error fetching weather data';
                errorMessageElement.classList.add('show-error'); // Show error message
                console.error('Error fetching weather data:', error);
            });
    } else {
        errorMessageElement.innerText = 'Please enter a city name';
        errorMessageElement.classList.add('show-error'); // Show error message
    }
});
