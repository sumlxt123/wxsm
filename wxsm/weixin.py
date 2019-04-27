#!/usr/bin/env python
# -*-coding:utf-8-*-
# author:sware

"""
实现企业微信消息推送类，文字、图片等
"""

import requests

# 自定义模块
import settings
from utils import Log

logger = Log()


class WeiXin(object):
    """
    定义微信的消息类，实现创建连接，访问，推送文字信息，推送图片信息
    官方文档：https://work.weixin.qq.com/api/doc#90000/90135/90236
    """
    api_url = "https://qyapi.weixin.qq.com"

    # 定义推送消息结构
    values = {
        "touser": '@all',
        "msgtype": 'text',
        "agentid": 1000002,
        "safe": 0
    }


    def __init__(self):
        # token API
        self.token_url = "{url}/cgi-bin/gettoken?corpid={corpid}&corpsecret={corpsecret}".format(
            url=self.api_url, corpid=settings.WEIXI['corpid'], corpsecret=settings.WEIXI['corpsecret']
        )
        logger.debug("token_usr:{0}".format(self.token_url))
        # 获取 token
        self.token = self.__get_token()
        logger.debug("access_token:{0}".format(self.token))
        # send messages API
        self.send_url = ('{url}/cgi-bin/message/send?access_token={access_token}'.format(
            url=self.api_url, access_token=self.token))


    def __get_token(self):
        """获取用户 access_token
        后期需要考虑，access_token 失效，以及请求超时的处理
        """
        return requests.get(self.token_url).json()['access_token']


    def send_messages(self, message=None, subject=None):
        """
        指定发送信息，与主题，当未指定时发送一条测试数据
        消息内容，最长不超过2048个字节，超过将截断
        特殊说明：其中text参数的content字段可以支持换行、以及A标签，即可打开自定义的网页（可参考以上示例代码）
        (注意：换行符请用转义过的\n)
        :param message: 消息
        :param subject: 主题
        :return:
        """
        message_value = self.values
        if subject is None :
            subject = '主题\n'
        if message is None:
            message = 'message'
        logger.debug('subject:{}message:{}'.format(subject,message))
        message_value['text']= {'content': "{0}\n{1}\n推送消息".format(subject, message)}
        errcode = requests.post(url=self.send_url,json=message_value).json()['errcode']

        if not errcode:
            logger.info('judge_request errcode values:{} ,Succesfully!'.format(errcode))
        else:
            logger.error(u'judge_request errcode values:{} ,Failed!'.format(errcode))
        return None


    def send_image(self, media_id=None):
        pass

















if __name__ == "__main__":
    weixin = WeiXin()
    weixin.send_messages(message='老虎看家，上市公司保障',subject='天下奇闻')
