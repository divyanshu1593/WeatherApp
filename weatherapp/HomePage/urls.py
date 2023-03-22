from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('CurrentWeather', views.current_weather, name="CurrentWeather"),
    path('home', views.home, name="home"),
    path('input_loc', views.input_loc, name="input_loc"),
    path('handle_input', views.handle_input, name="handle_input"),
    path('WeatherForecast', views.weather_forecast, name="WeatherForecast")
]