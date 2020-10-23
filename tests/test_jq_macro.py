from macros import JqSubstitutionMacro
from tests.utils import traverse_and_compare

macros = [
    JqSubstitutionMacro({"foo": {"bar": 7}})
]


def test_is_macro():
    macro = macros[0]
    assert macro.is_macro({"__jq": ".foo"})
    assert macro.is_macro("${.foo}")


def test_jq():
    obj = {
        "__jq": ".foo"
    }
    traverse_and_compare(obj, {"bar": 7}, macros)


def test_jq_nested():
    obj = {
        "foo": {
            "__jq": ".foo"
        }
    }
    exp = {"foo": {"bar": 7}}
    traverse_and_compare(obj, exp, macros)


def test_jq_str():
    obj = {"foo": "a number: ${.foo.bar}"}
    exp = {"foo": "a number: 7"}
    traverse_and_compare(obj, exp, macros)


def test_jq_obj_in_str():
    obj = "an obj: ${.foo}"
    exp = 'an obj: {"bar": 7}'
    traverse_and_compare(obj, exp, macros)