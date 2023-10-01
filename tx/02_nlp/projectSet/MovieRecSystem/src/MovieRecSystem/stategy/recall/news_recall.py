import copy
import random
from typing import Optional, List

from cachetools import cached, TTLCache

from ..services.spu_feature_service import SpuFeatureService
from ...entity.rec_item import RecItem
from ...utils.redis_util import RedisUtil


class NewsRecall(object):

    def get_candidates(self, k: Optional[int] = None) -> List[RecItem]:
        """
        获取前k个新商品
        :param k: 待获取的数量，如果为None，表示获取所有
        :return: 结果
        """
        return self._get_new_items(k)

    @staticmethod
    def _get_new_items(k: Optional[int] = None) -> List[RecItem]:
        spu_ids = SpuFeatureService.get_new_ids()
        if spu_ids is None or len(spu_ids) == 0:
            return []
        if k is not None and k > 0:
            spu_ids = copy.deepcopy(spu_ids)
            random.shuffle(spu_ids)
            spu_ids = spu_ids[:k]
        items: List[RecItem] = []
        for spu_id in spu_ids:
            items.append(RecItem.get_recall_rec_item(spu_id, 1.0, 'news', 'news'))
        return items
