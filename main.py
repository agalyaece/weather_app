from flask import Flask, render_template, request
import requests

app = Flask(__name__)

api_key = "7dc03b46608a2974b0883bd054768791"


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/weather', methods=['POST'])
def weather():
    city = request.form['city']
    if not city:
        return render_template('index.html', error="Please enter a city.")

    weather_data = get_weather_data(city)
    if not weather_data:
        return render_template('index.html', error="City not found.")

    return render_template('index.html', weather_data=weather_data)


def get_weather_data(city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric',  # Use 'imperial' for Fahrenheit
    }

    response = requests.get(base_url, params=params)
    print(response.text)
    if response.status_code == 200:
        data = response.json()
        weather_ = {
            'city': data['name'],
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon'],
        }
        return weather_

    return None


if __name__ == '__main__':
    app.run(debug=True)


