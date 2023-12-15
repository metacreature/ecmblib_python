import zipfile
from typing import Callable
from io import BytesIO
from lxml import etree
from .ecmb_utils import ecmbUtils
from .ecmb_content_base_sub import ecmbContentBaseSub


class ecmbContent(ecmbContentBaseSub):

    _cover_front = None
    _cover_front_format = None
    _cover_rear = None
    _cover_rear_format = None

    def __init__(self, book_obj):
        self._book_obj = book_obj
        self._contents = []

    
    def set_cover_front(self, src: str|BytesIO) -> None:
        (ignore, cover_front_format) = self._check_image(src, 'src', False)
        self._cover_front = src
        self._cover_front_format = cover_front_format


    def set_cover_rear(self, src: str|BytesIO) -> None:
        (ignore, cover_rear_format) = self._check_image(src, 'src', False)
        self._cover_rear = src
        self._cover_rear_format = cover_rear_format
    

    def int_validate(self, warnings: bool|Callable) -> bool:
        found = False
        for content in self._contents:
            if content.int_validate(warnings):
                found = True

        if not found:
            ecmbUtils.raise_exception(f'the book doesn\'t contain an image!')
        return found
    

    def int_build(self, target_file: zipfile.ZipFile) -> etree.Element:
        if not self.int_validate(False):
            return
        
        self._build_id = 'content'
        main_node = etree.Element('content')

        if self._cover_front:
            main_node.set('cover_front', 'cover_front.' + self._cover_front_format)
            self._write_image(target_file, 'cover_front.' + self._cover_front_format, self._cover_front)

        if self._cover_rear:
            main_node.set('cover_rear', 'cover_rear.' + self._cover_rear_format)
            self._write_image(target_file, 'cover_rear.' + self._cover_rear_format, self._cover_rear)

        target_file.mkdir(self.int_get_build_path(False))

        for content in self._contents:
            content_node = content.int_build(target_file)
            if content_node != None:
                main_node.append(content_node)
        
        return main_node