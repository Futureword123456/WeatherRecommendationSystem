import os
import django

#  手动启动django
# 设置配置环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather_analysis1.settings')

# 启动django
django.setup()
