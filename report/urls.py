from django.urls import path
from .views import WeatherView , J

urlpatterns = [
    path("",WeatherView.as_view(),name="home"),
    path('n/',J.as_view(),name="j")
]
