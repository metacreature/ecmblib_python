import zipfile, os, re
from lxml import etree
from typing import Callable
from .ecmb_enums import *
from .ecmb_utils import ecmbUtils, ecmbException
from .ecmb_metadata import ecmbMetaData
from .ecmb_based_on import ecmbBasedOn
from .ecmb_content import ecmbContent
from .ecmb_folder import ecmbFolder
from .ecmb_image import ecmbImage


class ecmbBook:

    _version = None
    _book_type = None
    _language = None
    _uid = None
    _width = None
    _height = None

    _content_ref = None

    _metadata_obj = None
    _content_obj = None
    _navigation_obj = None
    
    _build_id_counter = None
    _page_nr_counter = None

    def __init__(self, book_type: BOOK_TYPE, language: str, uid: str, width: int, height: int) :  
        book_type = ecmbUtils.enum_value(book_type)
        
        ecmbUtils.validate_enum(True, 'book_type', book_type, BOOK_TYPE)
        ecmbUtils.validate_regex(True, 'language', language, r'^[a-z]{2}$')
        ecmbUtils.validate_regex(True, 'uid', uid, r'^[a-z0-9_]{16,255}$')
        ecmbUtils.validate_int(True, 'width', width, 100)
        ecmbUtils.validate_int(True, 'height', height, 100)

        self._content_ref = {}

        self._metadata_obj = ecmbMetaData()
        self._content_obj = ecmbContent(self)

        self._version = '1.0'
        self._book_type = book_type
        self._language = language
        self._uid = uid
        self._width = width
        self._height = height


    def metadata(self) -> ecmbMetaData:
        return self._metadata_obj

    
    def based_on(self) -> ecmbBasedOn:
        return self._metadata_obj.based_on()
    
    
    def content(self) -> ecmbContent:
        return self._content_obj
    
    
    def validate(self, warnings: bool|Callable = True) -> None:
        self._metadata_obj.int_validate()
        self._page_nr_counter = 0
        self._content_obj.int_validate(warnings)
        if self._page_nr_counter % 2 != 0:
            ecmbUtils.write_warning(warnings, f'The Book has an an uneven page-count!')


    def write(self, file_name: str, warnings: bool|Callable = True, demo_mode: bool = False) -> None:

        self.validate(warnings)
        
        if not re.match(r'.ecmb$', file_name):
            file_name += '.ecmb'

        target_file = zipfile.ZipFile(file_name, 'w', zipfile.ZIP_DEFLATED)

        #try:
        target_file.writestr('mimetype', 'application/ecmb+zip', compress_type=zipfile.ZIP_STORED)

        root = etree.Element('book')
        root.set('version', self._version)
        root.set('type', self._book_type)
        root.set('language', self._language)
        root.set('uid', self._uid)
        root.set('width', str(self._width))
        root.set('height', str(self._height))

        metadata_node = self._metadata_obj.int_build()
        if metadata_node != None:
            root.append(metadata_node)

        self._build_id_counter = 0
        content_node = self._content_obj.int_build(target_file)
        if content_node != None:
            root.append(content_node)

        

        xml_str = etree.tostring(root, pretty_print=demo_mode)

        with open('test.xml', 'wb') as f:
            f.write(xml_str)

        #except Exception as e:
        #    target_file.close()
        #    os.remove(file_name) 
        #    raise e

        target_file.close()



    
    def int_register_content(self, content: ecmbFolder|ecmbImage) -> None:
        if content.get_unique_id() in self._content_ref.keys():
            ecmbUtils.raise_exception(f'the book contains allready content with the unique_id "' + content.get_unique_id() + '"!', 1)
        self._content_ref[content.get_unique_id()] = content


    def int_get_width(self) -> int:
        return self._width
    

    def int_get_height(self) -> int:
        return self._height
    

    def int_get_next_build_id(self) -> str:
        self._build_id_counter  += 1

        char_map = '0123456789abcdefghijklmnopqrstuvwxyz'

        build_id_int = self._build_id_counter
        build_id_str = ''

        while build_id_int > 0:
            build_id_str = char_map[build_id_int % 36] + build_id_str
            build_id_int = int((build_id_int - (build_id_int % 36))  / 36)
        
        return build_id_str
    

    def int_get_next_page_nr(self) -> int:
        self._page_nr_counter  += 1
        return self._page_nr_counter
    