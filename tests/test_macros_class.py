from macros import ClassMacro
from traversal import traverse

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
    }
}

macros = {
    "class": ClassMacro(macro_defs)
}


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