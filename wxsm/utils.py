#!/usr/bin/env python
# -*-coding:utf-8-*-
# author:sware
"""
工具箱：
日志、配置
"""

import os
import time
import logging


# log_path 是存放日志的路径
cur_path = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(os.path.dirname(cur_path),'logs')

# 如果logs文件夹不存在，就自动创建一个
if not os.path.exists(log_path): os.mkdir(log_path)

class Log(object):
    """
    # https://www.jianshu.com/p/8799aff60f24
    logging.basicConfig函数各参数：
    filename：指定日志文件名；
    filemode：和file函数意义相同，指定日志文件的打开模式，'w'或者'a'；
    format：指定输出的格式和内容，format可以输出很多有用的信息，
    参数：作用
    %(levelno)s：打印日志级别的数值
    %(levelname)s：打印日志级别的名称
    %(pathname)s：打印当前执行程序的路径，其实就是sys.argv[0]
    %(filename)s：打印当前执行程序名
    %(funcName)s：打印日志的当前函数
    %(lineno)d：打印日志的当前行号
    %(asctime)s：打印日志的时间
    %(thread)d：打印线程ID
    %(threadName)s：打印线程名称
    %(process)d：打印进程ID
    %(message)s：打印日志信息

    datefmt：指定时间格式，同time.strftime()；

    level：设置日志级别，默认为logging.WARNNING；

    stream：指定将日志的输出流，可以指定输出到sys.stderr，sys.stdout或者文件，默
    """
    def __init__(self,file=None):
        # self.log_path = log_path
        self.logname = os.path.join(log_path,"{}.log".format(
            time.strftime("%Y_%m_%d")))  # 当初始化时没有指定日志文件名称，默认使用时间作为名称
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        # 日志输出格式
        self.formatter = logging.Formatter('[%(asctime)s] - [%(filename)s - %(lineno)d line] - %(levelname)s: %(message)s')


    def __console(self, level, message):
        # if os.path.exists(self.logname): os.mkdir(self.logname)
        # 创建一个FileHandler，用于写到本地
        fh = logging.FileHandler(self.logname, 'a', encoding='utf-8')
        fh.setLevel(logging.INFO)
        fh.setFormatter(self.formatter)
        self.logger.addHandler(fh)

        # 创建一个StreamHandler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(self.formatter)
        self.logger.addHandler(ch)

        if level == 'info':
            self.logger.info(message)
        elif level == 'debug':
            self.logger.debug(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)
        else:
            raise Exception('only input info|debug|warning|error')
        # 此两行代码是为了避免日志输出重复的问题
        self.logger.removeHandler(ch)
        self.logger.removeHandler(fh)
        # 关闭打开的文件
        fh.close()


    def debug(self, message):
        self.__console('debug', message)


    def info(self, message):
        self.__console('info', message)

