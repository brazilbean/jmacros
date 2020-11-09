import logging

from jmacros.traversal import Token, traverse, MacroList


def traverse_and_compare(obj: Token, exp: Token, macros: MacroList):
    result, expand = traverse(obj, macros, [])
    logging.debug(f"Result: {result}")
    logging.debug(f"Expect: {exp}")
    assert result == exp
