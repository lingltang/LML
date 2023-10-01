from typing import List

from cachetools import TTLCache, cached

from ...utils import extract_with_index
from ...utils.redis_util import RedisUtil


class SpuFeatureService(object):
    @staticmethod
    @cached(cache=TTLCache(maxsize=100, ttl=600))
    def get_cache_list_int_v1(key):
        return RedisUtil.get_list_int(key)

    @staticmethod
    @cached(cache=TTLCache(maxsize=100, ttl=10))
    def get_cache_list_int_v2(key):
        return RedisUtil.get_list_int(key)

    @staticmethod
    def get_hot_ids(start: int = 0, end: int = -1) -> List[int]:
        """
        获取热映商品id列表
        :param start: 起始下标(包含)，0表示第一个
        :param end: 结束下标(包含)，-1表示最后一个
        :return: 商品id列表
        """
        ids = SpuFeatureService.get_cache_list_int_v1("rec:hot_spu")
        return extract_with_index(ids, start, end)

    @staticmethod
    def get_new_ids(start: int = 0, end: int = -1) -> List[int]:
        """
        获取新商品id列表
        :param start: 起始下标(包含)，0表示第一个
        :param end: 结束下标(包含)，-1表示最后一个
        :return: 商品id列表
        """
        ids = SpuFeatureService.get_cache_list_int_v1("rec:new_spu")
        return extract_with_index(ids, start, end)
