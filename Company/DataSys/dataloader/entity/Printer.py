import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pylab as pl
from typing import Tuple

# 配置matplotlib默认显示
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

class Printer:
    def __init__(self):
        self.plt = None

    # 柱状图    输入字典{主键:数据}
    def ShowBar(self,data,indexname=None,isPrintLabel=True,fontsize = 12,title = '',ytitle = '',xtitle='',fingersize:Tuple[int, int] =(22.4, 12.6),rotation=0,savepath:str=''):
        # 设置绘制图像大小
        plt.figure(figsize=fingersize)
        # 分列、堆叠（如果出现错误请检查传入参数shape是否一致）
        data_groupname = list(data.keys())
        if indexname is None:
            xlabel = data[data_groupname[0]].index.tolist()
        else:
            xlabel = indexname
        data_namelabel = [data[i].columns.tolist() for i in data_groupname]
        # 提取数据
        datavalues = pd.concat([i for i in data.values()], axis=1)
        # 列序号
        xlabelPoint = [x for x, _ in enumerate(xlabel)]
        # 配置绘图数据
        pltcolor = ['#D5D5D5', '#F5CD78', '#F4C1BC', '#D8CCE3', '#A7CF9A', '#F4E8A7', '#CAE5EE', '#E77F98', '#F8CC9C',
                    '#D1E1EF', '#A8D3E8', '#F3BECB', '#99B4D7']
        colorid = 0
        # 组数、记录数、组总宽度、记录宽度
        pltgrouplen = len(xlabel)
        plttakelen = len(data_namelabel)
        pltgroupinterval = 0.8
        plttakewidth = pltgroupinterval / plttakelen
        xlabellengthstart = plttakewidth * (plttakelen - 1) / 2
        # 中间间隔添加    左间隔、右间隔
        plttakeintrval = plttakewidth * 0.05
        plttakerealwidth = plttakewidth - plttakeintrval
        # 绘制登高线
        plt.grid(axis='y',which='major',linestyle = '--')
        # 绘制图像
        # edgecolor: 条形边缘的颜色。
        # linewidth: 条形轮廓的宽度。
        # alpha: 条形的透明度。
        takeid = 0
        for ils in data_namelabel:
            bottoms = np.zeros(pltgrouplen)
            xlabelPoint_now = [i - xlabellengthstart + plttakewidth * takeid for i in xlabelPoint]
            takeid += 1
            for i in ils:
                plt.bar(xlabelPoint_now, datavalues[i].tolist(), width=plttakerealwidth, label=i,
                        color=pltcolor[colorid%len(pltcolor)], bottom=bottoms,edgecolor='black',linewidth=0.5)
                # 数据标签
                if isPrintLabel:
                    for x1, y1, z in zip(xlabelPoint_now, bottoms + [i / 2 for i in datavalues[i].tolist()],
                                         datavalues[i].tolist()):
                        plt.text(x1, y1, str(z), ha='center', va='bottom', fontsize=fontsize)

                colorid += 1
                bottoms += datavalues[i].tolist()
        # 图例标签位置
        # 行标签名称
        plt.xlabel(xtitle,fontsize = fontsize+5)
        # 设置坐标轴及标签
        if rotation==0:
            plt.xticks(xlabelPoint, xlabel)
        else:
            plt.xticks(xlabelPoint, xlabel,rotation=rotation, ha='right')
        # 列标签名称
        plt.ylabel(ytitle,fontsize = fontsize+5)
        # 图例标签位置
        plt.legend(loc="upper right")
        # 图标题
        plt.title(title)
        if savepath != '':
            plt.savefig(savepath)
        plt.show()
        # 测试输出
        # print(xlabel,data_namelabel)
        # print(xlabelPoint)
        # print(datavalues['太一'].tolist())
        # print(pltgrouplen,plttakelen)

    # 折线图    输入数据
    def ShowPlot(self, data, indexname=None, isPrintLabel = True, fontsize = 15, title = '', ytitle = '', xtitle='', fingersize:Tuple[int, int] =(22.4, 12.6), rotation=0,savepath:str=''):
        # 设置绘制图像大小
        plt.figure(figsize=fingersize)
        # 获取数据
        if isinstance(data,pd.DataFrame):
            if indexname is None:
                xlabel = list(data.index)
            else:
                xlabel = indexname
            data_namelabel = list(data.columns)
        elif isinstance(data,pd.Series):
            if indexname is None:
                xlabel = list(data.index)
            else:
                xlabel = indexname
            data_namelabel = [data.name]
        # 原始数据
        datavalues = data.values.T.tolist()
        # 列序号
        xlabelPoint = [x for x, _ in enumerate(xlabel)]
        # 配置绘图数据
        pltcolor = ['#F5CD78','#D5D5D5',  '#F4C1BC', '#D8CCE3', '#A7CF9A', '#F4E8A7', '#CAE5EE', '#E77F98', '#F8CC9C',
                    '#D1E1EF', '#A8D3E8', '#F3BECB', '#99B4D7']
        # 绘制图像
        colorid = 0
        for ydata in datavalues:
            plt.plot(xlabelPoint, ydata, pltcolor[colorid % len(pltcolor)], marker='o', markersize=fontsize)
            # 数据标签
            if isPrintLabel:
                for x1, y1 in zip(xlabelPoint, ydata):
                    plt.text(x1, y1, str(y1), ha='center', va='bottom', fontsize=fontsize)
            colorid += 1
        # 绘制图例
        plt.legend(data_namelabel,fontsize = fontsize)
        # 行标签名称
        plt.xlabel(xtitle,fontsize = fontsize+5)
        # 设置坐标轴及标签
        if rotation==0:
            plt.xticks(xlabelPoint, xlabel)
        else:
            plt.xticks(xlabelPoint, xlabel,rotation=rotation, ha='right')
        # 列标签名称
        plt.ylabel(ytitle,fontsize = fontsize+5)
        # 标题
        plt.title(title)
        if savepath != '':
            plt.savefig(savepath)
        plt.show()

    def ShowPie(self,data,indexname = None,fontsize = 15,fingersize:Tuple[int, int] =(22.4, 12.6),savepath:str=''):
        # 设置绘制图像大小
        plt.figure(figsize=fingersize)
        # 获取数据
        if indexname is None:
            xlabel = list(data.index)
        else:
            xlabel = indexname
        # 原始数据
        datavalues = data.values.tolist()
        # 列序号
        xlabelPoint = [x for x, _ in enumerate(xlabel)]
        # 绘制图像
        plt.axis('equal')
        plt.pie(datavalues, labels=xlabel, autopct='%1.2f%%')
        # 绘制图例
        plt.legend(xlabel, fontsize=fontsize)
        # 列标签名称
        plt.ylabel("y轴标签", fontsize=fontsize + 5)
        if savepath != '':
            plt.savefig(savepath)
        plt.show()



if __name__ == '__main__':
    dataA = pd.DataFrame(np.random.randint(0, 99, [7, 4]),
                         index=['一', '二', '三', '四', '五', '六', '七'],
                         columns=['张三', '李四', '王五', '赵六'])
    dataB = pd.DataFrame(np.random.randint(0, 99, [7, 5]),
                         index=['一', '二', '三', '四', '五', '六', '七'],
                         columns=['太一', '慎二', '猫七', '勾八', '琴酒'])
    data = {'之前': dataA, '之后': dataB}
    p = Printer()
    p.ShowBar(data,rotation=0)
    p.ShowPlot(dataA)


# 散点图
'''
def legend():
    girls_grades = [89, 90, 70, 89, 100, 80, 90, 100, 80, 34]
    boys_grades = [30, 29, 49, 48, 100, 48, 38, 45, 20, 30]
    grades_range = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    fig = plt.figure()
    # 添加绘图区域
    ax = fig.add_axes([0, 0, 1, 1])
    ax.scatter(grades_range, girls_grades, color='r', label="girls")
    ax.scatter(grades_range, boys_grades, color='b', label="boys")
    ax.set_xlabel('Grades Range')
    ax.set_ylabel('Grades Scored')
    ax.set_title('scatter plot')
    # 添加图例
    plt.legend()
    plt.show()
'''

# 测试数据
''' 测试柱状图
    dataA = pd.DataFrame(np.random.randint(0,99,[7, 11]),
                        index=['一','二','三','四','五','六','七'],
                        columns=['张三','李四','王五','赵六','1','12','13','14','15','16','17'])
    dataB = pd.DataFrame(np.random.randint(0, 99, [7, 5]),
                        index=['一', '二', '三', '四', '五', '六', '七'],
                        columns=['太一','慎二','猫七','勾八','琴酒'])
    data = {'之前':dataA,'之后':dataB}
    p = Printer()
    p.ShowBar(data)
'''

''' 测试折线图
    data = pd.DataFrame(np.random.randint(0, 99, [7, 5]),
                        index=['一', '二', '三', '四', '五', '六', '七'],
                        columns=['太一','慎二','猫七','勾八','琴酒'])

    p = Printer()
    p.ShowPlot(data)
'''

''' 测试饼图
    data = pd.DataFrame(np.random.randint(0, 99, [7, 5]),
                        index=['一', '二', '三', '四', '五', '六', '七'],
                        columns=['太一', '慎二', '猫七', '勾八', '琴酒'])
    data = data['太一']

    p = Printer()
    p.ShowPie(data)
'''