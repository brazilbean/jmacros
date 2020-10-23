import json
import logging
from copy import deepcopy
from typing import Tuple
from jsonschema import validate, ValidationError
import re
from jmacros.traversal import MacroTypeDefinition, Token, format_trace, traverse, MacroList

log = logging.getLogger(__name__)

import importlib
has_jq = importlib.util.find_spec('jq') is not None
if has_jq:
    log.info("jq module detected")
    import jq
else:
    log.info("no jq module detected")
    import subprocess


def macro_eval(fun):
    def eval_macro(self, token: Token, macros: MacroList, trace: list):
        log.debug("%s: evaluating as %s: %s", format_trace(trace), self.__class__.__name__, json.dumps(token))
        return fun(self, deepcopy(token), macros, trace)
    return eval_macro


def jq_select(expression: str, obj):
    if has_jq:
        return jq.compile(expression).input(obj).all()
    else:
        return json.loads(subprocess.check_output(['jq', expression], input=json.dumps(obj).encode()))


class JqSubstitutionMacro(MacroTypeDefinition):
    SUB_REGEX = re.compile(r'(\$\{.*?\})')

    def __init__(self, data):
        self.data = data

    def is_macro(self, token: Token) -> bool:
        if isinstance(token, dict) and '__jq' in token:
            return True
        if isinstance(token, str) and self.SUB_REGEX.search(token):
            return True
        return False

    @macro_eval
    def eval_macro(self, token: Token, macros: MacroList, trace: list) -> Tuple[Token, bool]:
        if isinstance(token, dict):
            expression = token.pop('__jq')
            new_token = jq_select(expression, self.data)
            return traverse(new_token, macros, trace + [f"<{expression}>"])
        else:  # str
            while match := self.SUB_REGEX.search(token):
                new_token = jq_select(match.group(1)[2:-1], self.data)
                new_str = json.dumps(new_token) if isinstance(new_token, dict) or isinstance(new_token, list) else str(new_token)
                token = token.replace(match.group(1), new_str)
                log.debug(f"After replacement: {token}")
            return token, False


class ClassMacro(MacroTypeDefinition):
    def __init__(self, macro_definitions: dict):
        self.macro_definitions = macro_definitions

    def is_macro(self, token: Token) -> bool:
        return isinstance(token, dict) and ('__macro' in token or '__macro!' in token)

    @macro_eval
    def eval_macro(self, token: Token, macros: MacroList, trace: list) -> Tuple[Token, bool]:
        # Get macro definition
        if '__macro' in token:
            name = token.pop('__macro')
            macro, extend = self.macro_definitions[name], False
        elif '__macro!' in token:
            name = token.pop('__macro!')
            macro, extend = self.macro_definitions[name], True
        else:
            raise Exception('Illegal state')

        new_trace = trace + [name + "(template)"]

        # Validate input against the schema
        if 'schema' in macro:
            try:
                validate(token, macro['schema'])
            except ValidationError as err:
                log.error(
                    "%s: schema validation error on input to macro %s: %s",
                    format_trace(trace), name, repr(err)
                )
                raise err

        # Replace '%' in template with key
        template = json.loads(json.dumps(macro['template']).replace("%", str(trace[-1])))

        # Populate template from input (i.e. the token)
        subs_macros = [JqSubstitutionMacro(token)]
        result = traverse(template, subs_macros, new_trace)[0]

        return traverse(result, macros, new_trace)[0], extend
