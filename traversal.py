import logging
from typing import Union, Tuple, Protocol, Dict, List

log = logging.getLogger(__name__)

Value = Union[bool, int, float, str]
Token = Union[dict, list, Value]


class MacroTypeDefinition(Protocol):
    def is_macro(self, token: Token) -> bool:
        pass

    def eval_macro(self, token: Token, macros: List['MacroTypeDefinition'], trace: list) -> Tuple[Token, bool]:
        pass


MacroList = List[MacroTypeDefinition]


def format_trace(trace: list) -> str:
    return ".".join((str(i) for i in ["$"] + trace))


def traverse(token: Token, macros: MacroList, trace: list) -> Tuple[Token, bool]:
    for macro in macros:
        if macro.is_macro(token):
            log.debug("%s: is %s macro", format_trace(trace), macro.__class__.__name__)
            # do macro
            return macro.eval_macro(token, macros, trace)

    if isinstance(token, dict):
        log.debug("%s: is dict", format_trace(trace))

        # do dict
        kvs = []
        for key, value in token.items():
            new_value, extend = traverse(value, macros, trace + [key])
            if extend:
                assert isinstance(new_value, dict)
                # TODO - modify keys by parent key
                kvs.extend(new_value.items())
            else:
                kvs.append((key, new_value))
        return {k: v for k, v in kvs}, False

    elif isinstance(token, list):
        log.debug("%s: is list", format_trace(trace))

        # do list
        items = []
        for index, item in enumerate(token):
            new_item, extend = traverse(item, macros, trace + [index])
            if extend:
                assert isinstance(new_item, list)
                items.extend(new_item)
            else:
                items.append(new_item)
        return items, False

    else:
        log.debug("%s: is value", format_trace(trace))

        # do value
        return token, False
