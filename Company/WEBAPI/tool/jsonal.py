import json

def loadFile(filepath):
    res = None
    with open(filepath, 'r') as f:
        res = f.read()
    f.close()
    return res

class jsonal:
    def __init__(self,data):
        self.data = data
        self.res = None

    def loadFile(self):
        res = loadFile(self.data)
        if res != None:
            self.res = json.loads(res)
        return self.res

    def toDict(self):
        self.res = json.loads(self.data)
        return self.res

    def toJson(self):
        self.res = json.dumps(self.data)
        return self.res