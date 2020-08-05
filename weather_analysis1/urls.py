"""weather_analysis1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os

from django.conf.urls import url
from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from weather_analysis1 import settings
from weather_data.views import region_weather, max_degree, min_degree, day_wind_power, recommend

urlpatterns = [
    path('recommend/', recommend),
    path('admin/', admin.site.urls),

    # 用于获取地区天气数据
    path('region/<int:region_id>', region_weather),

    path('max_degree/', max_degree),
    path('min_degree/', min_degree),
    path('day_wind_power/', day_wind_power),
    # url(r'^favicon\.ico$', RedirectView.as_view(url=r'/static/image/favicon.ico'))


]

# 配置静态文件的路由（从配置文件里读取配置项再进行操作）：
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)

#  另外一种配置静态文件路由的方式（直接写死）
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# urlpatterns += static('/static/', document_root=[
#     os.path.join(BASE_DIR, "static"),
# ])
