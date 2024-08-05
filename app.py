from flask import Flask, request, render_template
import requests

app = Flask(__name__)

BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'
API_KEY = '4059c13588c380dad9296dadb7bfe6bb'  # Provided API key

def get_weather_data(city, units='metric'):
    try:
        params = {
            'q': city,
            'appid': API_KEY,
            'units': units
        }
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def get_weather_class(weather_data):
    weather_id = weather_data['weather'][0]['id']
    if 200 <= weather_id < 300:
        return 'storm'
    elif 300 <= weather_id < 600:
        return 'rainy'
    elif 600 <= weather_id < 700:
        return 'snowy'
    elif 700 <= weather_id < 800:
        return 'foggy'
    elif weather_id == 800:
        return 'clear-sky'
    else:
        return 'cloudy'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form['cityName']
        unit = request.form['unit']
        weather_data = get_weather_data(city, unit)
        if weather_data and weather_data.get('cod') == 200:
            weather_class = get_weather_class(weather_data)
            return render_template('result.html', weather_data=weather_data, units=unit, weather_class=weather_class)
        else:
            error = "Invalid city name or unable to fetch weather data."
            return render_template('index.html', error=error)
    return render_template('index.html')

@app.route('/result')
def result():
    return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True)
