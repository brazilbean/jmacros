import os
import pathlib
import urllib.parse
import urllib.request
from io import BufferedReader
from typing import Tuple

import yaml

from jmacros.macros.utils import macro_eval
from jmacros.traversal import MacroTypeDefinition, Token, MacroList, traverse


def _convert_to_uri(path: str) -> str:
    return pathlib.Path(path).absolute().as_uri()


def _resolve_uri(base: str, reference: str) -> str:
    return urllib.parse.urljoin(base, reference)


def _get_file_stream(uri: str) -> BufferedReader:
    return urllib.request.urlopen(uri)


def _read_file_object(uri: str) -> dict:
    return yaml.load(_get_file_stream(uri), yaml.FullLoader)


def _read_file_string(uri: str) -> str:
    with _get_file_stream(uri) as f:
        return f.read().decode()


def get_file_macros(base_uri: str = None):
    base_url = base_uri or _convert_to_uri(os.getcwd())
    return [FileStringMacro(base_url), FileObjectMacro(base_url)]


class FileStringMacro(MacroTypeDefinition):
    def __init__(self, base_url):
        self.base_url = base_url

    def is_macro(self, token: Token) -> bool:
        return isinstance(token, dict) and ('__file_string' in token)

    @macro_eval
    def eval_macro(self, token: Token, macros: MacroList, trace: list) -> Tuple[Token, bool]:
        reference = token.pop("__file_string")
        url = _resolve_uri(self.base_url, reference)
        result = _read_file_string(url)
        result, _ = traverse(result, get_file_macros(url), trace + [f"__file_string({url})"])

        return result, False


class FileObjectMacro(MacroTypeDefinition):
    def __init__(self, base_url):
        self.base_url = base_url

    def is_macro(self, token: Token) -> bool:
        return isinstance(token, dict) and ('__file_object' in token or '__file_object!' in token)

    @macro_eval
    def eval_macro(self, token: Token, macros: MacroList, trace: list) -> Tuple[Token, bool]:
        if '__file_object' in token:
            reference = token.pop('__file_object')
            extend = False
        elif '__file_object!' in token:
            reference = token.pop('__file_object!')
            extend = True
        else:
            raise Exception('Illegal state')

        url = _resolve_uri(self.base_url, reference)
        result = _read_file_object(url)
        result, _ = traverse(result, get_file_macros(url), trace + [f"__file_object({url})"])

        return result, extend
