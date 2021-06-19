#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lz
# Description:升降机次数测试脚本

import re
import time

import serial
from loguru import logger


def up():
 
    ser = serial.Serial("COM4", 9600, timeout=0.5)
    ser.flushInput() # 清空缓冲区
    ser.write('@21N#\r\n'.encode()) # 上升摄像机
    time.sleep(3)
    ser.write('@22N#\r\n'.encode()) # 打开电机
    logger.debug("上升摄像机")
    while True:
        line = ser.read(ser.in_waiting).decode("utf-8") # 读取缓冲区的指令
        # logger.debug(line)
        if (re.search('@51N#', line)): # 从接收的信息中查找
            ser.write('@22F#\r\n'.encode()) # 关闭电机
            logger.debug("检测到上光耦，关闭电机")
            ser.close()
            break
        else:
            pass

def down():
 
    ser = serial.Serial("COM4", 9600, timeout=0.5)
    ser.flushInput() # 清空缓冲区
    ser.write('@21F#\r\n'.encode()) # 下降摄像机
    time.sleep(3)
    ser.write('@22N#\r\n'.encode()) # 打开电机
    logger.debug("下降摄像机")
    while True:
        line = ser.read(ser.in_waiting).decode("utf-8") # 读取缓冲区的指令
        # logger.debug(line)
        if (re.search('@52N#',line)): # 从接收的信息中查找
            ser.write('@22F#\r\n'.encode()) # 关闭电机
            logger.debug("检测到下光耦，关闭电机")
            ser.close()
            break
        else:
            pass

def test():

    ser = serial.Serial("COM4", 9600, timeout=0.5)
    ser.write('@17F#\r\n'.encode()) # 打开灯带
    time.sleep(3)
    ser.write('@17N#\r\n'.encode()) # 关闭灯带
    logger.debug('灯带状态：' + ser.readline().decode('utf-8'))
    ser.close()

time_tup=time.localtime(time.time()) # 获取当前时间
format_time="%Y-%m-%d_%H%M%S"
cur_time=time.strftime(format_time,time_tup)
 
if __name__ == '__main__':

    logger.add('log_{}.txt'.format(cur_time), rotation="10 MB") # 将日志输出到txt文本中
    count = 0
    for i in range (0, 1): # 对函数做循环
        up()
        time.sleep(3) # 升降机转向需要3秒缓冲
        down()
        time.sleep(3)
        count += 1
        logger.info("已完成 --- > 第" + str(count) + "次")

