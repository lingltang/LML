from typing import Tuple

import pandas
import pandas as pd
import numpy as np

# DataExchange
# 建立一个日期数据
def STT(year:int=1970,month:int=1,day:int = 1,hour:int=0,minute:int=0,second:int=0)->pd.Timestamp:
    '''
    创建时间数据，外加截断时间仅保留日期
    '''
    if(hour != 0 or minute != 0 or second != 0):
        return pd.Timestamp(f'{year}-{month}-{day} {hour}:{minute}:{second}')
    else:
        return pd.Timestamp(f'{year}-{month}-{day}')

# 解析时间数据
def TTS(timedata:pd.Timestamp)-> Tuple[int, int, int, int, int, int]:
    '''
    转换数据出
    :param timedata:pd.Timestamp
    :return:[年，月，日，时，分，秒]
    '''
    return (timedata.year,timedata.month,timedata.day,timedata.hour,timedata.minute,timedata.second)

def CT(timedata:pd.Timestamp):
    timels = TTS(timedata)
    return STT(timels[0],timels[1],timels[2])

# 生成用于计算的时间
def STTL(day:int = 0,hour:int=0,minute:int=0,second:int=0)->pd.Timedelta:
    return pd.Timedelta(days=day,hours=hour,minutes=minute,seconds=second)

# 解析用于计算的时间格式
def TLTS(intime:pd.Timedelta)-> Tuple[int, int, int, int]:
    indata_sec = intime.seconds
    return (intime.days,indata_sec//3600,indata_sec%3600//60,indata_sec%60)

# 生成周期数据
# direction正1为向后推演时间，负1为向前推演时间
def DataRange(dayPoint:pandas.Timestamp,tCycleNum:int,timesignal:pandas.Timedelta,direction:int=1):
    if (tCycleNum < 1):
        direction *= (-1)
        tCycleNum *= (-1)
    dayList = [dayPoint + timesignal * direction * i for i in range(tCycleNum)]
    return dayList

if __name__ == '__main__':
    # 创建一个时间周期
    # d = DataRange(STT(2023,12,31,11,22,33),3,STTL(1))
    # print(d)
    pass