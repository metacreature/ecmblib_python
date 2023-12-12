import uuid, os, zipfile
from io import BytesIO
from PIL import Image
from lxml import etree
from typing import Callable
from typing import Self
from abc import ABC, abstractmethod
from .ecmb_utils import ecmbUtils
from .ecmb_enums import *

class ecmbContentBase():

    _book_obj = None
    _parent_content_obj = None

    _unique_id = None
    _build_id = None

       
    def get_unique_id(self) -> str:
        return self._unique_id
    
    
    def int_get_build_id(self) -> str:
        return self._build_id
    

    def int_set_parent(self, parent_content_obj: Self) -> None:
        if self._parent_content_obj != None:
            ecmbUtils.raise_exception(f'the content with the unique_id "' + self._unique_id + '" can\'t be added twice!', 1)
        self._parent_content_obj = parent_content_obj

    
    def int_get_build_path(self) -> str:
        if self._parent_content_obj:
            return self._parent_content_obj.int_get_build_path() + '/' + self._build_id
        return self._build_id


    def _init(self, book_obj, unique_id: str) -> None:
        
        from .ecmb import ecmbBook
        if type(book_obj) != ecmbBook:
            ecmbUtils.raise_exception(f'ecmbBook expected as the first param, but got diffrent type!', 1)

        ecmbUtils.validate_str_or_none(True,  'unique_id', unique_id)
        if not unique_id:
            unique_id = str(uuid.uuid4())

        self._unique_id = unique_id
        self._book_obj = book_obj
        self._book_obj.int_register_content(self)

    
    def _check_image(self, src: str|BytesIO, varname: str, allow_double: bool) -> (bool, str):
        error_msg = None
        
        if type(src) == BytesIO:
            error_msg = f'byte-image {varname} of unique_id "' + self._unique_id + '":'
            src.seek(0)
        elif ecmbUtils.validate_not_empty_str(False, varname, src):
            error_msg = f'image {varname}: "{src}":'
            if not os.path.exists(src):
                ecmbUtils.raise_exception(f'{error_msg} does not exist!', 1)
        else:
            ecmbUtils.raise_exception('please provide  BytesIO or a path to an existing image-file', 1)
            
        try: 
            img_obj = Image.open(src)
        except:
            ecmbUtils.raise_exception(f'{error_msg} faild to open! Maybe it\'s not an image!', 1)

        file_format = img_obj.format
        file_format = file_format.lower() if file_format else None
        if not file_format:
            ecmbUtils.raise_exception(f'{error_msg} faild to determine image-format! Maybe it\'s not an image!', 1)
        
        allowed_formats = [e.value for e in ALLOWED_IMAGE_EXTENTIONS]
        if not file_format in allowed_formats:
            ecmbUtils.raise_exception(f'{error_msg} allowed image-formats: "'+('", "'.join(allowed_formats)) +'", but "{file_format}" detected!', 1)
        
        is_double = False
        if img_obj.width != self._book_obj.int_get_width():
            if img_obj.width == self._book_obj.int_get_width() * 2:
                if not allow_double:
                    ecmbUtils.raise_exception(f'{error_msg} double-page-image detected, but not allowed in this place!', 1)
                is_double = True
            else:
                ecmbUtils.raise_exception(f'{error_msg} allowed image-width: "'+ str(self._book_obj.int_get_width()) +'", but "' + str(img_obj.width) + '" detected!', 1)
            
        if img_obj.height != self._book_obj.int_get_height():
            ecmbUtils.raise_exception(f'{error_msg} allowed image-height: "'+ str(self._book_obj.int_get_height()) +'", but "' + str(img_obj.height) + '" detected!', 1)
        
        if file_format == 'jpeg':
            file_format = 'jpg'
        
        return (is_double, file_format)
    

    def _write_image(self, target_file: zipfile.ZipFile, file_path: str, src: str|BytesIO) -> None:
        if type(src) == str:
            if not os.path.exists(src):
                ecmbUtils.raise_exception(f'{src} does not exist!')
            with open(src, 'rb') as f:
                data = f.read()
        else:
            data = src.getbuffer()

        target_file.writestr(file_path, data)


    

    @abstractmethod
    def int_validate(self, warnings: bool|Callable) -> bool:
        pass


    @abstractmethod
    def int_build(self, target_file) -> etree.Element:
        pass