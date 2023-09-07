import pandas as pd
import numpy as np

class AnalyzeData:
    def __init__(self, data, *handName, **parameter):
        self.data = data
        self.handname = self._loadData(handName,[])
        self.data_df = pd.read_csv(parameter['filepath'],sep=",")
        # 解析数据
        #self.data = self.feature_process()

    def feature_process(self):
        pass

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
        print(self.data_df.isnull)



    def defaultparam(self):
        print(self.handname)

    def _loadData(self, data, rData):
        return rData if data is None else data

if __name__ == '__main__':
    ad = AnalyzeData([11], filepath='../data/onlineShop/online_shoppers_intention.csv')
    ad.seeData()