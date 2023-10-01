from projectSet.MovieRecSystem.src.MovieRecSystem.entity.spu_feature import SpuFeatureEntity
from projectSet.MovieRecSystem.src.MovieRecSystem.entity.user_feature import UserFeatureEntity
from projectSet.MovieRecSystem.src.MovieRecSystem.stategy.entity.config_param import ConfigParams
from projectSet.MovieRecSystem.src.MovieRecSystem.stategy.entity.scene_meta import SceneMeta
from projectSet.MovieRecSystem.src.MovieRecSystem.stategy.strategy_runner import StrategyRunner


class NetApi:
    def __init__(self):
        self._strategy = StrategyRunner()
        print('init system')

    def test(self):
        # 策略对象提取
        _config = ConfigParams()
        _scene = SceneMeta()
        _user = UserFeatureEntity(
            record={
                'user_id': 11,
                'zip_code': '302222'
            }
        )
        _spu = SpuFeatureEntity(
            record={
                'id': 198,
                'actors': 'Tom,Gerry'
            }
        )

        # 根据参数构建结果
        _rs = self._strategy.get_rec_spu_ids_by_scene(_config,_scene,_user,_spu)

        return [dict(i) for i in _rs]

if __name__ == '__main__':
    na = NetApi()
    td = na.test()
    for i in td:
        print(i)