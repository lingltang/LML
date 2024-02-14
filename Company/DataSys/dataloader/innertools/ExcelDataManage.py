import pandas as pd
import copy
from dataloader.innertools import DE

# 合并字典中的内容
def concatdict(labledict: dict):
    lablels = list()
    for key in labledict.keys():
        lablels.extend(labledict[key])
    return lablels

class ExcelDataManage:
    def __init__(self):
        # 源数据
        self.sourceDfs = dict()
        # az数据
        self.azDfs = dict()

    def _selLabel(self,dfkey):
        if dfkey in self.sourceDfs.keys():
            return (True,self.sourceDfs[dfkey])
        elif dfkey in self.azDfs.keys():
            return (True,self.azDfs[dfkey])
        else:
            print(f'{dfkey}不存在数据列表中')
            return (False,None)

    # 通过路径加载df数据
    def loadPath(self,path,dfkey):
        try:
            df = pd.read_excel(path)
        except:
            print(f'路径错误:{path}')
            return 'PATH ERROR'
        if dfkey not in self.sourceDfs.keys():
            self.sourceDfs[dfkey] = df
            print(f'文件已打开\n数据路径:\t{path}\n数据名称:\t{dfkey}')
            return None
        return f'文件已打开,数据命名重复:{dfkey}'

    # 添加一个已有的数据
    def addDF(self,df:pd.DataFrame,dfkey):
        if dfkey not in self.sourceDfs.keys():
            self.azDfs[dfkey] = df
            print(f'df数据已载入\n数据名称:\t{dfkey}')
            return True
        return False

    # 删除一个存在的数据
    def delDF(self,dfkey):
        if dfkey in self.sourceDfs.keys():
            return self.sourceDfs.pop(dfkey)
        elif dfkey in self.azDfs.keys():
            return self.azDfs.pop(dfkey)
        else:
            return None

    # 过滤选取列数据
    def filterLabel(self,dfkey,labelList,newdfkey):
        res,df = self._selLabel(dfkey)
        if not res:
            return (False,f'{dfkey}不存在')
        mdflabels = df.columns
        inlabels = list()
        outlabels = list()
        for i in labelList:
            if i in mdflabels:
                inlabels.append(i)
            else:
                outlabels.append(i)
        if len(inlabels)>0:
            if newdfkey not in self.azDfs.keys():
                self.addDF(df[inlabels], newdfkey)
                return (True,outlabels)
            return (False,f'数据名称重复:{newdfkey}')
        return (False,'无对应标签')

    # 过滤
    def filterDF(self,dfkey,filterls:list,newdfkey):
        res, df = self._selLabel(dfkey)
        if not res:
            return (False, f'{dfkey}不存在')
        fdbls = []
        for filter in filterls:
            label,filt,fdata = filter
            if filt == '大于':
                fdbls.append(df[label] > fdata)
            elif filt == '小于':
                fdbls.append(df[label] < fdata)
            elif filt == '等于':
                fdbls.append(df[label].isin(fdata))
            else:
                print('格式错误\n正确格式为:\tlist[(标签名,过滤条件,数据)]')
                return (False,'格式模板错误')
        fdbl = fdbls.pop()
        for i in fdbls:
            fdbl&=i
        df = df[fdbl]
        if newdfkey not in self.azDfs.keys():
            self.addDF(df, newdfkey)
            return (True,df)
        return (False,f'数据名称重复:{newdfkey}')

    def dfApply(self,dfkey,newdfkey,label,fun,newlabel=None):
        res, df = self._selLabel(dfkey)
        if res is False:
            return (False,f'{dfkey}数据不存在')
        df = copy.deepcopy(df)
        if newlabel!=None:
            res = df[label].apply(fun)
            res.name = newlabel
            df = pd.concat([df, res], axis=1)
        else:
            df.loc[:,label] = df[label].apply(fun)
        if newdfkey not in self.azDfs.keys():
            self.addDF(df, newdfkey)
            return (True,df)
        return (False,f'数据名称重复:{newdfkey}')

    def dfgroupby(self,dfkey,labels:list,newdfkey):
        res, df = self._selLabel(dfkey)
        if res is False:
            return (False,f'{dfkey}数据不存在')
        df = df.groupby(labels)
        if newdfkey not in self.azDfs.keys():
            self.addDF(df, newdfkey)
            return (True,df)
        return (False,f'数据名称重复:{newdfkey}')

    # 合并数据
    def mergeDF(self,dfkeys:list,mainlabels:list,newdfkey:str):
        dfls = []
        for dfkey in dfkeys:
            res, df = self._selLabel(dfkey)
            if res is False:
                return (False, f'{dfkey}数据不存在')
            dfls.append(copy.deepcopy(df))
        df_all = pd.DataFrame()
        for df_m in dfls:
            df_all = pd.concat([df_all,df_m],axis=0)
        df = df_all.drop_duplicates(subset=mainlabels,inplace=False)
        if newdfkey not in self.azDfs.keys():
            self.addDF(df, newdfkey)
            return (True,df)
        return (False,f'数据名称重复:{newdfkey}')

if __name__ == '__main__':
    # path = r'C:\Users\ASUS\Desktop\TX0712.xlsx'
    # edm = ExcelDataManage()
    # edm.loadPath(path,'maindf')
    # # 过滤出对应的列进行输出
    # timelable = ['报修时间', '到达现场时间', '故障排除时间']
    # edm.filterLabel('maindf',timelable,'timedf')
    # # 时间队列
    # times = DE.DataRange(DE.STT(2024,1,1),4,DE.STTL(day=7),1)
    # print(times)
    # # 过滤数据
    # filters = [('报修类型','等于',['自查工单'])]
    # edm.filterDF('maindf',filters,'txdf')
    # print(edm.azDfs['txdf'])
    pass


