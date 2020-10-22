from typing import Dict

from traversal import Token, MacroTypeDefinition, traverse


def traverse_and_compare(obj: Token, exp: Token, macros: Dict[str, MacroTypeDefinition]):
    result, expand = traverse(obj, macros, [])
    assert result == exp
