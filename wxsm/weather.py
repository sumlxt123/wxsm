#!/usr/bin/env python
# -*-coding:utf-8-*-
# author:sware


"""
通过免费API 获取指定城市的天气预报
"""
import os
import json
import requests
from pypinyin import lazy_pinyin

import utils

city_path = os.path.dirname(os.path.abspath(__file__))
# print(city_path)

logger = utils.Log()

class WeatherApi(object):

    __instance = None

    def __init__(self):
        pass


    def __new__(cls, *args, **kwargs):
        """此判断用于实现单例模式，此方法不能继承：
        通过判断私有变量是否存在，如存在则直接返回，否则执行实例化
        """
        if not hasattr(cls, '__instance'):
            cls.__instance = object.__new__(cls, *args, **kwargs)
        return cls.__instance




    @classmethod
    def get_city_weather(cls, city_name='北京',day=1):
        """
        API:https://www.tianqiapi.com/api/?version=v1&cityid=101120201&city=青岛&ip=27.193.13.255&callback=
        参考资料：https://www.kancloud.cn/ccjin/yingq/603579
        其中ip测试应该对提取数据没有影响
        :return:
        """
        weather_message = []  #用于临时存放天气信息
        api_url = 'https://www.tianqiapi.com/api/?version=v1&cityid={0}&city={1}&ip=27.193.13.254&callback='
        city_name = ''.join(lazy_pinyin(city_name))
        city_id = cls.read_city(city_name)
        api_url = api_url.format(city_id,city_name)
        logger.debug('API url:{}'.format(api_url))

        try:
            city_weather_data = requests.get(api_url).json()
            message = ('{0}:\n\n{1}{2} {3} {4}\n'
                       '空气质量:{5}\n天气:{6} 温度{7} {8}{9}\n'
                       '空气指数:{10}\n'
                       '{11}:{12}{13}\n{14}:{15}{16}\n'
                       '温馨提示:{17}'
                       )
            for i in range(day+1):  # 当天数据与未来天气数据不同，因而使用if语句控制
                tmp = message.format( '未来第{}天天气'.format(i) if i else '今天天气' ,
                               city_weather_data['country'], city_weather_data['city'],
                               city_weather_data['data'][i]['date'],
                               city_weather_data['data'][i]['week'], '未知' if i else city_weather_data['data'][i]['air_level'],
                               city_weather_data['data'][i]['wea'], city_weather_data['data'][i]['tem'],
                               city_weather_data['data'][i]['win'][0], city_weather_data['data'][i]['win_speed'],
                               '未知' if i else city_weather_data['data'][i]['air'], city_weather_data['data'][i]['index'][0]['title'],
                               city_weather_data['data'][i]['index'][0]['level'],
                               city_weather_data['data'][i]['index'][0]['desc'],
                               city_weather_data['data'][i]['index'][3]['title'],
                               city_weather_data['data'][i]['index'][3]['level'],
                               city_weather_data['data'][i]['index'][3]['desc'],
                               '未知' if i else city_weather_data['data'][i]['air_tips']
                               )
                weather_message.append(tmp)
            print(weather_message[0])
            return weather_message
        except Exception as err:
            print('err message:{}'.format(err))
            logger.debug('err message:{}'.format(err))
            return None




    @classmethod
    def read_city(cls, city_name):
        """读取城市的json文件，返回城市编码"""
        with open(city_path+'/city.json') as f:
            city_list = json.load(f)

        for city in city_list:
            # 当找到与城市匹配的拼音时返回第一个匹配项id,当多音字时会有不准确的问题
            if city['cityEn'] == city_name:
                logger.debug('{0}对应的id值为:{0}'.format(city['cityEn'], city['id']))
                print(city['id'])
                return city['id']


if __name__ == "__main__":
    WeatherApi.get_city_weather()

