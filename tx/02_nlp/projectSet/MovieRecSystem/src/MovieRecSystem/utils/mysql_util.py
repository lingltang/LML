from ..config import mysql_config

def _encode(v, encoding='UTF-8') -> str:
    return str(v, encoding=encoding)

class MysqlUtil(object):
    def __init__(self):
        pass