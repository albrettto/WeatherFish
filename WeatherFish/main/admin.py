from django.contrib import admin
from .models import Cities, Datetimes, Weather_measurements, Feedback


@admin.register(Cities)
class CityAdmin(admin.ModelAdmin):
    list_display = ("city", "country", "latitude", "longitude")


admin.site.register(Datetimes)


@admin.register(Weather_measurements)
class Weather_measurementAdmin(admin.ModelAdmin):
    list_display = ("datetime","city","humidity","pressure","temperature", "wind_direction", "wind_speed", "description")
    list_filter = ("city", )


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    pass
