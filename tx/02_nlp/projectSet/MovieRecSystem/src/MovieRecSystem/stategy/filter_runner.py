from typing import List, Optional, Dict

from .entity.config_param import ConfigParams
from .entity.scene_meta import SceneMeta
from .filter.user_views_filter import UserViewsFilter
from ..entity.rec_item import RecItem
from ..entity.spu_feature import SpuFeatureEntity
from ..entity.user_feature import UserFeatureEntity
from ..utils.logger_util import logger


class FilterRunner(object):
    def __init__(self):
        self.user_views = UserViewsFilter(start=0, end=9)

    def filter_candidates_items(self,
                                items: List[RecItem],
                                spus: Dict[int, SpuFeatureEntity],
                                config: ConfigParams,
                                scene: SceneMeta,
                                user: Optional[UserFeatureEntity] = None,
                                spu: Optional[SpuFeatureEntity] = None
                                ) -> (List[RecItem], List[RecItem]):
        """
        针对召回的商品列表进行过滤
        :param items: 召回的商品列表
        :param spus: 召回商品对应的特征属性信息
        :param config: 参数
        :param scene: 策略对象
        :param user: 当前用户对象
        :param spu: 当前物品对象
        :return:
        """
        if items is None or len(items) == 0:
            return []
        # 1. 获取需要进行过滤的商品id字典
        filtered_spu_ids = {}  # key为待过滤的商品id，value为对应的过滤策略
        spu_ids = [item.spu_id for item in items if item.is_effect]  # 获取候选商品对应的商品id列表
        for _filter in scene.filters:
            _ids = self._get_filtered_spu_ids(_filter, spu_ids, spus, config, user, spu)
            if _ids is None or len(_ids) == 0:
                continue
            for _id in _ids:
                if _id in filtered_spu_ids:
                    filtered_spu_ids[_id].append(_filter)
                else:
                    filtered_spu_ids[_id] = [_filter]

        # 2. 遍历所有候选商品列表，进行filtered的过滤器添加
        effect_items, no_effect_items = [], []
        for item in items:
            if item.spu_id in filtered_spu_ids:
                _filter_explain = ','.join(filtered_spu_ids[item.spu_id])
                item.add_filter(_filter_explain, 'filter')
                if item.spu_id in spus:
                    # 如果待删除的商品id在商品特征属性列表中，那么进行删除操作
                    del spus[item.spu_id]
                no_effect_items.append(item)
            else:
                effect_items.append(item)
        return effect_items, no_effect_items

    def _get_filtered_spu_ids(self,
                              filter_strategy: str,
                              spu_ids: List[int],
                              spus: Dict[int, SpuFeatureEntity],
                              config: ConfigParams,
                              user: Optional[UserFeatureEntity],
                              spu: Optional[SpuFeatureEntity]) -> List[int]:
        """
        基于对应的过滤策略从spu_ids中选择出当前策略可能删除的商品id列表
        :param filter_strategy: 过滤策略字符串
        :param spu_ids: 候选商品id列表
        :param spus: 候选商品特征属性字典对象
        :param config: 参数对象
        :param user: 当前用户
        :param spu: 当前物品
        :return: 过滤商品id列表，是spu_ids的一个子集
        """
        ids = []
        try:
            if filter_strategy == 'views':
                ids = self.user_views.get_user_view_spu_ids(user)
            else:
                logger.warning(f"不支持当前过滤策略:{filter_strategy}")
        except Exception as e:
            logger.error(f"当前过滤策略{filter_strategy}执行失败。", exc_info=e)
        return ids
