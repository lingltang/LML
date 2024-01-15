import pandas as pd
import numpy as np

# 获取某几列的数据类型
def seeColsTypes(data,colList):
    resdict = dict()
    for i in colList:
        resdict[i] = seeColTypes(data,i)
    return resdict

# 获取某一列的数据类型
def seeColTypes(data,colname):
    typesnum = dict()
    for i in data[colname]:
        typei = type(i)
        if typei in typesnum.keys():
            typesnum[typei] += 1
            continue
        typesnum[typei] = 0
    return typesnum

# 获取顺序数据类型统计
def seeSeriesTypes(data):
    typesnum = dict()
    for i in data:
        typei = type(i)
        if typei in typesnum.keys():
            typesnum[typei] += 1
            continue
        typesnum[typei] = 0
    return typesnum


def getCycleData(data,startTime:pd.Timestamp,endTime:pd.Timestamp,timeLabel:str):
    if endTime<=startTime:
        return None
    ress = data[timeLabel]>startTime
    resd = data[timeLabel]<endTime
    res = ress and resd
    return data[res]

