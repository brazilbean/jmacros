import json
import logging
import re
from typing import Tuple
import importlib

from jmacros.macros.utils import macro_eval
from jmacros.traversal import MacroTypeDefinition, Token, MacroList, traverse

log = logging.getLogger(__name__)


has_jq = importlib.util.find_spec('jq') is not None
if has_jq:
    log.info("jq module detected")
    import jq
else:
    log.info("no jq module detected")
    import subprocess


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
                new_str = json.dumps(new_token) if isinstance(new_token, dict) or isinstance(new_token, list) else str(
                    new_token)
                token = token.replace(match.group(1), new_str)
                log.debug(f"After replacement: {token}")
            return token, False
