from lxml import etree
from .ecmb_utils import ecmbUtils
from .ecmb_enums import *
from .ecmb_metadata_base import ecmbMetaDataBase
from .ecmb_metadata_based_on import ecmbMetaDataBasedOn

class ecmbMetaData(ecmbMetaDataBase):

    _metadata_based_on_obj = None

    def __init__(self):
        self._metadata_based_on_obj = ecmbMetaDataBasedOn()
        super().__init__()


    def based_on(self) -> ecmbMetaDataBasedOn:
        return self._metadata_based_on_obj

    
    def set_volume(self, volume: int) -> None:
        if volume != None:
            ecmbUtils.validate_int(True,  'volume', volume, 1)
        self._data['volume'] = (volume, {})


    def set_description(self, description: str) -> None:
        ecmbUtils.validate_str_or_none(True,  'description', description)
        self._data['description'] = (description, {})


    def add_genre(self, genre: str) -> None:
        ecmbUtils.validate_not_empty_str(True,  'genre', genre)
        if not self._data.get('genres'):
            self._data['genres'] = []
        self._data['genres'].append(('genre', genre, {}))


    def add_content_warning(self, content_warning: CONTENT_WARNING) -> None:
        content_warning = ecmbUtils.enum_value(content_warning)

        ecmbUtils.validate_enum(True, 'content_warning', content_warning, CONTENT_WARNING)
        if not self._data.get('warnings'):
            self._data['warnings'] = []
        self._data['warnings'].append(('warning', content_warning, {}))

    
    def int_validate(self) -> None:
        title = self._data.get('title')
        title = title[0] if type(title) == tuple else None
        if type(title) != str or title == '':
            ecmbUtils.raise_exception(f'the book-title is missing! Please use book.metadata().set_title("My Book Title")')

        self._metadata_based_on_obj.int_validate()


    def int_build(self) -> etree.Element:
        self.int_validate()

        found = False
        main_node = etree.Element('metadata')

        if self._build(main_node):
            found = True

        based_on_node = self._metadata_based_on_obj.int_build()
        if based_on_node != None:
            found = True
            main_node.append(based_on_node)

        if found:
            return main_node
        return None

