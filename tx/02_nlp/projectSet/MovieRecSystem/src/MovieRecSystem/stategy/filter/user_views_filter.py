from typing import List, Optional

from ..services.user_feature_service import UserFeatureService
from ...entity.user_feature import UserFeatureEntity


class UserViewsFilter(object):
    def __init__(self, start: int = 0, end: int = -1):
        self.start = start
        self.end = end

    def get_user_view_spu_ids(self, user: Optional[UserFeatureEntity]) -> List[int]:
        """
        获取当前用户浏览的商品id列表
        :param user: 用户对象
        :return: 商品id列表
        """
        if user is None or user.id is None:
            return []
        # 提取最近浏览的商品id列表
        return UserFeatureService.get_user_view_ids(user.id, self.start, self.end)
