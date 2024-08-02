# Weather Comparison App

## Описание
Weather Comparison App - это веб-приложение, разработанное на Django, которое позволяет пользователям сравнивать текущие погодные условия

## Цели проекта
- Сравнение погоды: Предоставить пользователям возможность сравнивать текущие погодные условия и прогнозы в двух городах.
- Удобство использования: Обеспечить простой и интуитивно понятный интерфейс для ввода данных и отображения результатов.
- Динамическое отображение: Использовать динамические фоны и иконки для улучшения визуального восприятия.

## Основные функции
1. Получение текущей погоды: Приложение использует API OpenWeatherMap для получения текущих погодных условий.
2. Прогноз погоды: Приложение также предоставляет прогноз погоды на несколько дней вперед.
3. Сравнение городов: Пользователи могут вводить два города для сравнения их погодных условий.
4. Обработка ошибок: Приложение корректно обрабатывает некорректный ввод и отображает сообщения об ошибках.

## Технологии
- Django: Основной фреймворк для разработки веб-приложения.
- HTML/CSS: Для создания пользовательского интерфейса.
- JavaScript: Для динамического обновления контента.
- API OpenWeatherMap: Для получения данных о погоде.

## Установка и запуск
1. Клонируйте репозиторий:
   
    git clone https://github.com/dfefelov777/WeatherAppCompare_1.0.git
    
2. Перейдите в директорию проекта:
   
    cd WeatherAppCompare_1.0/Weather_App_Django/weather_project
    
3. Установите зависимости:
   
    pip install -r requirements.txt
    
4. Выполните миграции базы данных:
   
    python manage.py migrate
    
5. Запустите сервер разработки:
   
    python manage.py runserver
    
## Использование
1. Откройте браузер и перейдите по адресу http://127.0.0.1:8000/.
2. Введите названия двух городов для сравнения их погодных условий.
3. Нажмите кнопку "Сравни погоду" для отображения текущих погодных условий

## Пример кода
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
            time.sleep(2)  # Задержка перед повторной попыткой
    return None, None, 'Failed to fetch data after multiple attempts'
## Заключение
Проект "Weather Comparison App" демонстрирует возможности Django для создания интерактивных веб-приложений. Он предоставляет пользователям удобный способ сравнения погодных условий в разных городах.
