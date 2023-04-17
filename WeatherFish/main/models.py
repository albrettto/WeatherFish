from django.db import models


class Cities(models.Model):
    city = models.CharField('city', max_length=250, unique=True)
    country = models.CharField('country', max_length=250)
    latitude = models.FloatField('latitude')
    longitude = models.FloatField('longitude')

    def __str__(self):
        return self.city

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        unique_together = ('latitude', 'longitude')


class Datetimes(models.Model):
    datetime = models.DateTimeField('dates', unique=True)

    class Meta:
        verbose_name = 'Дату'
        verbose_name_plural = 'Даты'


class Weather_measurements(models.Model):
    datetime = models.ForeignKey('Datetimes', on_delete=models.CASCADE)
    city = models.ForeignKey('Cities', on_delete=models.CASCADE)
    humidity = models.IntegerField('humidity', null=True)
    pressure = models.IntegerField('pressure', null=True)
    temperature = models.FloatField('temperature', null=True)
    wind_direction = models.IntegerField('wind_direction', null=True)
    wind_speed = models.IntegerField('wind_speed', null=True)
    description = models.CharField('description', max_length=250, null=True)


    class Meta:
        verbose_name = 'Описание погоды'
        verbose_name_plural = 'описания погоды'
        unique_together = ('datetime', 'city')


class Feedback(models.Model):
    email = models.EmailField(max_length=200)
    message = models.TextField(max_length=1000)

    class Meta:
        verbose_name = 'email'
        verbose_name_plural = 'Обратная связь'

    def __str__(self):
        return self.email


class Town(models.Model):
    TOWNS= [('Albuquerque','Альбукерке'),('Atlanta','Атланта'),
    ('Boston','Бостон'),('Dallas','Даллас'),('Denver','Денвер'),
    ('Detroit','Детройт'),('Jacksonville','Джексонвилль'),
    ('Indianapolis','Индианаполис'),('Kansas City','Канзас-Сити'),
    ('Las Vegas','Лас-Вегас'),('Los Angeles','Лос-Анджелес'),
    ('Miami','Майами'),('Minneapolis','Миннеаполис'),('New York','Нью-Йорк'),
    ('Nashville','Нэшвилл'),('Pittsburgh','Питтсбург'),('Portland','Портленд'),
    ('San Antonio','Сан-Антонио'),('San Diego','Сан-Диего'),
    ('San Francisco','Сан-Франциско'),('Saint Louis','Сент-Луис'),
    ('Seattle','Сиэтл'),('Phoenix','Феникс'),('Philadelphia','Филадельфия'),
    ('Houston','Хьюстон'),('Chicago','Чикаго'),('Charlotte','Шарлота'),

    ('Vancouver','Ванкувер'),('Montreal','Монреаль'),('Toronto','Торонто'),

    ('Beersheba','Беэр-Шева'),('Jerusalem','Иерусалим'),('Nahariyya','Нагария'),
    ('Tel Aviv District','Район Тель-Авива'),('Haifa','Хайфа'),('Eilat','Эйлат')
    ]

    town_ch = models.CharField(
        max_length=25,
        default = "Albuquerque",
        choices = TOWNS)

class Measurement(models.Model):
    temp =  models.CharField(
        max_length = 2,
        default = 'C',
        choices=(('C', "°C"), ('F', "°F"), ('K', "°K")),
    )

    pres = models.CharField(
        max_length = 10,
        default = 'mmrt',
        choices=(('mmrt', 'мм рт.ст.'), ('gektopa', 'гектоПа')),
        )

    speed = models.CharField(
        max_length = 5,
        default = 'mc',
        choices=(('mc', 'м/с'), ('kmch', 'км/ч')),
        )
