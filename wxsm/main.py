#!/usr/bin/env python
# -*-coding:utf-8-*-
# author:sware

"""程序入口"""

import time
import utils
import weixin
import xinlang
from weather import WeatherApi


logger = utils.Log()

def main():
    remid_price = {'sz000009':{'hid':7.10,'low':6.6},}
    stock = 'sz000009'
    new_day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    new_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    wx = weixin.WeiXin()  # 初始化微信推送类
    while True:
        # 股票信息推送
        if ((new_day + ' 09:30:00') <= new_date <= (new_day + ' 11:30:00')) \
            or ((new_day + ' 13:00:00') <= new_date <= (new_day + ' 15:30:00')):
            stock_mes = xinlang.SinaJsApi.stock_real_time_data(stock)
            if remid_price[stock]['hid'] >= float(stock_mes[4].replace("'",'')):
                message = "{0}({1})在{2}最高价格为{3}".format(stock_mes[1],stock_mes[0],new_date,stock_mes[4])
                try:
                    wx.send_messages(message=message)  # 推送微信消息
                except Exception as err:
                    # print(err)
                    pass
        else:
            # logger.info('test log')
            pass

        # 天气信息推送
        if time.strftime('%H:%M:%S')=='06:00:00' or time.strftime('%H:%M:%S')=='12:00:00' \
            or time.strftime('%H:%M:%S') == '17:20:00':
            weather_message = WeatherApi.get_city_weather('北京',1)
            try:
                for i in weather_message:
                    wx.send_messages(weather_message[i])
            except Exception as err:
                # print(err)
                pass









if __name__ == "__main__":
    main()
