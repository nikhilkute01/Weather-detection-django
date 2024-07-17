import datetime
import requests
from django.shortcuts import render

def index(request):
    API_KEY = "e1402b79100c7f935a55ec3fd497a2ad"
    current_weather_url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    forecast_url = "http://api.openweathermap.org/data/3.0/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}"

    if request.method == "POST":
        city1 = request.POST['city1']
        city2 = request.POST.get('city2', '')

        weather_data1, daily_forecast1 = fetch_weather_forecast(city1, API_KEY, current_weather_url, forecast_url)
        weather_data2, daily_forecast2 = (None, None)
        
        if city2:
            weather_data2, daily_forecast2 = fetch_weather_forecast(city2, API_KEY, current_weather_url, forecast_url)

        context = {
            "weather_data1": weather_data1,
            "daily_forecast1": daily_forecast1,
            "weather_data2": weather_data2,
            "daily_forecast2": daily_forecast2,
        }

        return render(request, 'weather_app/index.html', context)

    else:
        return render(request, 'weather_app/index.html')

def fetch_weather_forecast(city, API_KEY, current_weather_url, forecast_url):
    try:
        response = requests.get(current_weather_url.format(city, API_KEY)).json()
        lat, lon = response['coord']['lat'], response['coord']['lon']
        forecast_response = requests.get(forecast_url.format(lat, lon, API_KEY)).json()

        weather_data = {
            'city': city,
            'temperature': round(response['main']['temp'] - 273.15, 2),
            'description': response['weather'][0]['description'],
            'icon': response['weather'][0]['icon']
        }

        daily_forecast = []
        if 'daily' in forecast_response:
            for daily_data in forecast_response['daily'][:5]:
                daily_forecast.append({
                    "day": datetime.datetime.fromtimestamp(daily_data['dt']).strftime("%A"),
                    "min_temp": round(daily_data['temp']['min'] - 273.15, 2),
                    "max_temp": round(daily_data['temp']['max'] - 273.15, 2),
                    "description": daily_data['weather'][0]['description'],
                    "icon": daily_data['weather'][0]['icon']
                })
        else:
            print("Key 'daily' not found in the forecast response.")
        
        return weather_data, daily_forecast
    except KeyError as e:
        print(f"KeyError: {e}")
        return None, None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None
