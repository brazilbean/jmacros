from traversal import traverse


def test_traverse():
    obj = {
        'foo': 'bar'
    }
    foo, extend = traverse(obj, {})
    assert obj == foo
