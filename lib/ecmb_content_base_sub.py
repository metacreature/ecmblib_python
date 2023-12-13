from __future__ import annotations
from io import BytesIO
from .ecmb_utils import ecmbUtils
from .ecmb_content_base import ecmbContentBase
from .ecmb_content_image import ecmbContentImage

class ecmbContentBaseSub(ecmbContentBase):

    _contents = None
    
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


    def add_folder(self, uid_or_folder: str|ecmbContentFolder = None) -> ecmbContentFolder:
        folder_obj = None

        if type(uid_or_folder) == ecmbContentFolder:
            folder_obj = uid_or_folder
        elif type(uid_or_folder) == str or uid_or_folder == None:
            folder_obj = ecmbContentFolder(self._book_obj, uid_or_folder)
        else:
            ecmbUtils.raise_exception('please provide ecmbContentFolder, a unique_id or None')
            
        folder_obj.int_set_parent(self)
        self._contents.append(folder_obj)

        return folder_obj
    

    def int_contains(self, obj: ecmbContentBase) -> bool:
        unique_id = obj.get_unique_id()
        for content in self._contents:
            if unique_id == content.get_unique_id() or (type(content) != ecmbContentImage and content.int_contains(obj)):
                return True
        return False



# for type-hinting and and type-check in combination with "from __future__ import annotations"
# can't include them on top coz these ar subclasses of ecmbNavigationBaseSub
from .ecmb_content_folder import ecmbContentFolder


        
