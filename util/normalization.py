# -*- coding: utf-8 -*-
# @Time : 2020/8/5 0005 9:11
# @Author : 杨华钟
# @Email : 2635681517@qq.com
# @File : normalization.py
import numpy as np


def sigmoid(X):
    return 1 / (1 + np.exp(-float(X)))


# 针对风力级数的归一化函数
def wind_power_normalization(level):
    if level < 2:
        return 0.6
    elif 2 <= level < 4:
        return 1
    elif 4 <= level < 6:
        return 0.3
    else:
        return 0


#  针对天气code进行归一化处理
def weather_type_normalization(code):
    if code in ['00', '01', '02']:
        return 1
    elif code in ['03', '04', '07', '08', '18', '21']:
        return 0.4
    elif code in ['09', '10', '22', '23', '24']:
        return 0
