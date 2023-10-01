import json
from typing import List, Optional


class RecExplain(object):
    """
    定义推荐过程中的explain临时执行结果
    """

    def __init__(self, stage: str, explain: str, source: str):
        self.stage = stage
        self.explain = explain
        self.source = source

    def __iter__(self):
        yield from {
            'stage': self.stage,
            'explain': self.explain,
            'source': self.source
        }.items()

    def __str__(self):
        return json.dumps(dict(self), ensure_ascii=False)


class RecItem(object):
    """
    最终返回给前端的推荐结果
    """

    def __init__(self, spu_id: int, score: float, explains: List[RecExplain]):
        self.spu_id: int = spu_id
        self.score: float = score
        self.explains: List[RecExplain] = explains
        self.is_effect: bool = True  # 当前商品是否有效

    def merge_explain(self, other_explains: List[RecExplain], score: Optional[float] = None):
        """
        合并策略
        :param score: 评分，如果给定的时候，那么和当前评分选最大值
        :param other_explains: 待合并的策略
        :return:
        """
        if score is not None:
            self.score = max(self.score, score)
        if self.explains is None:
            self.explains = []
        if other_explains is not None:
            self.explains.extend(other_explains)

    def __iter__(self):
        yield from {
            'spu_id': self.spu_id,
            'score': self.score,
            'explains': [dict(v) for v in self.explains]
        }.items()

    def all_dict(self):
        return {
            'spu_id': self.spu_id,
            'score': self.score,
            'explains': [dict(v) for v in self.explains],
            'is_effect': self.is_effect
        }

    def __str__(self):
        _dict = {
            'spu_id': self.spu_id,
            'score': self.score,
            'explains': [dict(v) for v in self.explains],
            'is_effect': self.is_effect
        }
        return json.dumps(_dict, ensure_ascii=False)

    def add_filter(self, explain, source):
        self.explains.append(RecExplain("filter", explain, source))
        self.is_effect = False

    def add_rank(self, explain, source):
        self.explains.append(RecExplain("rank", explain, source))

    @staticmethod
    def get_recall_rec_item(spu_id: int, score: float, explain: str, source: str):
        explains = [RecExplain("recall", explain, source)]
        return RecItem(spu_id, score, explains)
