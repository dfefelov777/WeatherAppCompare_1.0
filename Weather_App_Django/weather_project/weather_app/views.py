from django.shortcuts import render
import requests
import datetime
import time

def index(request):
    appid = 'your api key'
    current_weather_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
    forecast_url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}'

    if request.method == 'POST':
        city1 = request.POST.get('city1', '').strip()
        city2 = request.POST.get('city2', '').strip()

        weather_data1, daily_forecasts1 = None, None
        weather_data2, daily_forecasts2 = None, None
        error_message1, error_message2 = None, None

        if city1:
            weather_data1, daily_forecasts1, error_message1 = fetch_weather_and_forecast(city1, appid, current_weather_url, forecast_url)

        if city2:
            weather_data2, daily_forecasts2, error_message2 = fetch_weather_and_forecast(city2, appid, current_weather_url, forecast_url)

        context = {
            'weather_data1': weather_data1,
            'daily_forecasts1': daily_forecasts1,
            'weather_data2': weather_data2,
            'daily_forecasts2': daily_forecasts2,
            'error_message1': error_message1,
            'error_message2': error_message2,
        }

        return render(request, 'weather_app/index.html', context)
    else:
        return render(request, 'weather_app/index.html')


def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.get(current_weather_url.format(city, api_key)).json()
            if response.get('cod') != 200:
                return None, None, response.get('message', 'Error fetching data')

            lat, lon = response['coord']['lat'], response['coord']['lon']
            forecast_response = requests.get(forecast_url.format(lat, lon, api_key)).json()

            weather_data = {
                'city': city,
                'temperature': round(response['main']['temp'] - 273.15, 2),
                'description': response['weather'][0]['description'],
                'icon': response['weather'][0]['icon'],
            }

            daily_forecasts = []
            if 'daily' in forecast_response:
                for daily_data in forecast_response['daily'][:5]:
                    daily_forecasts.append({
                        'day': datetime.datetime.fromtimestamp(daily_data['dt']).strftime('%A'),
                        'min_temp': round(daily_data['temp']['min'] - 273.15, 2),
                        'max_temp': round(daily_data['temp']['max'] - 273.15, 2),
                        'description': daily_data['weather'][0]['description'],
                        'icon': daily_data['weather'][0]['icon'],
                    })

            return weather_data, daily_forecasts, None
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(2)  # Задержка перед повторной попыткой, чтобы приложение не падало
    return None, None, 'Failed to fetch data after multiple attempts'
