from typing import Callable
from .ecmb_utils import ecmbUtils
from .ecmb_navigation_base import ecmbNavigationBase
from .ecmb_navigation_base_sub import ecmbNavigationBaseSub


class ecmbNavigation(ecmbNavigationBaseSub):

    def __init__(self, book_obj):
        self._book_obj = book_obj
        self._children = []


    def int_set_parent(self, parent_content_obj: ecmbNavigationBase) -> None:
        pass


    def int_validate(self, warnings: bool|Callable) -> bool:
        if not super().int_validate(warnings):
            ecmbUtils.write_warning(warnings, 'Its recommended to provide a navigation!')
            return False
        return True