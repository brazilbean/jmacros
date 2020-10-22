from traversal import traverse


def test_traverse():
    obj = {
        "foo": "bar",
        "baz": [1, 2, 3],
        "quux": {"a": "b"}
    }
    foo, extend = traverse(obj, {}, [])
    assert obj == foo


