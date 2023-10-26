import pandas
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import matplotlib.pyplot as plt
from typing import List


class AnalyzeData:
    def __init__(self, data, *handName, **parameter):
        self.data = data
        self.handname = self._loadData(handName,[])
        self.data_df = pd.read_csv(parameter['filepath'],sep=",")
        # 预处理数据
        #self.data = self.feature_process()

    '''
    显示数据图像
    '''
    # 显示条状统计图
    def pltbar(self, x, y):
        plt.bar(x, y)
        plt.xticks(range(len(x)), x)
        plt.show()

    # 显示点图
    def pltpoint(self, x, y):
        plt.scatter(x, y)
        plt.show()

    # 显示饼图
    def pltpie(self, x, lable=None, lableNum=0, pctdistance=0.6, pieinterval=1):
        # 通过lableSize区间确定pieinterval的值
        if lableNum == 0 or isinstance(lable, np.ndarray):
            print("auto operation pctdistance and lableNum")
            lableNum = x.size
            if lableNum > 20:
                pieinterval = 0.6
            elif lableNum > 10:
                pieinterval = 0.3
            elif lableNum > 2:
                pieinterval = 0.2
            else:
                pieinterval = 0.1
        # 分配每个扇区与中心的距离
        explode = [(i + 1) / lableNum * pieinterval for i in range(lableNum)]
        plt.pie(self, x, labels=lable, autopct="%0.2f%%", pctdistance=pctdistance, explode=explode)
        plt.show()

    '''
    数据处理
    包含阈值分阶
    '''

    # 获取类别大于阈值的数据
    def sparseData(self ,data_df, MaxCountNum=60, isplt=False):
        sparseList = []
        denceList = []
        # 类型少的数据分布
        for k in data_df.keys():
            # data_df_counts.append([k,data_df[k].value_counts()])
            if len(data_df[k].value_counts()) < MaxCountNum:
                if isplt:
                    mes_k_count = data_df[k].value_counts()
                    x = mes_k_count.index.values
                    y = mes_k_count.values
                    self.pltpie(y, lable=x)
                sparseList.append(k)
            else:
                denceList.append(k)
        return sparseList, denceList

    def getOneDataPie(self ,data_df, idx):
        # 数据样本与各类的相关性
        # datalist = data_df_counts[-1]
        if isinstance(idx, int):
            lablename = data_df.keys()[idx]
        else:
            lablename = idx
        mes_k_count = data_df[lablename].value_counts()
        x = mes_k_count.index.values
        y = mes_k_count.values
        self.pltpie(y, lable=x)
        # 返回各个类别的统计值以及对应的标签
        return y, x

    # 获取列表数据的图统计数据
    def getLableCount(self ,data_df, lablelist):
        labdic = dict()
        for lable in lablelist:
            mes_k_count = data_df[lable].value_counts()
            labdic[lable] = [mes_k_count.values, mes_k_count.index.values]
        # 返回结构{'lableName':[lableDataList,lableClassNameList]}
        return labdic

    # 获取含有空值的列标签
    def getNullList(self ,data_df):
        nullDataList = data_df.isnull().any()  # 查看数据是否有空值
        return nullDataList

    # 获取标签数据列表
    def getDataTypeList(self ,data_df, dt=np.dtype('O')):
        return data_df.dtypes[(data_df.dtypes == dt).values].index.values

    # 初始化映射数据
    def loadSTIMap(self ,lableList, completion=True):
        idx_n = 0
        stiMap = dict()
        lableList = np.unique(lableList)
        for i in lableList:
            stiMap[i] = idx_n
            idx_n += 1
        if completion:
            stiMap['@L'] = idx_n
        return stiMap

    # 通过数据字典转换id
    def exchangeSTI(self ,stiList, stiMap):
        sm = stiMap.keys()
        encodeList = []
        for i in stiList:
            if i not in sm:
                encodeList.append(sm[-1])
            else:
                encodeList.append(stiMap[i])
        return encodeList

    # 通过映射字典获取原值
    def exchangeITS(self ,itsList, stiMap):
        sm = stiMap.keys()
        recodeList = []
        for i in itsList:
            if i == sm[-1]:
                recodeList.append('Null')
            else:
                recodeList.append(stiMap[i])
        return recodeList

    # 根据生成id生成onehot编码
    def onehotITO(self ,itoList, maxlen):
        return torch.nn.functional.one_hot(torch.tensor(itoList), maxlen)

    # 根据onehot编码计算最大id
    def onehotOTI(stiList: List[int], stiMap):
        v, i = stiList.max()
        # 最大值，对应id
        return v, i

    '''
    
    '''
    # 预处理
    def feature_process(self, a: List[int]):
        pass

    # 查看数据基本信息
    def seeData(self, headNum = 5):
        print("="*50,'数据大小',"="*50)
        print(self.data_df.shape)
        print("="*50,'数据基本格式',"="*50)
        print(self.data_df.describe())
        print("="*50,f'数据前{headNum}项',"="*50)
        print(self.data_df.head(headNum))
        print("="*50,'各列数据类型',"="*50)
        print(self.data_df.dtypes)
        print("="*50,'各列是否存在空值',"="*50)
        for k in self.data_df.keys():
            if None in self.data_df[k].values:
                print(self.data_df[k].value_counts().keys)



    def defaultparam(self):
        print(self.handname)

    def _loadData(self, data, rData):
        return rData if data is None else data

if __name__ == '__main__':
    # ad = AnalyzeData([11], filepath='../data/onlineShop/online_shoppers_intention.csv')
    # ad.seeData()
    da = pd.DataFrame(torch.tensor([0,0,1]))
    print(da)