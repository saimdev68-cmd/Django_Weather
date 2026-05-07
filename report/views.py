from django.shortcuts import render
from django.views import View
from django.conf import settings
import requests
from datetime import datetime

# Create your views here.

class WeatherView(View):
    def get(self, request):
        city = request.GET.get("city") or ""
        weather_data = None

        if city:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={settings.WEATHER_API_KEY}&units=metric"

            try:
                response = requests.get(url, timeout=5)
                data = response.json()

                if response.status_code == 200 and "main" in data:

                    wind_speed_kmh = data["wind"]["speed"] * 3.6
                    visibility = data.get("visibility", 0) / 1000

                    weather_data = {
                        "city": data["name"],
                        "temperature": data["main"]["temp"],
                        "description": data["weather"][0]["description"],
                        "humidity": data["main"]["humidity"],
                        "wind_speed": round(wind_speed_kmh, 2),
                        "sunrise": datetime.fromtimestamp(data["sys"]["sunrise"]),
                        "sunset": datetime.fromtimestamp(data["sys"]["sunset"]),
                        "feels_like": data["main"]["feels_like"],
                        "temp_min": data["main"]["temp_min"],
                        "temp_max": data["main"]["temp_max"],
                        "visibility": round(visibility, 2),
                        "condition_main": data["weather"][0]["main"],
                        "current_time": datetime.now(),  # FIXED
                    }

                else:
                    weather_data = {"error": data.get("message", "City not found")}

            except Exception as e:
                weather_data = {"error": "API request failed"}

        return render(request, "index.html", {
            "weather": weather_data,
            "city": city
        })