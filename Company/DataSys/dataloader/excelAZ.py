from dataloader.tool.exceltype import ExcelSTT, CyclesDay, ColTypes
import pandas as pd
import numpy as np

def getallLable(labledict:dict):
    lablels = list()
    for key in labledict.keys():
        lablels.extend(labledict[key])
    return lablels
class excelAZ:
    def __init__(self,path,readlable:dict):
        # 数据表头加载
        allLable = getallLable(readlable)
        # 载入数据表头到总表
        self.labledict = readlable
        # 读取数据
        self.df = pd.read_excel(path,usecols=allLable)
        # 临时使用的数据
        self.df_draw = None
        # 执行预处理
        self._reExcelTimeData()

    def _reExcelTimeData(self):
        for timelable in self.labledict['timelables']:
            self.df[timelable] = self.df[timelable].apply(ExcelSTT)

    # 加载周期数据
    def CycleList(self, cl: dict,isReturn:bool=False):
        clls = dict()
        for key in cl.keys():
            st = cl[key][0]
            et = cl[key][1]
            at = cl[key][2]
            clls[key]=(CyclesDay(st,et,at))
        if isReturn:
            return clls
        self.cycleDict = clls

    # 统计列信息
    def LayerCount(self,lableName:str):
        return self.df[lableName].value_counts()


    #
    def tableModify(self,xCountLable,tableFilter:dict = None):
        if tableFilter == None:
            self.df[xCountLable].value_counts()
        self.df_draw = self.FilterDf(tableFilter)[xCountLable].value_counts()
        return self.df_draw

    def FilterDf(self,selFilterList:dict):
        if selFilterList is None:
            return self.df
        df_t = self.df
        for key in selFilterList.keys():
            args = selFilterList[key]
            # g  大于
            # l  小于
            # e  等于
            for arg in args:
                selLable = key
                selValues = arg[1]
                if arg[0] == 'g':
                    filterD = df_t[selLable] > selValues[0]
                    df_t = df_t[filterD]
                elif arg[0] == 'l':
                    df_t = df_t[df_t[selLable] < selValues[0]]
                elif arg[0] == 'e':
                    # if len(selValues) == 1:
                    #     df_t = df_t[df_t[selLable] == selValues[0]]
                    # else:
                    #     df_ls = list()
                    #     for selValue in selValues:
                    #         df_ls.append(df_t[df_t[selLable] == selValue])
                    #     df_t = pd.concat(df_ls).drop_duplicates()
                    df_t = df_t[df_t[selLable].isin(selValues)]
                else:
                    print('模板格式错误')
        return df_t

    def ColType(self,lable):
        return ColTypes(self.df,lable)


if __name__ == '__main__':
    pass