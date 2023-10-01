from typing import Optional, List, Dict

from projectSet.MovieRecSystem.src.MovieRecSystem.entity.rec_item import RecItem
from projectSet.MovieRecSystem.src.MovieRecSystem.entity.spu_feature import SpuFeatureEntity
from projectSet.MovieRecSystem.src.MovieRecSystem.entity.user_feature import UserFeatureEntity
from projectSet.MovieRecSystem.src.MovieRecSystem.stategy.entity.config_param import ConfigParams
from projectSet.MovieRecSystem.src.MovieRecSystem.stategy.entity.scene_meta import SceneMeta
from projectSet.MovieRecSystem.src.MovieRecSystem.stategy.filter_runner import FilterRunner
from projectSet.MovieRecSystem.src.MovieRecSystem.stategy.rank_runner import RankRunner
from projectSet.MovieRecSystem.src.MovieRecSystem.stategy.recall_runner import RecallRunner
from projectSet.MovieRecSystem.src.MovieRecSystem.utils.logger_util import logger


class StrategyRunner(object):
    def __init__(self):
        self.recall_runner = RecallRunner()
        self.filter_runner = FilterRunner()
        self.rank_runner = RankRunner()

    def get_rec_spu_ids_by_scene(self,
                                 config:ConfigParams,
                                 scene:SceneMeta,
                                 user:Optional[UserFeatureEntity]=None,
                                 spu:Optional[SpuFeatureEntity]=None
                                 )->List[RecItem]:
        """
        基于给定的策略对象获取对应的推荐结果
        :param config: 参数信息，比如：最终返回前多少商品作为推荐结果
        :param scene: 策略对象/场景对象；定义具体的召回、过滤、精排、重排等策略；
        :param user: 用户对象，可能为空，包含当前用户属性
        :param spu: 物品对象，可能为空，包含当前物品属性
        :return: 推荐结果
        """
        if scene is None:
            logger.warning("必须给定有效的策略对象，当前入参为空!")
            return []
        # 1. 召回
        items = self.recall_runner.fetch_candidates_items(config, scene, user, spu)

        # 2. 基于召回商品列表&获取对应的商品特征属性对象
        # NOTE: 因为召回出来的商品列表是比较大的，所有在某些操作系统中，获取商品特征属性分为两个步骤来获取
        # 步骤1、在召回之后，过滤之前获取，仅获取部分少量特征 --> 主要应用于过滤
        # 步骤2、在过滤之后，排序之前获取，获取全部特征(模型需要的) --> 主要应用于排序
        spus: Dict[int, SpuFeatureEntity] = {}

        # 3. 过滤
        effect_items, no_effect_items = self.filter_runner.filter_candidates_items(
            items, spus, config, scene, user, spu
        )

        # 4. 排序
        items = self.rank_runner.rank_candidates_items(effect_items, spus, config, scene, user, spu)

        # 5. 结果返回
        logger.info(
            "当前参数[%s - %s - %s - %s]情况下推荐结果为:%s;被过滤的商品列表为:%s",
            config.number_push, scene.name, None if user is None else user.id,
            None if spu is None else spu.id,
            json.dumps([item.all_dict() for item in items]),
            json.dumps([item.all_dict() for item in no_effect_items])
        )
        return [v for v in items if v.is_effect][:config.number_push]
