import zipfile
from io import BytesIO
from lxml import etree
from typing import Callable
from .ecmb_utils import ecmbUtils
from .ecmb_content_base import ecmbContentBase

class ecmbImage(ecmbContentBase):

    _src = None
    _src_format = None
    _src_left = None
    _src_left_format = None
    _src_right = None
    _src_right_format = None
    
    def __init__(self, book_obj, src: str|BytesIO, src_left: str|BytesIO = None, src_right: str|BytesIO = None, unique_id: str = None):
        self._init(book_obj, unique_id)

        (is_double, src_format) = self._check_image(src, 'src', True)
        if is_double:
            if not src_left or not src_right:
                msg = 'for image: "' + src + '"' if type(src) == str else 'at unique_id: "' + self._unique_id + '"'
                ecmbUtils.raise_exception(f'double-page-image detected, but src_left or/and src_right missing {msg}!')
            
            (ignore, src_left_format) = self._check_image(src_left, 'src_left', False)
            (ignore, src_right_format) = self._check_image(src_right, 'src_right', False)
            
            self._src_left = src_left
            self._src_left_format = src_left_format
            self._src_right = src_right
            self._src_right_format = src_right_format
            
        self._src = src
        self._src_format = src_format


    def int_validate(self, warnings: bool|Callable) -> bool:
        self._book_obj.int_get_next_page_nr()

        if self._src_left:
            page_nr = self._book_obj.int_get_next_page_nr()
            if page_nr % 2 != 0:
                msg = 'image: "' + self._src + '"' if type(self._src ) == str else 'image with the unique_id: "' + self._unique_id + '"'
                ecmbUtils.write_warning(warnings, f'{msg} is on an uneven page!')

        return True
    

    def int_build(self, target_file: zipfile.ZipFile) -> etree.Element:
        self._build_id = self._book_obj.int_get_next_build_id()
        file_path = self.int_get_build_path()

        if self._src_left:
            node = etree.Element('dimg')

            node.set('src', self._build_id + '_f.' + self._src_format)
            self._write_image(target_file, file_path + '_f.' + self._src_format, self._src)

            node.set('src_left', self._build_id + '_l.' + self._src_left_format)
            self._write_image(target_file, file_path + '_l.' + self._src_left_format, self._src_left)

            node.set('src_right', self._build_id + '_r.' + self._src_right_format)
            self._write_image(target_file, file_path + '_r.' + self._src_right_format, self._src_right)
        else:
            node = etree.Element('img')

            node.set('src', self._build_id + '.' + self._src_format)
            self._write_image(target_file, file_path + '.' + self._src_format, self._src)
        
        return node
        