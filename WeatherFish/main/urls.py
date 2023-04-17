from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name = 'start'),
    path('forecast_hour', views.forecast_hour, name = 'forecast_hour'),
    path('forecast_ten_days', views.forecast_ten_days, name = 'forecast_ten_days'),
    path('forecast_month', views.forecast_month, name = 'forecast_month'),
    path('forecast_range', views.forecast_range, name = 'forecast_range'),
]
