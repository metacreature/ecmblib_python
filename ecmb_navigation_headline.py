from typing import TypeVar, Callable
from .ecmb_utils import ecmbUtils
from .ecmb_navigation_base_sub import ecmbNavigationBaseSub

ecmbBook = TypeVar("ecmbBook")


class ecmbNavigationHeadline(ecmbNavigationBaseSub):

    def __init__(self, book_obj: ecmbBook, label: str, title:str = None):
        super()._init(book_obj, label, title)


    def int_validate(self, warnings: bool|Callable) -> bool:
        if not super().int_validate(warnings):
            ecmbUtils.write_warning(warnings, 'the headline "' + self._label + '" doesn\'t contain an item!')
            return False
        return True