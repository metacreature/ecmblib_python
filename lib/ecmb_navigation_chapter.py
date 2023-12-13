from typing import  Callable
from .ecmb_utils import ecmbUtils
from .ecmb_navigation_base_sub import ecmbNavigationBaseSub
from .ecmb_content_folder import ecmbContentFolder
from .ecmb_content_image import ecmbContentImage


class ecmbNavigationChapter(ecmbNavigationBaseSub):

    _target_folder_obj = None

    def __init__(self, book_obj, label: str, folder: str|ecmbContentFolder, target: str|ecmbContentImage, title:str = None):
        super()._init(book_obj, label, title)
        super()._set_target(target)


        target_folder_obj = None
        if type(folder) == ecmbContentFolder or type(folder) == str and folder != '':
            target_folder_obj = self._book_obj.int_get_content(folder)
        else:
            ecmbUtils.raise_exception('folder must be either an unique_id or an ecmbContentFolder at chapter"' + self._label + '"!')

        if not target_folder_obj:
            ecmbUtils.raise_exception('the given folder was not found in the book at chapter "' + self._label + '"!')

        self._target_folder_obj = target_folder_obj


    def int_validate(self, warnings: bool|Callable) -> bool:
        if not self._target_folder_obj.int_contains(self._target_image_obj):
            ecmbUtils.write_warning(warnings, 'given target-image is not part of the chapter\'s target-folder at chapter "' + self._label + '"!')

        parent_folder = self._parent_navigation_obj.int_parent_chapter_folder()
        if parent_folder and not parent_folder.int_contains(self._target_folder_obj):
            ecmbUtils.write_warning(warnings, 'the target-folder is not part of parent chapter\'s target-folder at  chapter "' + self._label + '"!')

        super().int_validate(warnings)

        return True
    

    def int_parent_chapter_folder(self) -> ecmbContentFolder:
        return self._target_folder_obj