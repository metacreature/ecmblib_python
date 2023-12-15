from typing import Callable
from lxml import etree
from .ecmb_utils import ecmbUtils
from .ecmb_navigation_base_sub import ecmbNavigationBaseSub


class ecmbNavigationHeadline(ecmbNavigationBaseSub):

    def __init__(self, book_obj, label: str, title:str = None):
        super()._init(book_obj, label, title)


    def int_validate(self, warnings: bool|Callable) -> bool:
        if not super().int_validate(warnings):
            ecmbUtils.write_warning(warnings, 'the headline "' + self._label + '" doesn\'t contain a navigation-item!')
            return False
        return True
    

    def int_build(self) -> etree.Element:
        if not self.int_validate(False):
            return
        
        main_node = etree.Element('headline')
        main_node.set('label', self._label)
        if self._title:
            main_node.set('title', self._title)

        for child in self._children:
            child_node = child.int_build()
            if child_node != None:
                main_node.append(child_node)
        
        return main_node