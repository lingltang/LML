import pandas as pd

'''
未启用该模块
'''

class DFTL:
    def __init__(self,df:pd.DataFrame):
        self.df = df
        self.names = df.columns

    def dfapply(self,label,fun,newlabel=None):
        if newlabel!=None:
            self.df[newlabel] = self.df[label].apply(fun)
        self.df[label] = self.df[label].apply(fun)
        return self.df
    # 显示基本数据
    def showMes(self):
        print(self.df)
        print(self.names)

    # 获取某一列的数据类型
    def seeColTypes(self,colname):
        typesnum = dict()
        for i in self.df[colname]:
            typei = type(i)
            if typei in typesnum.keys():
                typesnum[typei] += 1
                continue
            typesnum[typei] = 0
        return typesnum

    # 获取某几列的数据类型
    def seeColsTypes(self,colList):
        resdict = dict()
        for i in colList:
            resdict[i] = self.seeColTypes(self.df,i)
        return resdict

if __name__ == '__main__':
    # print(DFTL(pd.read_excel(r'C:\Users\ASUS\Desktop\TX0712.xlsx')).df)
    pass