from typing import List, Optional, Dict

from .entity.config_param import ConfigParams
from .entity.scene_meta import SceneMeta
from .recall.hots_recall import HotsRecall
from .recall.news_recall import NewsRecall
from ..entity.rec_item import RecItem
from ..entity.spu_feature import SpuFeatureEntity
from ..entity.user_feature import UserFeatureEntity
from ..utils.logger_util import logger


class RecallRunner(object):
    def __init__(self):
        self.hots = HotsRecall()
        self.news = NewsRecall()

    def fetch_candidates_items(self, config: ConfigParams,
                               scene: SceneMeta,
                               user: Optional[UserFeatureEntity] = None,
                               spu: Optional[SpuFeatureEntity] = None) -> List[RecItem]:
        """
        根据具体的召回策略获取对应的召回商品列表；
        :param config: 参数
        :param scene: 策略对象
        :param user: 当前用户
        :param spu: 当前物品
        :return: 召回的商品列表
        """
        recalls = scene.recalls
        if recalls is None or len(recalls) == 0:
            raise ValueError("策略参数recalls为空，必须给定有效的策略值!")
        recall_dict: Dict[int, RecItem] = {}
        # 遍历提取每个策略对应的召回结果
        for _recall in recalls:
            _items = self._get_recommend_candidates(_recall, config, user, spu)
            if _items is None:
                logger.warning(f"召回策略{_recall}返回结果为空，请检查!相关参数为:{config} -- {user} -- {spu}.")
                continue
            for _item in _items:
                if _item.spu_id == 0:
                    logger.warning(f"召回策略{_recall}召回结果异常:{_item}")
                    continue
                if _item.spu_id in recall_dict:
                    # 多个召回策略均召回了当前商品，就需要将explain进行合并
                    recall_dict[_item.spu_id].merge_explain(_item.explains, _item.score)
                else:
                    recall_dict[_item.spu_id] = _item
        # 结果处理转换
        if len(recall_dict) == 0:
            raise ValueError(f"召回策略的执行没有召回出任何商品，请检查:{recalls}")
        return list(recall_dict.values())

    def _get_recommend_candidates(self,
                                  recall: str,
                                  config: ConfigParams,
                                  user: Optional[UserFeatureEntity] = None,
                                  spu: Optional[SpuFeatureEntity] = None
                                  ) -> List[RecItem]:
        """
        获取具体策略对应的召回结果
        NOTE：实际上一个推荐系统框架搭建好后，基本上就是改动这部分的代码
        :param recall: 策略名称字符串(全系统唯一)
        :param config: 配置对象
        :param user: 当前用户对象
        :param spu: 当前物品对象
        :return: 召回结果列表
        """
        items = []
        try:
            k = config.number_push  # 针对推荐需要返回的商品数量
            if recall == 'hots':
                items = self.hots.get_candidates(k=k * 2)
            elif recall == 'news':
                items = self.news.get_candidates(k=k * 2)
            else:
                logger.error(f"当前不支持该召回策略:{recall}")
        except Exception as e:
            logger.error(f"当作召回策略{recall}执行失败！", exc_info=e)
        return items
