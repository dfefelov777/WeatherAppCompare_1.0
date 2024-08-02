from django.shortcuts import render
import requests
import datetime
import time

def index(request):
    api_key = 'fe8239de343d34109d094ef35ef03d59'
    current_weather_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
    forecast_url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}'

    if request.method == 'POST':
        city1 = request.POST['city1']
        city2 = request.POST.get('city2', None)

        weather_data1, daily_forecasts1 = fetch_weather_and_forecast(city1, api_key, current_weather_url, forecast_url)

        if city2:
            weather_data2, daily_forecasts2 = fetch_weather_and_forecast(city2, api_key, current_weather_url,
                                                                         forecast_url)
        else:
            weather_data2, daily_forecasts2 = None, None

        context = {
            'weather_data1': weather_data1,
            'daily_forecasts1': daily_forecasts1,
            'weather_data2': weather_data2,
            'daily_forecasts2': daily_forecasts2,
        }

        return render(request, 'weather_app/index.html', context)
    else:
        return render(request, 'weather_app/index.html')


def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.get(current_weather_url.format(city, api_key)).json()
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
            else:
                print("Key 'daily' not found in the response")

            return weather_data, daily_forecasts
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(2)  # Задержка перед повторной попыткой
    return None, None