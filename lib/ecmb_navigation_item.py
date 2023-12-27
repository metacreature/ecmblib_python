import re
from typing import Callable
from lxml import etree
from .ecmb_enums import *
from .ecmb_utils import ecmbUtils
from .ecmb_navigation_base import ecmbNavigationBase
from .ecmb_content_image import ecmbContentImage


class ecmbNavigationItem(ecmbNavigationBase):

    def __init__(self, book_obj, label: str, target: str|ecmbContentImage, target_side: TARGET_SIDE = TARGET_SIDE.AUTO, title:str = None):
        super()._init(book_obj, label, title)
        super()._set_target('navigation-item', target, target_side)


    def int_validate(self, warnings: bool|Callable) -> bool:
        parent_folder_obj = self._parent_navigation_obj.int_get_parent_chapters_folder()
        if parent_folder_obj and not parent_folder_obj.int_contains(self._target_image_obj):
            ecmbUtils.raise_exception('given target-image  is not part of parent chapter\'s target-folder at item "' + self._label + '"!')
        return True
    

    def int_build(self) -> etree.Element:
        if not self.int_validate(False):
            return
        
        main_node = etree.Element('item')
        main_node.set('label', self._label)
        if self._title:
            main_node.set('title', self._title)

        image_link = self._target_image_obj.int_get_image_path(self._target_image_side)

        parent_folder_obj = self._parent_navigation_obj.int_get_parent_chapters_folder()
        if parent_folder_obj:
            parent_folder_link = parent_folder_obj.int_get_build_path()
            image_link = re.sub('^'+parent_folder_link, '', image_link)

        main_node.set('href', image_link)
        
        return main_node