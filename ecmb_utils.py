import re, inspect
from enum import Enum
from typing import Callable


class ecmbException(Exception):
    pass

class ecmbUtils():
    
    @staticmethod
    def get_caller(stack_nr: int = 0) -> str:
        stack_nr += 1
        stack = inspect.stack()
        classname = stack[stack_nr][0].f_locals["self"].__class__.__name__
        methodname = stack[stack_nr][0].f_code.co_name
        return f'{classname}.{methodname}():'
    

    @staticmethod
    def write_warning(warnings: bool|Callable, msg: str, stack_nr: int = 0) -> None:
        caller = ecmbUtils.get_caller(stack_nr + 1)
        if warnings == True:
            print(f'\033[1;33;40m  -- WARNING: {caller} {msg}\033[0m', flush=True)
        elif callable(warnings):
            warnings(f'{caller} {msg}')

    
    @staticmethod
    def raise_exception(msg: str, stack_nr: int = 0) -> None:
        caller = ecmbUtils.get_caller(stack_nr + 1)
        raise ecmbException(f'{caller} {msg}')


    @staticmethod
    def enum_value(value) -> str:
        if isinstance(value, Enum):
            return value.value
        return value


    @staticmethod
    def validate_str_or_none(raise_exception: bool, varname: str,  value, stack_nr: int = 0) -> bool:
        if value != None and type(value) != str:
            if raise_exception:
                ecmbUtils.raise_exception(f'{varname} has to be a string or None', stack_nr + 1)
            return False
        return True
    

    @staticmethod
    def validate_not_empty_str(raise_exception: bool, varname: str,  value, stack_nr: int = 0) -> bool:
        if type(value) != str or value == '':
            if raise_exception:
                ecmbUtils.raise_exception(f'{varname} has to be a not empty string', stack_nr + 1)
            return False
        return True
    

    @staticmethod
    def validate_int(raise_exception: bool, varname: str,  value, min_value: int = None, max_value: int = None, stack_nr: int = 0) -> bool:
        if type(value) != int or (min_value and value < min_value) or (max_value and value > max_value):
            if raise_exception:
                msg = f'{varname} has to be as integer'
                msg += ' >= ' + str(min_value) if min_value else ''
                msg += ' <= ' + str(max_value) if max_value else ''
                ecmbUtils.raise_exception(msg, stack_nr + 1)
            return False
        return True
    

    @staticmethod
    def validate_enum(raise_exception: bool, varname: str,  value, enum_class: Enum, stack_nr: int = 0) -> bool:
        
        enum_values = [e.value for e in enum_class]
        if not value or type(value) != str or not value in enum_values:
            if raise_exception:
                ecmbUtils.raise_exception(f'{varname} has to be one of these values: "'+('", "'.join(enum_values)) +'"', stack_nr + 1)
            return False
        return True
    

    @staticmethod
    def validate_regex(raise_exception: bool, varname: str,  value, regex: str, stack_nr: int = 0) -> bool:
        if type(value) != str or not re.match(regex, value):
            if raise_exception:
                ecmbUtils.raise_exception(f'{varname} has to be as string and match: "{regex}"', stack_nr + 1)
            return False
        return True
    