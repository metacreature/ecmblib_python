from typing import Self, Callable
from abc import ABC, abstractmethod
from lxml import etree
from .ecmb_enums import *
from .ecmb_utils import ecmbUtils
from .ecmb_content_folder import ecmbContentFolder
from .ecmb_content_image import ecmbContentImage


class ecmbNavigationBase(ABC):

    _book_obj = None
    _parent_navigation_obj = None
    _label = None
    _title = None
    _target_image_obj = None
    _target_image_side = None

    def set_title(self, title:str) -> None:
        ecmbUtils.validate_str_or_none(True,  'title', title)
        self._title = title


    def int_set_parent(self, parent_navigation_obj: Self) -> None:
        if self._parent_navigation_obj != None:
            ecmbUtils.raise_exception(f'the navigation-obj with the label "' + self._label + '" can\'t be added twice!', 1)
        self._parent_navigation_obj = parent_navigation_obj

        
    def int_get_parent_chapters_folder(self) -> ecmbContentFolder:
        if self._parent_navigation_obj:
            return self._parent_navigation_obj.int_get_parent_chapters_folder()
        return None


    def _init(self, book_obj, label: str, title: str) -> None:
        if not 'ecmbBook' in str(type(book_obj)):
            ecmbUtils.raise_exception(f'ecmbBook expected, but got diffrent type!', 1)
        
        ecmbUtils.validate_not_empty_str(True,  'label', label, 1)
        ecmbUtils.validate_str_or_none(True,  'title', title, 1)

        self._book_obj = book_obj
        self._label = label
        self._title = title


    def _set_target(self, target: str|ecmbContentImage, target_side: TARGET_SIDE) -> None:
        target_side = ecmbUtils.enum_value(target_side)
        if target_side:
            ecmbUtils.validate_enum(True, 'target_side', target_side, TARGET_SIDE, 1)

        target_image_obj = None
        if type(target) == ecmbContentImage or (type(target) == str and target != ''):
            target_image_obj = self._book_obj.int_get_content(target)
        else:
            ecmbUtils.raise_exception('target must be either an unique_id or an ecmbContentImage on navigation-item "' + self._label + '"!', 1)

        if not target_image_obj:
            ecmbUtils.raise_exception('the given target was not found in the book on navigation-item "' + self._label + '"!', 1)

        self._target_image_obj = target_image_obj
        self._target_image_side = target_side


    @abstractmethod
    def int_validate(self, warnings: bool|Callable) -> bool:
        pass


    @abstractmethod
    def int_build(self) -> etree.Element:
        pass