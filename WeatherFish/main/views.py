from django.shortcuts import render, redirect
from .models import Cities, Datetimes, Weather_measurements, Feedback
from datetime import datetime, timedelta
from .forms import Calendar_Form, Measurement_Form, Feedback_Form, Town_Form
import numpy as np
from django.urls import reverse, reverse_lazy


class Info_weather:
    obj = []
    list_temp = []
    list_humidity = []
    list_pressure = []
    list_wind_speed = []
    list_date = []
    list_day = []
    list_day_month = []
    list_time = []
    list_dats_id = []
    sum_temperature = 0
    n_temperature = 0
    sum_wind_speed = 0
    n_wind_speed = 0
    sum_pressure = 0
    n_pressure = 0
    sum_humidity = 0
    n_humidity = 0

    def clear(self):
        self.obj = []
        self.list_temp = []
        self.list_humidity = []
        self.list_pressure = []
        self.list_wind_speed = []
        self.list_date = []
        self.list_day = []
        self.list_day_month = []
        self.list_time = []
        self.list_dats_id = []
        self.sum_temperature = 0
        self.n_temperature = 0
        self.sum_wind_speed = 0
        self.n_wind_speed = 0
        self.sum_pressure = 0
        self.n_pressure = 0
        self.sum_humidity = 0
        self.n_humidity = 0
        return self


class info_average:
    info_avg = []
    avg_temperature = []
    avg_wind_speed = []
    avg_pressure = []
    avg_humidity = []

    def clear(self):
        self.info_avg = []
        self.avg_temperature = []
        self.avg_wind_speed = []
        self.avg_pressure = []
        self.avg_humidity = []
        return self


def temperature_conversion(t, t_temp):
    if t == 'C':
        temp = t_temp - 273.15
    elif t == 'F':
        temp = t_temp * 1.8 - 459.67
    else:
        temp = t_temp
    return round(temp,1)


def pressure_conversion(p, p_pres):
    if p == 'mmrt':
        pr = round(float(p_pres) * 0.750064,2)
    else:
        pr = p_pres
    return pr


def speed_conversion(s, s_speed):
    if s == 'kmch':
        sp = s_speed * 3.6
    else:
        sp = s_speed
    return sp


def fill_info_weather(city_name, dats, t, p, s):
    info = Info_weather()
    info.clear()

    for i in range(len(dats)):
        info.list_dats_id.append(dats[i].id)

    gorod = Cities.objects.filter(city=city_name)
    info.obj = Weather_measurements.objects.filter(city_id=gorod[0].id, datetime_id__in=info.list_dats_id)

    for i in range(len(info.list_dats_id) - 1):
        info.list_date.append(info.obj[i].datetime.datetime.strftime('%d.%m.%Y'))
        info.list_time.append(info.obj[i].datetime.datetime.strftime('%H:%M'))
        info.list_day.append(info.obj[i].datetime.datetime.strftime('%d'))
        info.list_day_month.append(info.obj[i].datetime.datetime.strftime('%d.%m'))
        if info.obj[i].temperature == 'nan':
            info.list_temp.append(0)
        else:
            temp = temperature_conversion(t, info.obj[i].temperature)
            info.list_temp.append(temp)
            info.sum_temperature += temp
            info.n_temperature += 1

        if info.obj[i].humidity == 'nan':
            info.list_humidity.append(0)
        else:
            info.list_humidity.append(info.obj[i].humidity)
            info.sum_humidity += info.obj[i].humidity
            info.n_humidity += 1

        if info.obj[i].pressure == 'nan':
            info.list_pressure.append(0)
        else:
            pr = pressure_conversion(p, info.obj[i].pressure)
            info.list_pressure.append(pr)
            info.sum_pressure += pr
            info.n_pressure += 1

        if info.obj[i].wind_speed == 'nan':
            info.list_wind_speed.append(0)
        else:
            sp = speed_conversion(s, info.obj[i].wind_speed)
            info.list_wind_speed.append(sp)
            info.sum_wind_speed += sp
            info.n_wind_speed += 1

    return info


def fill_info_weather_with_avg(city_name, first_date, count, t, p, s):
    average = info_average()
    average.clear()

    date_nabor = [first_date]
    for i in range(1, count):
        date_nabor.append(first_date + timedelta(days=i))

    dats = Datetimes.objects.filter(datetime__in=date_nabor)
    info = fill_info_weather(city_name, dats, t, p, s)

    for i in range(2, len(date_nabor) + 1):
        dats_avg = Datetimes.objects.filter(datetime__range=date_nabor[i - 2:i])
        average.info_avg.append(fill_info_weather(city_name, dats_avg, t, p, s))
        if (average.info_avg[i - 2].n_temperature):
            average.avg_temperature.append(round((average.info_avg[i - 2].sum_temperature / average.info_avg[i - 2].n_temperature), 1))
        else:
            average.avg_temperature.append(0)

        if (average.info_avg[i - 2].n_pressure):
            average.avg_pressure.append(round((average.info_avg[i - 2].sum_pressure / average.info_avg[i - 2].n_pressure)))
        else:
            average.avg_pressure.append(0)

        if (average.info_avg[i - 2].n_humidity):
            average.avg_humidity.append(round((average.info_avg[i - 2].sum_humidity / average.info_avg[i - 2].n_humidity)))
        else:
            average.avg_humidity.append(0)

        if (average.info_avg[i - 2].n_wind_speed):
            average.avg_wind_speed.append(round((average.info_avg[i - 2].sum_wind_speed / average.info_avg[i - 2].n_wind_speed), 1))
        else:
            average.avg_wind_speed.append(0)
    return average, info


################################################################################
###                 РќРђРЁР Р“Р›РћР‘РђР›Р¬РќР«Р• РџР•Р Р•РњР•РќРќР«Р• (РїРѕ СѓРјРѕР»С‡Р°РЅРёСЋ)                ###
################################################################################
mf = Measurement_Form()
tf = Town_Form()
cf = Calendar_Form()
ff = Feedback_Form()
date_inf = "02.10.2012"
date_inf2 = "05.10.2012"
city_name = 'Albuquerque'
temperature = 'C'
pressure = 'mmrt'
speed = 'mc'
path = ''


def index(request):
    global mf
    global tf
    global cf
    global ff
    global date_inf
    global city_name
    global temperature
    global pressure
    global speed
    t = temperature
    p = pressure
    s = speed

    if request.method == 'POST':
        cf = Calendar_Form(request.POST)
        ff = Feedback_Form(request.POST)
        if (Measurement_Form(request.POST).is_valid()):
            mf = Measurement_Form(request.POST)
        if(Town_Form(request.POST).is_valid()):
            tf = Town_Form(request.POST)
        if ff.is_valid():
            fform = ff.save(commit=False)
            fform.save()
            return redirect('start')
        if request.POST.get("date_inf") != None:
            date_inf = request.POST.get("date_inf")
        if request.POST.get("town_ch") != None:
            city_name = request.POST.get("town_ch")
        if request.POST.get("temp") != None:
            t = request.POST.get("temp")
        if request.POST.get("pres") != None:
            p = request.POST.get("pres")
        if request.POST.get("speed") != None:
            s = request.POST.get("speed")
        first_date = datetime.strptime(date_inf, "%d.%m.%Y")
        avarage = fill_info_weather_with_avg(city_name, first_date, 5, t, p, s)
        temp_hours = []
        temp_hours.append(temperature_conversion(t,avarage[0].info_avg[0].obj[9].temperature))
        temp_hours.append(temperature_conversion(t,avarage[0].info_avg[0].obj[12].temperature))
        temp_hours.append(temperature_conversion(t,avarage[0].info_avg[0].obj[18].temperature))
        temp_hours.append(temperature_conversion(t,avarage[0].info_avg[0].obj[22].temperature))
        data = {'city_name':city_name, 'towns': avarage[0].info_avg[0].obj,
               'list_temp': avarage[0].avg_temperature,
               'list_humidity': avarage[0].avg_humidity,
               'list_wind_speed': avarage[0].avg_wind_speed,
               'list_pressure': avarage[0].avg_pressure,
               'list_date': avarage[1].list_date,
               'temp_hours':temp_hours,
               'mf': mf, 'tf': tf, 'cf': cf, 'ff': ff,
               't' : t, 'p' : p, 's' : s }
        return render(request, 'main/index.html', data)
    else:
        first_date = datetime.strptime(date_inf, "%d.%m.%Y")
        avarage = fill_info_weather_with_avg(city_name, first_date, 5, t, p, s)
        temp_hours = []
        temp_hours.append(temperature_conversion(t,avarage[0].info_avg[0].obj[9].temperature))
        temp_hours.append(temperature_conversion(t,avarage[0].info_avg[0].obj[12].temperature))
        temp_hours.append(temperature_conversion(t,avarage[0].info_avg[0].obj[18].temperature))
        temp_hours.append(temperature_conversion(t,avarage[0].info_avg[0].obj[22].temperature))
        data = {'city_name':city_name, 'towns': avarage[0].info_avg[0].obj,
               'list_temp': avarage[0].avg_temperature,
               'list_humidity': avarage[0].avg_humidity,
               'list_wind_speed': avarage[0].avg_wind_speed,
               'list_pressure': avarage[0].avg_pressure,
               'list_date': avarage[1].list_date,
               'temp_hours':temp_hours,
               'mf': mf, 'tf': tf, 'cf': cf, 'ff': ff,
               't' : t, 'p' : p, 's' : s }
    return render(request, 'main/index.html', context = data)


def forecast_hour(request):
    global mf
    global tf
    global cf
    global ff
    global date_inf
    global city_name
    global temperature
    global pressure
    global speed
    t = temperature
    p = pressure
    s = speed

    if request.method == 'POST':
        cf = Calendar_Form(request.POST)
        ff = Feedback_Form(request.POST)
        if (Measurement_Form(request.POST).is_valid()):
            mf = Measurement_Form(request.POST)
        if(Town_Form(request.POST).is_valid()):
            tf = Town_Form(request.POST)
        if ff.is_valid():
            fform = ff.save(commit=False)
            fform.save()
            return redirect('forecast_hour')
        if request.POST.get("date_inf") != None:
            date_inf = request.POST.get("date_inf")
        if request.POST.get("town_ch") != None:
            city_name = request.POST.get("town_ch")
        if request.POST.get("temp") != None:
            t = request.POST.get("temp")
        if request.POST.get("pres") != None:
            p = request.POST.get("pres")
        if request.POST.get("speed") != None:
            s = request.POST.get("speed")
        start_date = datetime.strptime(date_inf, "%d.%m.%Y")
        end_date = start_date + timedelta(days=1)
        dats = Datetimes.objects.filter(datetime__range=(start_date, end_date))
        info = fill_info_weather(city_name, dats, t, p, s)
        temp_hours = []
        temp_pres = []
        temp_speed = []
        for i in range(24):
            temp_hours.append(temperature_conversion(t,info.obj[i].temperature))
            temp_pres.append(pressure_conversion(p, info.obj[i].pressure))
            temp_speed.append(speed_conversion(s, info.obj[i].wind_speed))
        data = {'towns': info.obj[:len(info.list_time)],
               'list_temp': info.list_temp,
               'list_humidity': info.list_humidity,
               'list_pressure': info.list_pressure,
               'list_time': info.list_time,
               'temp_hours':temp_hours,
               'temp_pres':temp_pres,
               'temp_speed':temp_speed,
               'mf': mf, 'tf': tf, 'cf': cf, 'ff': ff,
               't' : t, 'p' : p, 's' : s }
        return render(request, 'main/forecast_hour.html', data)
    else:
        start_date = datetime.strptime(date_inf, "%d.%m.%Y")
        end_date = start_date + timedelta(days=1)
        dats = Datetimes.objects.filter(datetime__range=(start_date, end_date))
        info = fill_info_weather(city_name, dats, t, p, s)
        temp_hours = []
        temp_pres = []
        temp_speed = []
        for i in range(24):
            temp_hours.append(temperature_conversion(t, info.obj[i].temperature))
            temp_pres.append(pressure_conversion(p, info.obj[i].pressure))
            temp_speed.append(speed_conversion(s, info.obj[i].wind_speed))
        data = {'towns': info.obj[:len(info.list_time)],
               'list_temp': info.list_temp,
               'list_humidity': info.list_humidity,
               'list_pressure': info.list_pressure,
               'list_time': info.list_time,
               'temp_hours':temp_hours,
               'temp_pres':temp_pres,
               'temp_speed':temp_speed,
               'mf': mf, 'tf': tf, 'cf': cf, 'ff': ff,
               't' : t, 'p' : p, 's' : s }
    return render(request, 'main/forecast_hour.html', context = data)


def forecast_ten_days(request):
    global mf
    global tf
    global cf
    global ff
    global date_inf
    global city_name
    global temperature
    global pressure
    global speed
    t = temperature
    p = pressure
    s = speed

    if request.method == 'POST':
        cf = Calendar_Form(request.POST)
        ff = Feedback_Form(request.POST)
        if (Measurement_Form(request.POST).is_valid()):
            mf = Measurement_Form(request.POST)
        if(Town_Form(request.POST).is_valid()):
            tf = Town_Form(request.POST)
        if ff.is_valid():
            fform = ff.save(commit=False)
            fform.save()
            return redirect('forecast_ten_days')
        if request.POST.get("date_inf") != None:
            date_inf = request.POST.get("date_inf")
        if request.POST.get("town_ch") != None:
            city_name = request.POST.get("town_ch")
        if request.POST.get("temp") != None:
            t = request.POST.get("temp")
        if request.POST.get("pres") != None:
            p = request.POST.get("pres")
        if request.POST.get("speed") != None:
            s = request.POST.get("speed")
        first_date = datetime.strptime(date_inf, "%d.%m.%Y")
        avarage = fill_info_weather_with_avg(city_name, first_date, 11, t, p, s)
        data = {'towns':  avarage[1].obj[:len(avarage[1].list_time)],
               'list_temp': avarage[0].avg_temperature,
               'list_humidity': avarage[0].avg_humidity,
               'list_wind_speed': avarage[0].avg_wind_speed,
               'list_pressure': avarage[0].avg_pressure,
               'list_date': avarage[1].list_date,
               'mf': mf, 'tf': tf, 'cf': cf, 'ff': ff,
               't' : t, 'p' : p, 's' : s }
        return render(request, 'main/forecast_ten_days.html', data)
    else:
        first_date = datetime.strptime(date_inf, "%d.%m.%Y")
        avarage = fill_info_weather_with_avg(city_name, first_date, 11, t, p, s)
        data = {'towns':  avarage[1].obj[:len(avarage[1].list_time)],
               'list_temp': avarage[0].avg_temperature,
               'list_humidity': avarage[0].avg_humidity,
               'list_wind_speed': avarage[0].avg_wind_speed,
               'list_pressure': avarage[0].avg_pressure,
               'list_date': avarage[1].list_date,
               'mf': mf, 'tf': tf, 'cf': cf, 'ff': ff,
               't' : t, 'p' : p, 's' : s }
    return render(request, 'main/forecast_ten_days.html', context = data)


def forecast_month(request):
    global mf
    global tf
    global cf
    global ff
    global date_inf
    global city_name
    global temperature
    global pressure
    global speed
    t = temperature
    p = pressure
    s = speed

    if request.method == 'POST':
        cf = Calendar_Form(request.POST)
        ff = Feedback_Form(request.POST)
        if (Measurement_Form(request.POST).is_valid()):
            mf = Measurement_Form(request.POST)
        if(Town_Form(request.POST).is_valid()):
            tf = Town_Form(request.POST)
        if ff.is_valid():
            fform = ff.save(commit=False)
            fform.save()
            return redirect('forecast_month')
        if request.POST.get("date_inf") != None:
            date_inf = request.POST.get("date_inf")
        if request.POST.get("town_ch") != None:
            city_name = request.POST.get("town_ch")
        if request.POST.get("temp") != None:
            t = request.POST.get("temp")
        if request.POST.get("pres") != None:
            p = request.POST.get("pres")
        if request.POST.get("speed") != None:
            s = request.POST.get("speed")
        first_date = datetime.strptime(date_inf, "%d.%m.%Y")
        avarage = fill_info_weather_with_avg(city_name, first_date, 29, t, p, s)
        data = {'towns':  avarage[1].obj[:len(avarage[1].list_time)],
               'list_temp': avarage[0].avg_temperature,
               'list_humidity': avarage[0].avg_humidity,
               'list_wind_speed': avarage[0].avg_wind_speed,
               'list_pressure': avarage[0].avg_pressure,
               'list_date': avarage[1].list_date,
               'list_day': avarage[1].list_day,
               'mf': mf, 'tf': tf, 'cf': cf, 'ff': ff,
               't' : t, 'p' : p, 's' : s }
        return render(request, 'main/forecast_month.html', data)
    else:
        first_date = datetime.strptime(date_inf, "%d.%m.%Y")
        avarage = fill_info_weather_with_avg(city_name, first_date, 29, t, p, s)
        data = {'towns':  avarage[1].obj[:len(avarage[1].list_time)],
               'list_temp': avarage[0].avg_temperature,
               'list_humidity': avarage[0].avg_humidity,
               'list_wind_speed': avarage[0].avg_wind_speed,
               'list_pressure': avarage[0].avg_pressure,
               'list_date': avarage[1].list_date,
               'list_day': avarage[1].list_day,
               'mf': mf, 'tf': tf, 'cf': cf, 'ff': ff,
               't' : t, 'p' : p, 's' : s }
    return render(request, 'main/forecast_month.html', context = data)


def forecast_range(request):
    global mf
    global tf
    global cf
    global ff
    global date_inf
    global date_inf2
    global city_name
    global temperature
    global pressure
    global speed
    t = temperature
    p = pressure
    s = speed

    if request.method == 'POST':
        cf = Calendar_Form(request.POST)
        ff = Feedback_Form(request.POST)
        if (Measurement_Form(request.POST).is_valid()):
            mf = Measurement_Form(request.POST)
        if(Town_Form(request.POST).is_valid()):
            tf = Town_Form(request.POST)
        if ff.is_valid():
            fform = ff.save(commit=False)
            fform.save()
            return redirect('forecast_range')
        if request.POST.get("date_inf") != None and request.POST.get("date_inf2") != None:
            date_inf = request.POST.get("date_inf")
            date_inf2 = request.POST.get("date_inf2")
        if request.POST.get("town_ch") != None:
            city_name = request.POST.get("town_ch")
        if request.POST.get("temp") != None:
            t = request.POST.get("temp")
        if request.POST.get("pres") != None:
            p = request.POST.get("pres")
        if request.POST.get("speed") != None:
            s = request.POST.get("speed")
        start_date = datetime.strptime(date_inf, "%d.%m.%Y")
        end_date = datetime.strptime(date_inf2, "%d.%m.%Y") + timedelta(days=1)
        dats = Datetimes.objects.filter(datetime__range=(start_date, end_date))
        info = fill_info_weather(city_name, dats, t, p, s)
        count = end_date - start_date
        temp_hours = []
        temp_pres = []
        temp_speed = []
        for i in range(count.days * 24):
            temp_hours.append(temperature_conversion(t,info.obj[i].temperature))
            temp_pres.append(pressure_conversion(p, info.obj[i].pressure))
            temp_speed.append(speed_conversion(s, info.obj[i].wind_speed))
        data = {'towns': info.obj[:len(info.list_time)],
               'list_temp': info.list_temp,
               'list_humidity': info.list_humidity,
               'list_pressure': info.list_pressure,
               'list_time': info.list_time,
               'temp_hours':temp_hours,
               'temp_pres':temp_pres,
               'temp_speed':temp_speed,
               'mf': mf, 'tf': tf, 'cf': cf, 'ff': ff,
               't' : t, 'p' : p, 's' : s }
        return render(request, 'main/forecast_range.html', data)
    else:
        start_date = datetime.strptime(date_inf, "%d.%m.%Y")
        end_date = datetime.strptime(date_inf2, "%d.%m.%Y") + timedelta(days=1)
        dats = Datetimes.objects.filter(datetime__range=(start_date, end_date))
        info = fill_info_weather(city_name, dats, t, p, s)
        count = end_date - start_date
        temp_hours = []
        temp_pres = []
        temp_speed = []
        for i in range(count.days * 24):
            temp_hours.append(temperature_conversion(t,info.obj[i].temperature))
            temp_pres.append(pressure_conversion(p, info.obj[i].pressure))
            temp_speed.append(speed_conversion(s, info.obj[i].wind_speed))
        data = {'towns': info.obj[:len(info.list_time)],
               'list_temp': info.list_temp,
               'list_humidity': info.list_humidity,
               'list_pressure': info.list_pressure,
               'list_time': info.list_time,
               'temp_hours':temp_hours,
               'temp_pres':temp_pres,
               'temp_speed':temp_speed,
               'mf': mf, 'tf': tf, 'cf': cf, 'ff': ff,
               't' : t, 'p' : p, 's' : s }
    return render(request, 'main/forecast_range.html', context = data)
