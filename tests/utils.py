import logging
from typing import Dict

from jmacros.traversal import Token, MacroTypeDefinition, traverse


def traverse_and_compare(obj: Token, exp: Token, macros: Dict[str, MacroTypeDefinition]):
    result, expand = traverse(obj, macros, [])
    logging.debug(f"Result: {result}")
    logging.debug(f"Expect: {exp}")
    assert result == exp
