from typing import Union, Tuple
import logging
import json

log = logging.getLogger(__name__)

Value = Union[bool, int, float, str]
Token = Union[dict, list, Value]


def _format_trace(trace: list) -> str:
    return ".".join((str(i) for i in ["$"] + trace))


def _eval_macro(token: Token, macros: dict, trace: list) -> Tuple[Token, bool]:
    log.debug("%s: eval macro %s", _format_trace(trace), json.dumps(token))

    if '__macro' in token:
        name = token['__macro']
        macro, extend = macros[name], False
    elif '__macro!' in token:
        name = token['__macro!']
        macro, extend = macros[name], True
    else:
        raise Exception('Illegal state')

    return traverse(macro['template'], macros, trace + [name + "(template)"])[0], extend


def _is_macro(token: Token) -> bool:
    return isinstance(token, dict) and ('__macro' in token or '__macro!' in token)


def traverse(token: Token, macros: dict, trace: list) -> Tuple[Token, bool]:
    if _is_macro(token):
        log.debug("%s: is macro", _format_trace(trace))
        # do macro
        return _eval_macro(token, macros, trace)

    elif isinstance(token, dict):
        log.debug("%s: is dict", _format_trace(trace))

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
        log.debug("%s: is list", _format_trace(trace))

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
        log.debug("%s: is value", _format_trace(trace))

        # do value
        return token, False
