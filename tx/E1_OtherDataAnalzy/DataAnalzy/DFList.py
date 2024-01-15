import AZData
from ConstData.StructData import DF,DFlog

class DFList():
    def __init__(self):
        self.dfm = list()
        self.logs = list()



    def __addDfm(self):
        pass

    def __addlog(self):
        pass

if __name__ == '__main__':
    dataF = DF(1,'cc',1,'tx')
    c = DFList()
    c.addDfm(dataF)