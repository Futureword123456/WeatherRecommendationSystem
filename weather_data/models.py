from django.db import models

# Create your models here.
from region.models import Region


#  用于记录天气数据的模型
class WeatherData(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    day_weather = models.CharField(max_length=20)
    day_weather_code = models.CharField(max_length=2)
    day_weather_short = models.CharField(max_length=20)
    day_wind_direction = models.CharField(max_length=20)
    day_wind_direction_code = models.CharField(max_length=2)
    day_wind_power = models.SmallIntegerField()
    day_wind_power_code = models.CharField(max_length=2)
    max_degree = models.FloatField()
    min_degree = models.FloatField()
    night_weather = models.CharField(max_length=20)
    night_weather_code = models.CharField(max_length=2)
    night_weather_short = models.CharField(max_length=20)
    night_wind_direction = models.CharField(max_length=20)
    night_wind_direction_code = models.CharField(max_length=2)
    night_wind_power = models.SmallIntegerField()
    night_wind_power_code = models.CharField(max_length=2)
    time = models.DateField()
    # 用于记录 天气数据是什么时候插入数据库的
    #  auto_now_add 自动的将 创建数据的时间 插入字段
    created = models.DateTimeField(auto_now_add=True)


class WeatherResult(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    result = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
