import pymysql
from tool.jsonal import jsonal

class sqltl:
    def __init__(self,configFile = "./config/sql.json"):
        self.sl = jsonal(configFile).loadFile()
        sl = self.sl
        self.conn = self.__reConnect()
        self.execute = None

    def __reConnect(self):
        sl = self.sl
        self.conn = pymysql.connect(host=sl['host'],user=sl['user'],password=sl['password'],
                                    database=sl['database'],port=sl['port'])

    def selectData(self,sql):
        self.__reConnect()
        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        result = None
        try:
            cursor.execute(sql)
            result = cursor.fetchall()  # 返回所有数据
        except Exception as e:
            print(e)
            self.conn.rollback()
        finally:
            cursor.close()
            self.conn.close()
        return result

    def insertData(self,sql,data):
        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute(sql, data)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
        finally:
            cursor.close()

if __name__ == "__main__":
    sqltltx = sqltl(configFile = "../config/sql.json")
    systems = sqltltx.selectData("select equipment_sys from eicrbasic where equipment_sys != '' group by equipment_sys;")
    print(systems)
