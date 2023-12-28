"""
 File: ecmb_metadata_based_on.py
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


class ecmbMetaDataBasedOn(ecmbMetaDataBase):
    
    def set_type(self, book_type: BASED_ON_BOOK_TYPE) -> None:
        book_type = ecmbUtils.enum_value(book_type)

        if book_type != None and book_type != '':
            ecmbUtils.validate_enum(True, 'book_type', book_type, BASED_ON_BOOK_TYPE)
        self._data['type'] = (book_type, {})


    def set_title(self, title: str) -> None:
        ecmbUtils.validate_str_or_none(True, 'title', title)
        self._data['title'] = (title, {})
    

    def int_validate(self) -> None:
        found = False
        for value in self._data.values():
            if type(value) == list:
                for list_value in value:
                    if list_value[1] != None and list_value[1] != '':
                        found = True
            else:
                if value[0] != None and value[0] != '':
                    found = True
        if not found:
            return

        title = self._data.get('title')
        title = title[0] if type(title) == tuple else None
        if type(title) != str or title  == '':
            ecmbUtils.raise_exception(f'if you provide a based-on-information the title is mandatory! Please use book.based_on().set_title("My Book Title")')


    def int_build(self) -> etree.Element:
        self.int_validate()

        found = False
        main_node = etree.Element('basedon')

        if self._build(main_node):
            found = True

        if found:
            return main_node
        return None