from typing import Union, Tuple

Value = Union[bool, int, float, str]
Token = Union[dict, list, Value]


def _eval_macro(token: Token, macros: dict) -> Tuple[Token, bool]:
    if '__macro' in token:
        macro, extend = macros[token['__macro']], False
    elif '__macro!' in token:
        macro, extend = macros[token['__macro!']], True
    else:
        raise Exception('Illegal state')

    return macro['template'], extend


def _is_macro(token: Token) -> bool:
    return isinstance(token, dict) and ('__macro' in token or '__macro!' in token)


def traverse(token: Token, macros: dict) -> Tuple[Token, bool]:
    if _is_macro(token):
        # do macro
        return _eval_macro(token, macros)

    elif isinstance(token, dict):
        # do dict
        kvs = []
        for key, value in token.items():
            new_value, extend = traverse(value, macros)
            if extend:
                assert isinstance(new_value, dict)
                # TODO - modify keys by parent key
                kvs.extend(new_value.items())
            else:
                kvs.append((key, new_value))
        return {k: v for k, v in kvs}, False

    elif isinstance(token, list):
        # do list
        items = []
        for item in token:
            new_item, extend = traverse(item, macros)
            if extend:
                assert isinstance(new_item, list)
                items.extend(new_item)
            else:
                items.append(new_item)
        return items, False

    else:
        # do value
        return token, False
