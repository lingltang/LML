from typing import Union, List, Tuple

import pandas
import pandas as pd
import numpy as np
from pandas import Timestamp


# 建立一个日期数据
def STT(year:int=0,month:int=0,day:int = 0,hour:int=0,minute:int=0,second:int=0)->pd.Timestamp:
    '''
    自动适配数据，生成对应时间
    :param year: 年
    :param month: 月
    :param day: 日
    :param hour: 时
    :param minute: 分
    :param second: 秒
    :return:
    '''
    if(hour != 0 or minute != 0 or second != 0):
        return pd.Timestamp(f'{year}-{month}-{day} {hour}:{minute}:{second}')
    else:
        return pd.Timestamp(f'{year}-{month}-{day}')

def TTS(timedata:pd.Timestamp)-> Tuple[int, int, int, int, int, int]:
    '''
    转换数据出
    :param timedata:pd.Timestamp
    :return:[年，月，日，时，分，秒]
    '''
    return (timedata.year,timedata.month,timedata.day,timedata.hour,timedata.minute,timedata.second)

# 转化文本到时间日
def ExcelSTT(strdata:str):
    '''
    用于转换pd.DataFrame的数据
    :param strdata: 默认转换str数据
    :return:
    '''
    try:
        return pd.Timestamp(strdata)
    except:
        print(f'数据格式错误:{strdata}')
    return pd.NA

# 创建一个时间周期
def DayRange(startDay,number,freq='D'):
    return pd.date_range(startDay, periods=number, freq=freq)

def DayNearByDay(dayPoint:pandas.Timestamp,tCycleNum:int,tCycleDay:int,direction:int=-1):
    '''
    本函数用于生成某一时间点，向前或向后的周期时间点
    :param dayPoint: 时间点
    :param tCycleNum: 周期个数
    :param tCycleDay: 周期时长
    :param direction: 方向，正1为向后推演时间，负1为向前推演时间
    :param freq: 时间周期
    :return:
    '''
    if(tCycleNum<1):
        direction*=(-1)
        tCycleNum*=(-1)
    addtime = pd.Timedelta(days=tCycleDay)
    dayList = [dayPoint+addtime*direction*i for i in range(tCycleNum)]
    return dayList

# 时间差计算
def Subtime(startTime:pd.Timestamp,endTime:pd.Timestamp,tla = 'm'):
    tl = (endTime-startTime).to_numpy().item().total_seconds()
    if tla == 's':
        return tl
    if tla == 'm':
        return tl/60
    if tla == 'h':
        return tl/3600
    if tla == 'd':
        return tl/86400
    else:
        return tl

# 转换周期数据：起始日期每次增加周期量直到大于末周期
def CyclesDay(startTime:pd.Timestamp,endTime:pd.Timestamp,addCycle=1,instartdata = True,inenddata = True):
    '''
    :param startTime: 开始时间
    :param endTime: 结束时间
    :param addCycle: 周期长度（天）
    :param instartdata: 是否包含非标准起始时间（时分秒不为0），为True时往后延长一天
    :param inenddata: 是否包含最后日期
    :return:
    '''
    cdls = list()
    # 将不规则时间归至0时
    syear, smonth, sday, shour, sminute, ssecond = TTS(startTime)
    eyear, emonth, eday, ehour, eminute, esecond = TTS(endTime+pd.Timedelta(days=1))
    startTime = STT(syear,smonth,sday)
    if addCycle < 0:
        cdls.append(startTime)
        if ehour !=0 or eminute !=0 or esecond !=0:
            cdls.append(STT(eyear,emonth,eday))
        else:
            cdls.append(endTime)
    else:
        addTime = pd.Timedelta(days=addCycle)
        if shour != 0 or sminute != 0 or ssecond != 0:
            if instartdata:
                startTime += addTime
        while startTime < endTime:
            cdls.append(startTime)
            startTime += addTime
        if inenddata:
            if startTime>endTime:
                cdls.append(startTime)
    return cdls

#################################################################################
# 列出数据某一类数据类型的统计
def ColTypes(data,colname):
    typesnum = dict()
    for i in data[colname]:
        typei = type(i)
        if typei in typesnum.keys():
            typesnum[typei] += 1
            continue
        typesnum[typei] = 0
    return typesnum


if __name__ == '__main__':
    print(np.zeros(7))
    # tx = DayNearByDay(STT(2024,1,1),2,7)
    # for i in tx:
    #     print(i)
    # print(tx)
