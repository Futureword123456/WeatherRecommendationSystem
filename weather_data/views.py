from datetime import datetime, timedelta

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.template.defaultfilters import first

from region.models import Region
from util.weather_analysis import caculate_region_result
from util.weather_spider import delete_weather_by_region, get_weather_by_region
from weather_analysis1.settings import WEATHER_DATE_START, WEATHER_DATE_END
from weather_data.form import RegionForm
from weather_data.models import WeatherData, WeatherResult


def region_weather(request, region_id):
    region = Region.objects.get(id=region_id)
    region_list = Region.objects.filter(level='0')

    if request.method == 'POST':
        # 使用表单对象 处理用户发来的表单数据
        form = RegionForm(request.POST)
        # 对表单的数据做校验的is_valid()，返回True或False
        #  is_valid()方法 把校验成功的数据，转换成可用的数据类型，放在表单对象的cleaned_data的属性中
        if form.is_valid():
            region.latitude = form.cleaned_data.get('latitude')
            region.longtitude = form.cleaned_data.get('longtitude')
            region.is_display = form.cleaned_data.get('is_display')
            region.save()
            messages.success(request, '城市信息修改成功！', extra_tags='success')
        else:
            messages.error(request, '输入的数据有误，修改失败！', extra_tags='danger')
        #  重定向响应 以get请求方式 跳回原页面
        return HttpResponseRedirect(request.path)
    #  查出该地区 最近八天的天气数据
    data = WeatherData.objects.filter(region_id=region_id,
                                      time__range=(WEATHER_DATE_START, WEATHER_DATE_END))
    if data.count() < 8:
        # 清除一下 该地区在数据库中的老数据
        delete_weather_by_region(region)
        new_data = get_weather_by_region(region)
        for v in new_data.values():
            WeatherData.objects.create(region=region, **v)
        data = WeatherData.objects.filter(region_id=region_id,
                                          time__range=(WEATHER_DATE_START, WEATHER_DATE_END))
        # 查询该地区是否计算出天气推荐指数
    if not region.weatherresult_set.filter(created__day=datetime.now().day):
        WeatherResult.objects.create(region=region, result=caculate_region_result(region))

    context = {
        'region': region,
        'data': data,
        'region_list': region_list
    }

    # render 快捷函数  会把请求对象， 模板路径 、上下文 渲染成响应对象
    return render(request, 'weather_table.html', context)
    # template = loader.get_template('weather_table.html')
    # return HttpResponse(template.render(context))


def max_degree(request):
    region_list = Region.objects.filter(is_display=True)
    # 生成最高温的数据列表
    data = []
    for r in region_list:
        dic = {'name': r.name,
               'value': r.weatherdata_set.filter(time=datetime.now() + timedelta(days=1))
                   .first().max_degree
               }
        data.append(dic)
    geo_coord = {}
    for r in region_list:
        geo_coord[r.name] = [r.longtitude, r.latitude]

    context = {
        'data': data,
        'geo_coord': geo_coord,
        'title': '全国主要城市明日高温情况',
        'num': 1.2,
        'color': 'orangered',
        'name': '高温℃'
    }
    return render(request, 'maxDegreeMap.html', context)


# 最低温
def min_degree(request):
    region_list = Region.objects.filter(is_display=True)
    # 生成最高温的数据列表
    data = []
    for r in region_list:
        dic = {'name': r.name,
               'value': r.weatherdata_set.filter(time=datetime.now() + timedelta(days=1))
                   .first().min_degree
               }
        data.append(dic)
        print(dic)
    geo_coord = {}
    for r in region_list:
        geo_coord[r.name] = [r.longtitude, r.latitude]

    context = {
        'data': data,
        'geo_coord': geo_coord,
        'title': '全国主要城市明日高温情况',
        'num': 1.2,
        'color': 'blue',
        'name': '低温℃'
    }
    return render(request, 'minDegreeMap.html', context)


# 风力图
def day_wind_power(request):
    region_list = Region.objects.filter(is_display=True)
    data = []

    for r in region_list:
        dic = {
            'value': r.weatherdata_set.filter(time=datetime.now() + timedelta(days=1))
                .first().day_wind_power
        }
        value = list(dic.values())
        for i in value:
            data.append(i)
            print(i)
    context = {
        'data': data,
    }
    return render(request, 'windForce.html', context)


# 推荐
def recommend(request):
    region_list = Region.objects.filter(is_display=True)
    data = []
    for r in region_list:
        dic = {'name': r.name,
               'value': r.weatherresult_set.first().result
               }
        data.append(dic)
    geo_coord = {}
    for r in region_list:
        geo_coord[r.name] = [r.longtitude, r.latitude]

    context = {
        'data': data,
        'geo_coord': geo_coord,
        'title': '全国主要城市天气旅游推荐指数',
        'subtitle': '根据未来6天天气情况，计算出是否适合旅游',
        'num': 3,
        'color': 'yellow',
        'name': '推荐指数'
    }
    return render(request, 'reCommend.html', context)
