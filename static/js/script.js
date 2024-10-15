// Handle form submission and fetch weather data
document.getElementById('weather-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const city = document.getElementById('city').value;
    
    // Clear previous results
    document.getElementById('weather-result').style.display = 'none';
    document.getElementById('error-message').innerHTML = '';
  
    fetch(`/api/weather/${city}`)
      .then(response => response.json())
      .then(data => {
        if (data.error) {
          document.getElementById('error-message').innerHTML = data.error;
        } else {
          document.getElementById('city-name').innerText = data.city;
          document.getElementById('temp').innerText = `Temperature: ${data.temperature}°C`;
          document.getElementById('humidity').innerText = `Humidity: ${data.humidity}%`;
          document.getElementById('wind-speed').innerText = `Wind Speed: ${data.wind_speed} m/s`;
          document.getElementById('weather-result').style.display = 'block';
        }
      })
      .catch(error => {
        document.getElementById('error-message').innerHTML = 'Error fetching weather data.';
      });
  });
  