from typing import List, Optional, Dict

from .entity.config_param import ConfigParams
from .entity.scene_meta import SceneMeta
from ..entity.rec_item import RecItem
from ..entity.spu_feature import SpuFeatureEntity
from ..entity.user_feature import UserFeatureEntity


class RankRunner(object):
    def __init__(self):
        pass

    def rank_candidates_items(self,
                              items: List[RecItem],
                              spus: Dict[int, SpuFeatureEntity],
                              config: ConfigParams,
                              scene: SceneMeta,
                              user: Optional[UserFeatureEntity] = None,
                              spu: Optional[SpuFeatureEntity] = None
                              ) -> List[RecItem]:
        """
        针对商品列表进行对应策略的排序
        :param items: 候选商品列表
        :param spus: 候选商品对应的商品特征属性列表
        :param config: 参数
        :param scene: 策略对象
        :param user: 当前用户对象
        :param spu: 当前物品对象
        :return: 排序好的结果
        """
        if items is None or len(items) == 0:
            return []
        # 1. 排序-->仅针对有效的商品列表进行排序即可
        for _rank in scene.ranks:
            items = self._rank_items(_rank, items, spus, config, user, spu)
        return items

    def _rank_items(self,
                    rank: str,
                    items: List[RecItem],
                    spus: Dict[int, SpuFeatureEntity],
                    config: ConfigParams,
                    user: Optional[UserFeatureEntity] = None,
                    spu: Optional[SpuFeatureEntity] = None
                    ) -> List[RecItem]:
        """
        依照给定的策略进行数据排序，并返回结果
        :param rank: 策略字符串
        :param items: 候选商品列表
        :param spus: 候选商品对应的商品特征属性列表
        :param config: 参数
        :param user: 当前用户对象
        :param spu: 当前物品对象
        :return: 当前策略的排序结果
        """
        # TODO: 和召回、过滤一样，都是具体策略的编写了
        return items
