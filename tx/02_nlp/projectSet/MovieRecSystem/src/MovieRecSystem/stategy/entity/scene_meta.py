"""
定义策略元数据对象
"""

from typing import List, Optional


class SceneMeta(object):
    def __init__(self, record: Optional[dict] = None):
        # 场景名称
        self.name = "name"
        # 召回策略名称字符串
        self.recalls: List[str] = ["hots", "news"]
        # 过滤策略名称字符串
        self.filters: List[str] = ["views", "blacklist", "user_no_like"]
        # 排序策略名称字符串
        self.ranks: List[str] = ["lr"]
        # 重排序策略名称字符串
        self.reranks: List[str] = []
        # 基于参数初始化
        self.__init_with_record(record)

    def __init_with_record(self, record):
        if record is None or len(record) == 0:
            return

        def _split(_v):
            if _v is None:
                return []
            return list(map(lambda t: t.strip(), _v.split(",")))

        self.name = record['name']
        self.recalls = _split(record['recalls'])
        self.filters = _split(record['filters'])
        self.ranks = _split(record['ranks'])
        self.reranks = _split(record['reranks'])
