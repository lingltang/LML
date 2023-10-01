import threading
from typing import List, Set, Dict

import redis

from ..config import redis_config


def _encode(v, encoding='UTF-8') -> str:
    return str(v, encoding=encoding)


class RedisUtil(object):
    lock = threading.Lock()  # 锁
    instance = None  # 操作redis的对象

    def __init__(self):
        # 构建一个reids的连接池对象
        self._pool = redis.ConnectionPool(**redis_config.cfg)

    def create_redis(self) -> redis.Redis:
        """
        创建一个操作redis的对象
        :return: redis对象
        """
        return redis.Redis(connection_pool=self._pool)

    @staticmethod
    def _get_redis() -> redis.Redis:
        if RedisUtil.instance is None:
            # 获取锁
            RedisUtil.lock.acquire()
            try:
                if RedisUtil.instance is None:
                    RedisUtil.instance = RedisUtil()
            finally:
                # 释放锁
                RedisUtil.lock.release()
        return RedisUtil.instance.create_redis()

    # ---------------------------------------------------------------------
    # 主要对外提供的方法

    @staticmethod
    def get_slist(key: str, sep: str = ",") -> List[str]:
        """
        提取key对应的value，并将value按照给定分隔符划分为list字符串列表
        NOTE: redis中value的类型实际上是字符串，只是以sep分割
        :param key: key字符串
        :param sep: 分隔符
        :return: 结果对象
        """
        with RedisUtil._get_redis() as client:
            value = client.get(key)
            if value is None:
                return []
            value = _encode(value)  # 编码
            return value.split(sep=sep)

    @staticmethod
    def get_slist_int(key: str, sep: str = ",") -> List[int]:
        """
        在get_slist的基础上，再次将字符串转换为int类型
        :param key: key字符串
        :param sep: 分隔符
        :return: 结果对象
        """
        _list = RedisUtil.get_slist(key, sep)
        if _list is None:
            return []
        return [int(_v) for _v in _list]

    @staticmethod
    def get_list(key: str, start: int = 0, end: int = -1) -> List[str]:
        """
        直接提取redis中list类型对象的结果
        NOTE：redis中value的类型就是list
        :param key: key对象
        :param start: 截取的起始位置，0表示开始位置
        :param end: 截取的结束位置，-1表示结尾位置
        :return: list结果
        """
        with RedisUtil._get_redis() as client:
            if not client.exists(key):
                return []
            values = client.lrange(key, start, end)
            if values is None:
                return []
            return [_encode(v) for v in values]

    @staticmethod
    def get_list_int(key: str, start: int = 0, end: int = -1) -> List[int]:
        """
        基于get_list提取int列表
        :param key: key对象
        :param start: 截取的起始位置
        :param end: 截取的结束位置
        :return: list结果
        """
        _list = RedisUtil.get_list(key, start, end)
        if _list is None:
            return []
        return [int(_v) for _v in _list]

    @staticmethod
    def get_set(key: str) -> List[str]:
        """
        获取一个key对应的set集合数据，并将其转换为list
        :param key: key字符串
        :return:
        """
        with RedisUtil._get_redis() as client:
            if not client.exists(key):
                return []
            values = client.smembers(key)
            if values is None:
                return []
            return [_encode(v) for v in values]

    @staticmethod
    def get_set_int(key: str) -> List[int]:
        """
        在get_set的基础上，将结果转换为int返回
        :param key:
        :return:
        """
        _list = RedisUtil.get_set(key)
        if _list is None:
            return []
        return [int(_v) for _v in _list]

    @staticmethod
    def get_hash(key: str, fields: List[str] = None) -> Dict[str, str]:
        """
        获取redis中hash类型的数据
        :param key:  key名称
        :param fields: 属性名称列表，如果为None，表示获取全部属性信息
        :return:
        """
        with RedisUtil._get_redis() as client:
            if not client.exists(key):
                return {}
            if fields is None:
                values = client.hgetall(key)
            else:
                values = client.hmget(key, fields)
            if values is None:
                return {}
            result = {}
            for _k, _v in zip(fields, values):
                result[_k] = _encode(_v)
            return result
