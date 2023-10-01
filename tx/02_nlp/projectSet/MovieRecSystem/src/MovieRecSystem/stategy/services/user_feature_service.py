from typing import List

from cachetools import cached, TTLCache

from ...utils.redis_util import RedisUtil


class UserFeatureService(object):
    @staticmethod
    @cached(cache=TTLCache(maxsize=10000, ttl=5))
    def get_user_view_ids(user_id: int, start: int = 0, end: int = -1) -> List[int]:
        """
        提取当前用户最近浏览的商品id列表
        :param user_id: 用户id
        :param start: 商品列表的起始下标(包含)
        :param end: 商品列表的结尾下标(包含)
        :return: 列表
        """
        if user_id is None or user_id <= 0:
            return []
        # key里面包含大括号的主要目的是，当redis是分布式的时候，会基于大括号里面的内容决定数据应该落在那个节点上
        _key = "rec:user:views:{" + str(user_id) + "}"
        _values = RedisUtil.get_list_int(_key, start, end)
        return _values
