from traversal import traverse

macros = {
    "foobar": {
        "template": {"a": "b"}
    },
    "foolist": {
        "template": [1, 2, 3]
    }
}


def test_traverse():
    obj = {
        "foo": "bar",
        "baz": [1, 2, 3],
        "quux": {"a": "b"}
    }
    foo, extend = traverse(obj, macros)
    assert obj == foo


def test_traverse_macro_in_place():
    obj = {
        "foo": {"__macro": "foobar"}
    }
    foo, extend = traverse(obj, macros)
    assert foo == {
        "foo": {"a": "b"}
    }


def test_traverse_macro_in_place_array():
    obj = {
        "foo": [1, {"__macro": "foobar"}, 3]
    }
    foo, extend = traverse(obj, macros)
    assert foo == {
        "foo": [1, {"a": "b"}, 3]
    }


def test_traverse_macro_extend():
    obj = {
        "foo": {"__macro!": "foobar"}
    }
    foo, extend = traverse(obj, macros)
    assert foo == {"a": "b"}


def test_traverse_macro_extend_array():
    obj = [1, {"__macro!": "foolist"}, 3]
    foo, extend = traverse(obj, macros)
    assert foo == [1, 1, 2, 3, 3]

