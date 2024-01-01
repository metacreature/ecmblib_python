"""
 File: ecmb_metadata.py
 Copyright (c) 2023 Clemens K. (https://github.com/metacreature)
 
 MIT License
 
 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:
 
 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.
 
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 SOFTWARE.
"""

from lxml import etree
from .ecmb_utils import ecmbUtils
from .ecmb_enums import *
from .ecmb_metadata_base import ecmbMetaDataBase
from .ecmb_metadata_original import ecmbMetaDataOriginal
from .ecmb_metadata_based_on import ecmbMetaDataBasedOn

class ecmbMetaData(ecmbMetaDataBase):

    _metadata_original_obj = None
    _metadata_based_on_obj = None

    def __init__(self):
        self._metadata_original_obj = ecmbMetaDataOriginal()
        self._metadata_based_on_obj = ecmbMetaDataBasedOn()
        super().__init__()


    def get_original(self) -> ecmbMetaDataOriginal:
        return self._metadata_original_obj
    
    original: ecmbMetaDataOriginal = property(get_original)


    def get_based_on(self) -> ecmbMetaDataBasedOn:
        return self._metadata_based_on_obj
    
    based_on: ecmbMetaDataBasedOn = property(get_based_on)


    def set_title(self, title: str) -> None:
        ecmbUtils.validate_not_empty_str(True, 'title', title)
        self._data['title'] = (title, {})

    
    def set_volume(self, volume: int) -> None:
        if volume != None:
            ecmbUtils.validate_int(True,  'volume', volume, 1)
        self._data['volume'] = (volume, {})


    def set_description(self, description: str) -> None:
        ecmbUtils.validate_str_or_none(True,  'description', description)
        self._data['description'] = (description, {})


    def set_note(self, note: str) -> None:
        ecmbUtils.validate_str_or_none(True, 'note', note)
        self._data['note'] = (note, {})


    def add_editor(self, name: str, editortype: EDITOR_TYPE, href: str = None) -> None:
        editortype = ecmbUtils.enum_value(editortype)

        ecmbUtils.validate_not_empty_str(True, 'name', name)
        ecmbUtils.validate_enum(True, 'editortype', editortype, EDITOR_TYPE)
        if href != None and href != '':
            ecmbUtils.validate_regex(True, 'href', href, '^(http|https)://.+$')
            
        if not self._data.get('editors'):
            self._data['editors'] = []
        self._data['editors'].append(('editor', name, {'type': editortype, 'href': href}))


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

        self._metadata_original_obj.int_validate()
        self._metadata_based_on_obj.int_validate()


    def int_build(self) -> etree.Element:
        self.int_validate()

        found = False
        main_node = etree.Element('metadata')

        if self._build(main_node):
            found = True

        original_node = self._metadata_original_obj.int_build()
        if original_node != None:
            found = True
            main_node.append(original_node)

        based_on_node = self._metadata_based_on_obj.int_build()
        if based_on_node != None:
            found = True
            main_node.append(based_on_node)

        if found:
            return main_node
        return None

