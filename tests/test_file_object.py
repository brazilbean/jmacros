from jmacros.macros.file_macros import get_file_macros, _convert_to_uri
from tests.utils import traverse_and_compare

macros = get_file_macros(_convert_to_uri(__file__))


def test_file_object_simple():
    obj = {"foo": {"__file_object": "files/a-json-object.json"}}
    exp = {"foo": {"a": "b"}}
    traverse_and_compare(obj, exp, macros)


def test_file_object_extend():
    obj = {"foo": {"__file_object!": "files/a-json-object.json"}, "bar": "baz"}
    exp = {"a": "b", "bar":"baz"}
    traverse_and_compare(obj, exp, macros)


def test_file_object_recursion():
    obj = {"foo": {"__file_object": "files/a-json-object-with-refs.json"}}
    exp = {"foo": {"foo": {"a": "b"}}}
    traverse_and_compare(obj, exp, macros)


def test_file_string():
    obj = {"foo": {"__file_string": "files/simple-string.txt"}}
    exp = {"foo": "word"}
    traverse_and_compare(obj, exp, macros)
