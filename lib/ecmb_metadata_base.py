from abc import ABC, abstractmethod
from lxml import etree
from .ecmb_utils import ecmbUtils
from .ecmb_enums import *

class ecmbMetaDataBase(ABC):

    _data = None

    def __init__(self):
       self._data = {}


    def set_isbn(self, isbn: str) -> None:
        if isbn != None and isbn != '':
            ecmbUtils.validate_regex(True, 'isbn', isbn, '^([0-9]{10}|[0-9]{13})$')
        self._data['isbn'] = (isbn, {})

    
    def set_publisher(self, publisher: str, href: str = None) -> None:
        ecmbUtils.validate_str_or_none(True, 'publisher', publisher)
        if href != None and href != '':
            ecmbUtils.validate_regex(True, 'href', href, '^(http|https)://.+$')
        self._data['publisher'] = (publisher, {'href': href})


    def set_publishdate(self, publishdate: str) -> None:
        if publishdate != None and publishdate != '':
            ecmbUtils.validate_regex(True, 'publishdate', publishdate, '^[0-9]{4}(-[0-9]{2}-[0-9]{2})?$')
        self._data['publishdate'] = (publishdate, {})

    
    def set_title(self, title: str) -> None:
        ecmbUtils.validate_not_empty_str(True, 'title', title)
        self._data['title'] = (title, {})
        

    def add_author(self, name: str, authortype: AUTHOR_TYPE = AUTHOR_TYPE.AUTHOR, href: str = None) -> None:
        authortype = ecmbUtils.enum_value(authortype)

        ecmbUtils.validate_not_empty_str(True, 'name', name)
        ecmbUtils.validate_enum(True, 'authortype', authortype, AUTHOR_TYPE)
        if href != None and href != '':
            ecmbUtils.validate_regex(True, 'href', href, '^(http|https)://.+$')
            
        if not self._data.get('authors'):
            self._data['authors'] = []
        self._data['authors'].append(('author', name, {'type': authortype, 'href': href}))


    @abstractmethod
    def int_validate(self) -> None:
        pass


    @abstractmethod
    def int_build(self) -> etree.Element:
        pass


    def _build(self, main_node: etree.Element) -> bool:
        found = False
        for node_name, node_data in self._data.items():
            if type(node_data) == list:
                found_list = False
                main_node_list = etree.Element(node_name)
                for list_data in node_data:
                    value = self._clean_value(list_data[1])
                    if value != None:
                        found_list = True
                        etree.SubElement(main_node_list, list_data[0], attrib = self._clean_attributes(list_data[2])).text = value
                if found_list:
                    found = True
                    main_node.append(main_node_list)
            else:
                value = self._clean_value(node_data[0])
                if value != None:
                    found = True
                    etree.SubElement(main_node, node_name, attrib = self._clean_attributes(node_data[1])).text = value
        return found


    def _clean_attributes(self, attributes:dict) -> dict:
        result = {}
        if type(attributes) == dict:
            for attr_name, attr_value in attributes.items():
                attr_value = self._clean_value(attr_value)
                if attr_value != None:
                    result[attr_name] = attr_value
        return result
    

    def _clean_value(self, value) -> str:
       if value != None and value != '':
            if type(value) == bool:
                value = 'true' if value else 'false'
            return str(value)
       return None