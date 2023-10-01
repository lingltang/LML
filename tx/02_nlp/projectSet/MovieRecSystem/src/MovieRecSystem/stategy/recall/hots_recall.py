import copy
import random
from typing import Optional, List

from ..services.spu_feature_service import SpuFeatureService
from ...entity.rec_item import RecItem


class HotsRecall(object):
    def get_candidates(self, k: Optional[int] = None) -> List[RecItem]:
        """
        获取前k个热映商品
        :param k: 待获取的数量，如果为None，表示获取所有
        :return: 结果
        """
        return self._get_hot_items(k)

    @staticmethod
    def _get_hot_items(k: Optional[int] = None) -> List[RecItem]:
        spu_ids = SpuFeatureService.get_hot_ids()  # 获取所有的热映商品id列表
        if spu_ids is None or len(spu_ids) == 0:
            return []
        if k is not None and k > 0:
            spu_ids = copy.deepcopy(spu_ids)
            random.shuffle(spu_ids)
            spu_ids = spu_ids[:k]
        items: List[RecItem] = []
        for spu_id in spu_ids:
            items.append(RecItem.get_recall_rec_item(spu_id, 1.0, 'hots', 'hots'))
        return items
