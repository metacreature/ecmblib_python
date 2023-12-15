import zipfile
from lxml import etree
from typing import Callable
from .ecmb_utils import ecmbUtils
from .ecmb_content_base_sub import ecmbContentBaseSub
from .ecmb_content_image import ecmbContentImage

class ecmbContentFolder(ecmbContentBaseSub):

    _contents = None

    def __init__(self, book_obj, unique_id: str = None):
        self._init(book_obj, unique_id)
        self._contents = []


    def int_validate(self, warnings: bool|Callable) -> bool:
        found = False
        for content in self._contents:
            if content.int_validate(warnings):
                found = True

        if not found:
            ecmbUtils.raise_exception('folder with the unique_id "' + self._unique_id + '" is empty!')
        return found


    def int_build(self, target_file: zipfile.ZipFile) -> etree.Element:
        if not self.int_validate(False):
            return
        
        self._build_id = self._book_obj.int_get_next_build_id()
        main_node = etree.Element('dir')
        main_node.set('name', self._build_id )

        target_file.mkdir(self.int_get_build_path(False))

        for content in self._contents:
            content_node = content.int_build(target_file)
            if content_node != None:
                main_node.append(content_node)
        
        return main_node


    def int_get_first_image(self) -> ecmbContentImage:
        for content in self._contents:
            if type(content) == ecmbContentImage:
                return content
            image = content.int_get_first_image()
            if image:
                return image


        
