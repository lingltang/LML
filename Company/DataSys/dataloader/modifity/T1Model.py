# coding:utf-8
import numpy as np

from dataloader.entity import Printer
from dataloader.innertools import DE
import pandas as pd
from dataloader.innertools.ExcelDataManage import ExcelDataManage as EDMCLS

# 转化文本到时间日
def ExcelSTT(strdata:str):
    try:
        return pd.Timestamp(strdata)
    except:
        print(f'数据格式错误:{strdata}')
    return pd.NA

# 转化文本到时间年
def ExcelSTTYEAR(indata:pd.Timestamp):
    try:
        return DE.TTS(indata)[0]
    except:
        print(f'数据格式错误:{indata}')
    return pd.NA

# 转化文本到时间月
def ExcelSTTMON(indata:pd.Timestamp):
    try:
        return DE.TTS(indata)[1]
    except:
        print(f'数据格式错误:{indata}')
    return pd.NA

# model-组统计
def tableGroupCountClssify():
    pass

if __name__ == '__main__':
    # 文件路径
    sourcefilepath = r'C:\Users\ASUS\Desktop\TXDATA.xlsx'
    # 创建核心
    EDM = EDMCLS()
    EDM.loadPath(sourcefilepath,'源数据')
    # 处理时间格式
    passtimelable = '报修时间'
    EDM.dfApply('源数据','正则化数据-1','报修时间',ExcelSTT)
    EDM.dfApply('正则化数据-1','正则化数据-2','报修时间',ExcelSTTYEAR,'年份')
    EDM.dfApply('正则化数据-2','正则化数据-3','报修时间',ExcelSTTMON,'月份')
    # 系统选择
    selsystem = ['中航信离港系统(T1)','工作人员通道人脸识别系统(T1)','T1航显系统','T1视频监控系统','T1出入口控制系统','T1广播系统','泊位引导系统(T1)','T1网络','全景视频监控系统','内通系统(T1)','航班查询系统(T1)','SITA离港系统','T1二维码核验设备','T1综合布线系统','T1海关视频监控设备','T1时钟系统','T1机房管理','生产实况系统（T1）','有线电视系统(T1)','T1大屏显示系统','T1云平台系统','机坪道口车辆识别系统(T1)','信息管理网(T1)','T1主网','T1离港网络','T1安检网络']
    filters = [('设备系统', '等于', selsystem)]
    EDM.filterDF('正则化数据-3', filters, '正则化数据-4')
    # 时间周期数据
    startTime = DE.STT(2024,2,3)
    selnumst = 4
    seldatast = DE.STTL(7)
    seldatalist = DE.DataRange(startTime,selnumst+1,seldatast,-1)[::-1]
    # 拆分数据
    # 每年/月报修总量数据
    filters = [('设备系统', '等于', selsystem)]
    EDM.filterDF('正则化数据-4', filters, '正则化数据-G')
    # EDM.dfgroupby('正则化数据-G', ['年份', '月份', '报修类型'], '月份统计-时间')
    # print('=============================')
    filters = [('报修时间','大于',DE.STT(2023,1,1)),('报修时间','小于',DE.STT(2023,9,1))]
    EDM.filterDF('正则化数据-G', filters, '正则化数据-GT')

    filters = [('报修时间','大于',DE.STT(2023,8,1)),('报修时间','小于',DE.STT(2024,3,1))]
    EDM.filterDF('正则化数据-G', filters, '正则化数据-GA')

    EDM.mergeDF(['正则化数据-GT','正则化数据-GA'],['主键'],'正则化数据-GTA')
    res = EDM.dfgroupby('正则化数据-GTA', ['年份', '月份', '设备'], '月份统计-时间')

    statisticsData = dict()
    # resl = list(res[1])
    # for sle in resl:
    #     print(sle[0],end='\t')
    #     print(sle[1].shape)
    # print('=============================')
    for i,e in res[1]:
        year,mon,typename = i
        h,_ = e.shape
        print(e)
        if typename not in statisticsData.keys():
            statisticsData[typename] = [[],[]]
        statisticsData[typename][0].append(f'{year}年{mon}月')
        statisticsData[typename][1].append(h)
    df_draw = pd.DataFrame()
    for sd in statisticsData.keys():
        df_m = pd.DataFrame(statisticsData[sd][1],index=statisticsData[sd][0],columns=[sd])
        df_draw = pd.concat([df_draw,df_m],axis=1)
    df_draw.fillna(0,inplace=True)
    print(df_draw)

    Printer.Printer().ShowBar({'月度数据':df_draw})
