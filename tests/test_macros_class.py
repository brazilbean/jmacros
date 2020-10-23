from jmacros.macros import ClassMacro
from tests.utils import traverse_and_compare
from jmacros.traversal import traverse

macro_defs = {
    "foobar": {
        "template": {"a": "b"}
    },
    "foolist": {
        "template": [1, 2, 3]
    },
    "foorecurse": {
        "template": {
            "foo": {"__macro": "foobar"}
        }
    },
    "foojq": {
        "schema": {
            "type": "object",
            "required": ["number", "obj"],
            "properties": {
                "number": {"type": "number"},
                "obj": {"type": "object"}
            }
        },
        "template": {
            "foo": "the number is ${.number}",
            "bar": {"__jq": ".obj"}
        }
    },
    "foosub": {
        "template": {"%.%": "the key was %"}
    }
}

macros = [ClassMacro(macro_defs)]


def test_class_macro_in_place():
    obj = {
        "foo": {"__macro": "foobar"}
    }
    foo, extend = traverse(obj, macros, [])
    assert foo == {
        "foo": {"a": "b"}
    }


def test_class_macro_in_place_array():
    obj = {
        "foo": [1, {"__macro": "foobar"}, 3]
    }
    foo, extend = traverse(obj, macros, [])
    assert foo == {
        "foo": [1, {"a": "b"}, 3]
    }


def test_class_macro_extend():
    obj = {
        "foo": {"__macro!": "foobar"}
    }
    foo, extend = traverse(obj, macros, [])
    assert foo == {"a": "b"}


def test_class_macro_extend_array():
    obj = [1, {"__macro!": "foolist"}, 3]
    foo, extend = traverse(obj, macros, [])
    assert foo == [1, 1, 2, 3, 3]


def test_class_recursive_macro():
    obj = {
        "foo": {"__macro": "foorecurse"}
    }
    foo, extend = traverse(obj, macros, [])
    assert foo == {
        "foo": {
            "foo": {"a": "b"}
        }
    }


def test_class_jq_template():
    obj = {
        "foo": {"__macro": "foojq", "number": 7, "obj": {"bar": 7}}
    }
    exp = {
        "foo": {"foo": "the number is 7", "bar": {"bar": 7}},
    }
    traverse_and_compare(obj, exp, macros)


def test_class_order_preserved():
    obj = {
        "foo": {"__macro": "foobar"},
        "baz": {"__macro!": "foobar"},
        "bar": {"__macro": "foobar"}
    }
    exp = {
        "foo": {"a": "b"},
        "a": "b",
        "bar": {"a": "b"}
    }
    result = traverse(obj, macros, [])[0]
    assert len(exp) == len(result)
    for k1, k2 in zip(exp, result):
        assert k1 == k2


def test_percent_sub():
    obj = {
        "foo": {"__macro!": "foosub"}
    }
    exp = {
        "foo.foo": "the key was foo"
    }
    traverse_and_compare(obj, exp, macros)