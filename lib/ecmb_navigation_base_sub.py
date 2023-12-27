from __future__ import annotations
from typing import Callable
from .ecmb_enums import *
from .ecmb_utils import ecmbUtils
from .ecmb_navigation_base import ecmbNavigationBase
from .ecmb_navigation_item import ecmbNavigationItem
from .ecmb_content_folder import ecmbContentFolder
from .ecmb_content_image import ecmbContentImage


class ecmbNavigationBaseSub(ecmbNavigationBase):

    _children = None

    def _init(self, book_obj, label: str, title: str) -> None:
        super()._init(book_obj, label, title)
        self._children = []


    def add_headline(self, label_or_headline: str|ecmbNavigationHeadline, title: str = None) -> ecmbNavigationHeadline:
        headline_obj = None

        if type(label_or_headline) == ecmbNavigationHeadline:
            headline_obj = label_or_headline
        elif type(label_or_headline) == str:
            headline_obj = ecmbNavigationHeadline(self._book_obj, label_or_headline, title)
        else:
            ecmbUtils.raise_exception('please provide ecmbNavigationHeadline or a label!')
            
        headline_obj.int_set_parent(self)
        self._children.append(headline_obj)

        return headline_obj
    

    def add_chapter(self, label_or_chapter: str|ecmbNavigationChapter, uid_or_folder: str|ecmbContentFolder, uid_or_image: str|ecmbContentImage = None, target_side: TARGET_SIDE = TARGET_SIDE.AUTO, title: str = None) -> ecmbNavigationChapter:
        chapter_obj = None

        if type(label_or_chapter) == ecmbNavigationChapter:
            chapter_obj = label_or_chapter
        elif type(label_or_chapter) == str:
            chapter_obj = ecmbNavigationChapter(self._book_obj, label_or_chapter, uid_or_folder, uid_or_image, target_side, title)
        else:
            ecmbUtils.raise_exception('please provide ecmbNavigationChapter or a label!')
            
        chapter_obj.int_set_parent(self)
        self._children.append(chapter_obj)

        return chapter_obj


    def add_item(self, label_or_item: str|ecmbNavigationItem, uid_or_image: str|ecmbContentImage, target_side: TARGET_SIDE = TARGET_SIDE.AUTO, title: str = None) -> ecmbNavigationItem:
        item_obj = None

        if type(label_or_item) == ecmbNavigationItem:
            item_obj = label_or_item
        elif type(label_or_item) == str:
            item_obj = ecmbNavigationItem(self._book_obj, label_or_item, uid_or_image, target_side, title)
        else:
            ecmbUtils.raise_exception('please provide ecmbNavigationItem or a label!')
            
        item_obj.int_set_parent(self)
        self._children.append(item_obj)

        return item_obj
    

    def int_validate(self, warnings: bool|Callable) -> bool:
        found = False
        for child in self._children:
            if child.int_validate(warnings):
                found = True
        return found
    

# for type-hinting and and type-check in combination with "from __future__ import annotations"
# can't include them on top coz these ar subclasses of ecmbNavigationBaseSub
from .ecmb_navigation_chapter import ecmbNavigationChapter
from .ecmb_navigation_headline import ecmbNavigationHeadline