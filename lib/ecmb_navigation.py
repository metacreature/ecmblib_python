from typing import Callable
from lxml import etree
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
    

    def int_build(self) -> etree.Element:
        if not self.int_validate(False):
            return
        
        main_node = etree.Element('navigation')

        for child in self._children:
            child_node = child.int_build()
            if child_node != None:
                main_node.append(child_node)
        
        return main_node