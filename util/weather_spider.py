from datetime import datetime, timedelta

import util
import requests

# 根据区域城市 来获取7日天气数据：
from region.models import Region
from weather_analysis1.settings import TX_WEATHER_PARAMS, TX_WEATHER_URL, TX_WEATHER_HEADERS
from weather_data.models import WeatherData


def get_weather_by_region(region: Region):
    """
    根据区域获取天气信息
    :param region: 传一个区域model对象
    :return: 返回7日天气信息的字典
    """
    params = TX_WEATHER_PARAMS
    params["province"] = region.get_province_name()
    params["city"] = region.name
    res = requests.get(TX_WEATHER_URL, params=params, headers=TX_WEATHER_HEADERS)
    return res.json()["data"]["forecast_24h"]


def get_weather_by_display_regions():
    """
    爬取要在地图上展示的城市的7日天气数据
    :return:
    """
    # 获取要展示的城市的region的列表
    region_list = Region.objects.filter(is_display=True)
    # region_list = Region.objects.all()
    # 对区域进行遍历，根据区域列表中的区域，调用爬取函数进行天气数据的爬取
    for r in region_list:
        data = get_weather_by_region(r)
        if data:
            #  把天气数据保存到数据库中
            for v in data.values():
                WeatherData.objects.create(region=r, **v)
                print("%s天气已经成功保存" % r.name)


def delete_weather_by_region(region: Region):
    """
    根据区域信息，删掉从当前时间开始 前一天到后6天的天气数据
    :param region:
    :return:
    """
    start = datetime.now() - timedelta(days=1)
    end = datetime.now() + timedelta(days=6)
    data = WeatherData.objects.filter(time__gte=start, time__lte=end, region=region)
    if data.count() > 0:
        print(data.delete())


def delete_weather_all():
    start = datetime.now() - timedelta(days=1)
    end = datetime.now() + timedelta(days=6)
    data = WeatherData.objects.filter(time__gte=start, time__lte=end)
    if data.count() > 0:
        print(data.delete())


if __name__ == '__main__':
    # wh = Region.objects.get(name="武汉市")
    # print(get_weather_by_region(wh))
    # get_weather_by_display_regions()
    # print(delete_weather_by_region(wh))
    # delete_weather_all()
    get_weather_by_display_regions()
