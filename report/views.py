from django.shortcuts import render
from django.views import View
from django.conf import settings
import requests
from datetime import datetime
from django.http import JsonResponse
from django.utils import timezone

# Create your views here.

class WeatherView(View):    
    def get(self,request):
        city = request.GET.get("city") or ""
        weather_data = None
        if city:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={settings.WEATHER_API_KEY}&units=metric"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                wind_speed_kmh = data["wind"]["speed"] * 3.6
                visibility = data["visibility"] / 1000
                weather_data = {
                    "city":data["name"],
                    "temperature":data["main"]["temp"],
                    "description":data["weather"][0]["description"],
                    "humidity":data["main"]["humidity"],
                    "wind_speed":round(wind_speed_kmh,2),
                    "sunrise": datetime.fromtimestamp(data["sys"]["sunrise"]),
                    "sunset":datetime.fromtimestamp(data["sys"]["sunset"]),
                    'feels_like':data["main"]["feels_like"],
                    "temp_min":data["main"]["temp_min"],
                    "temp_max":data["main"]["temp_max"],
                    "visibility":visibility,
                    "current_time": timezone.now().timestamp(), 
                    "condition_main": data["weather"][0]["main"],
                }
            else:
                weather_data = {"error":"city not found"}
        return render (request,"index.html",{"weather":weather_data,"city":city})
    
class J(View):
        def get(self,request):
            city = request.GET.get("city") or ""
            weather_data = None
            if city:
                url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={settings.WEATHER_API_KEY}&units=metric"
                response = requests.get(url)

                if response.status_code == 200:
                    data = response.json()
                    return JsonResponse (data)
                else:
                    weather_data = {"error":"city not found"}
            return JsonResponse (weather_data)