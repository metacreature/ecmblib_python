import zipfile
from typing import Self
from io import BytesIO
from lxml import etree
from typing import Callable
from .ecmb_utils import ecmbUtils
from .ecmb_content_base import ecmbContentBase
from .ecmb_image import ecmbImage

class ecmbFolder(ecmbContentBase):

    _contents = None

    def __init__(self, book_obj, unique_id: str = None):
        self._init(book_obj, unique_id)
        self._contents = []
        
    
    def add_image(self, src_or_image: str|BytesIO|ecmbImage, src_left: str|BytesIO = None, src_right: str|BytesIO = None, unique_id: str = None) -> ecmbImage:
        image_obj = None
        if type(src_or_image) == BytesIO or ecmbUtils.validate_not_empty_str(False, 'src_or_image', src_or_image):
            image_obj = ecmbImage(self._book_obj, src_or_image, src_left, src_right, unique_id)
        elif type(src_or_image) == ecmbImage:
            image_obj = src_or_image
        else:
            ecmbUtils.raise_exception('please provide ecmbImage, BytesIO or a path to an existing image-file')
        
        image_obj.int_set_parent(self)
        self._contents.append(image_obj)

        return image_obj


    def add_folder(self, uid_or_folder: str|Self = None) -> Self:
        folder_obj = None

        from .ecmb_content import ecmbContent
        if ecmbUtils.validate_str_or_none(False, 'uid_or_folder', uid_or_folder):
            folder_obj = ecmbFolder(self._book_obj, uid_or_folder)
        elif type(uid_or_folder) == ecmbFolder and type(uid_or_folder) != ecmbContent:
            folder_obj = uid_or_folder
        else:
            ecmbUtils.raise_exception('please provide ecmbFolder, a unique_id or None')
            
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
    






        
