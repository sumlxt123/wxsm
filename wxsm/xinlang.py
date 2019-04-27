#!/usr/bin/env python
# -*-coding:utf-8-*-
# author:sware
# 用于通过新浪股票信息API获取指定股票价格及浮动

"""
抓取指定股票日指定交易日的信息，并将数据写入数据库
股票代码、交易日期、开盘价、收盘价、最高价、最低价、涨幅
新浪接口参考资料
https://blog.csdn.net/Llingmiao/article/details/79941066
https://blog.csdn.net/zai_yuzhong/article/details/51735769
https://www.sinacloud.com/doc/api.html#jie-kou-lie-biao
"""
import re
import time
import json
import requests

from utils import Log

logger = Log()

class SinaJsApi(object):
    """
    此类使用新浪sinajs接口，获取指定股票的信息
    http://finance.sina.com.cn/realstock/company/sz002095/qianfuquan.js?d=2015-06-16
    """
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}

    def __init__(self, stock=None, start_date=None, end_date=None, fq=False, sinajs=None):
        """
        :param stock: 股票代码
        :param start_date: 开始时间
        :param end_date: 结束时间
        :param fq: 是否复权
        :param sinajs: 新浪接口
        """
        self._stock = stock
        self._start_date = start_date
        self._end_date = end_date
        self._fq = fq
        self.__sinajs = (sinajs if None else 'http://finance.sina.com.cn/realstock/company/{0}/{1}.js?d={1}')


    def get_his_data(self, stock=None, date=None, fq=True):
        """获取指定股票的前复权股票价格"""
        if stock is None and date is None :
            new_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            url = self.__sinajs.format(self._stock, 'qianfuquan', new_date)
            logger.info("url:{}".format(url))
            rep = requests.get(url=url, headers=self.headers)
            m = re.findall(r'data\:(.*)}\]',rep.text) # 获取需要的字符串
            m = m[0].replace('{_','{"').replace('",_',',"').replace(':"','":')
            m = json.loads(m.replace('_','-').replace('"}','}')) # 将字典的key添加“” 并使用json模块，处理成字典


    @classmethod
    def stock_real_time_data(cls,stock=None):
        """
        获取指定股票的实时价格，返回股票的价格和成交价格
        :param stock:股票id
        :return:返回列表
        """
        stock_price = []
        url = 'http://hq.sinajs.cn/list={0}'
        if stock is None:  # 当输入不为空，且为列表时使用for循环获取
            raise Exception("stock input is empty value.")
        url = url.format(stock)
        repson = requests.get(url=url, headers=cls.headers)
        logger.info(repson.text)
        m = re.findall(r'hq_str_(.*)="(.*)"',repson.text)
        stock_price.append(m[0][0])
        stock_price.extend(m[0][1].split(','))  # 将接口获取的值转换为列表
        logger.debug(stock_price)
        return stock_price



    @classmethod
    def zhishu_real_time_data(cls):
        """
        获取常见指数的实时点数
        :return:返回列表
        """
        url = 'http://hq.sinajs.cn/list={0}'
        zhishu_dict = {}
        zhishu_list = []
        zhishu = ['s_sh000001','s_sz399001','s_sz399300','s_sz399006','int_hangseng','s_sz399005',
                  'int_ftse','int_nikkei','int_dji','int_nasdaq','int_sp500']
        for i in zhishu:
            try:

                resp = requests.get(url=url.format(i))
                if resp.status_code == 200:
                    # print(resp.text)
                    if i[0] == 's':
                        zhishu_list.append(re.findall(r'_s_(.*)=', resp.text)[0])
                    else:
                        zhishu_list.append(re.findall(r'_int_(.*)=', resp.text)[0])
                    zhishu_list.extend(re.findall(r'="(.*)"', resp.text)[0].split(','))
                    logger.info(zhishu_list)
                    zhishu_dict[zhishu_list[1]] = zhishu_list
                    zhishu_list = []
                else:
                    logger.info('防止访问过快，延迟5s.......')
                    time.sleep(5)
            except Exception as err:
                logger.info(err)
        logger.debug('股票信息:\n{}'.format(zhishu_dict))
        return zhishu_dict


















if __name__ == "__main__":
    # a = SinaJsApi('sz000009')
    # a.get_his_data(fq=True)

    SinaJsApi.stock_real_time_data('sz000009')
    SinaJsApi.zhishu_real_time_data()
    main()

    pass

