import zipfile
from typing import Self
from io import BytesIO
from lxml import etree
from typing import Callable
from .ecmb_utils import ecmbUtils
from .ecmb_content_base import ecmbContentBase
from .ecmb_content_image import ecmbContentImage

class ecmbContentFolder(ecmbContentBase):

    _contents = None

    def __init__(self, book_obj, unique_id: str = None):
        self._init(book_obj, unique_id)
        self._contents = []
        
    
    def add_image(self, src_or_image: str|BytesIO|ecmbContentImage, src_left: str|BytesIO = None, src_right: str|BytesIO = None, unique_id: str = None) -> ecmbContentImage:
        image_obj = None
        if type(src_or_image) == ecmbContentImage:
            image_obj = src_or_image
        elif type(src_or_image) == BytesIO or type(src_or_image) == str:
            image_obj = ecmbContentImage(self._book_obj, src_or_image, src_left, src_right, unique_id)     
        else:
            ecmbUtils.raise_exception('please provide ecmbContentImage, BytesIO or a path to an existing image-file')
        
        image_obj.int_set_parent(self)
        self._contents.append(image_obj)

        return image_obj


    def add_folder(self, uid_or_folder: str|Self = None) -> Self:
        folder_obj = None

        from .ecmb_content import ecmbContent
        if type(uid_or_folder) == ecmbContentFolder and type(uid_or_folder) != ecmbContent:
            folder_obj = uid_or_folder
        elif type(uid_or_folder) == str or uid_or_folder == None:
            folder_obj = ecmbContentFolder(self._book_obj, uid_or_folder)
        else:
            ecmbUtils.raise_exception('please provide ecmbContentFolder, a unique_id or None')
            
        folder_obj.int_set_parent(self)
        self._contents.append(folder_obj)

        return folder_obj
    

    def int_validate(self, warnings: bool|Callable) -> bool:
        found = False
        for content in self._contents:
            if content.int_validate(warnings):
                found = True

        if not found:
            ecmbUtils.write_warning(warnings, 'folder with the unique_id "' + self._unique_id + '" is empty!')
        return found


    def int_build(self, target_file: zipfile.ZipFile) -> etree.Element:
        if not self.int_validate(False):
            return
        
        self._build_id = self._book_obj.int_get_next_build_id()
        main_node = etree.Element('dir')
        main_node.set('name', self._build_id )

        target_file.mkdir(self.int_get_build_path())

        for content in self._contents:
            content_node = content.int_build(target_file)
            if content_node != None:
                main_node.append(content_node)
        
        return main_node
    

    def int_contains(self, obj: ecmbContentBase) -> bool:
        unique_id = obj.get_unique_id()
        for content in self._contents:
            if unique_id == content.get_unique_id() or (type(content) != ecmbContentImage and content.int_contains(obj)):
                return True
        return False






        
