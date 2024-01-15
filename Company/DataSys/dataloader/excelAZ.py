from dataloader.tool.exceltype import ExcelSTT, CyclesDay, ColTypes
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

def getallLable(labledict:dict):
    lablels = list()
    for key in labledict.keys():
        lablels.extend(labledict[key])
    return lablels
class excelAZ:
    def __init__(self,path,readlable:dict):
        allLable = getallLable(readlable)
        self.labledict = readlable
        self.df = pd.read_excel(path,usecols=allLable)
        self.df_draw = None
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

    # 执行周期抽取（未完成）
    def RunData(self):
        if self.cycleDict is None:
            print('无数据')
        else:
            for i in self.cycleDict.keys():
                pass

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

    # color: 指定颜色，可以是颜色名称或十六进制值。
    # edgecolor: 条形边缘的颜色。
    # linewidth: 条形轮廓的宽度。
    # alpha: 条形的透明度。
    # hatch: 特定样式的条形（例如斜线）。
    # plt.xticks(rotation=0)  # 将x轴刻度标签旋转为垂直显示
    # plt.ylabel('值')  # 设置y轴标签

    def DataToOneDf(self,df_ls:list,axis = 0):
        # df_re = df_ls.pop()
        # for df in df_ls:
        #     df_re = pd.merge(df_re,df,on='state')
        # self.df_draw = df_re
        # return df_re
        self.df_draw = pd.concat(df_ls[0],axis=axis)
        self.df_draw.columns = df_ls[1]
        self.df_draw.fillna(0,inplace=True)
        return self.df_draw

    def Drawbar(self):
        pd.DataFrame().index.values
        df = self.df_draw
        evdata = [df[key] for key in df.keys()]
        evlabel = df.index.values
        self.__DrawBar(evdata,evlabel)
        # plt.xticks(rotation=45, ha='right')
        # plt.show()

    def __DrawBar(self,evData,evLabel):
        lognum = len(evLabel) #6
        print(evLabel)
        logvaluenum = len(evData[0].values) #48
        y_xy = np.arange(lognum)
        x_xy = np.arange(logvaluenum)
        width = 0.1
        wide = 0.1
        for i in range(6):
            # print(list(evData[i].values))
            plt.bar(x_xy+width*(i-lognum/2),list(evData[i].values),wide,label=evLabel[i])
        plt.xticks(y_xy,labels=evLabel)
        plt.xticks(rotation=45, ha='right')
        plt.show()
    def Drawplot(self,df_lable_ex:list = None):
        df = self.df_draw.T
        df_labels = list()
        df_null = list()
        if df_lable_ex == None:
            df_labels = df.keys().values
        else:
            df_tx = df_lable_ex
            for label in df_tx:
                if label in df.keys().values:
                    df_labels.append(label)
                else:
                    df_null.append(label)
        for df_create_null in df_null:
            df[df_create_null] = pd.Series()
            df_labels.append(df_create_null)
        print(df)
        self.df_draw.fillna(0, inplace=True)
        print(df_labels,len(df_labels))
        m_fd = 4
        m_jg = int(len(df_labels)/m_fd)+1
        m_fdid = [m_jg*i for i in range(m_fd)]
        m_fdid.append(len(df_labels))
        m_limlsy = [[0,50],[0,20],[0,20],[0,20]]
        for i in range(m_fd):
            label = df_labels[m_fdid[i]:m_fdid[i+1]:1]
            print(label)
            df_v = df[label]

            ylables = label
            plt.plot(df_v)
            plt.ylim(m_limlsy[i])
            plt.legend(ylables)
            plt.xticks(rotation=45, ha='right')
            plt.show()
        plt.plot(df)
        plt.legend(df_labels)
        plt.xticks(rotation=45, ha='right')
        plt.show()

if __name__ == '__main__':
    pass