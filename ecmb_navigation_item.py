from typing import Callable
from .ecmb_utils import ecmbUtils
from .ecmb_navigation_base import ecmbNavigationBase
from .ecmb_image import ecmbImage


class ecmbNavigationItem(ecmbNavigationBase):

    def __init__(self, book_obj, label: str, target: str|ecmbImage, title:str = None):
        super()._init(book_obj, label, title)
        super()._set_target(target)


    def int_validate(self, warnings: bool|Callable) -> bool:
        parent_folder = self._parent_navigation_obj.int_parent_chapter_folder()
        if parent_folder and not parent_folder.int_contains(self._target_image_obj):
            ecmbUtils.write_warning(warnings, 'given target-image  is not part of parent chapter\'s target-folder at  item "' + self._label + '"!')
        return True