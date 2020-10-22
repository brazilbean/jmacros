import json
import logging
from typing import Tuple, Dict

from traversal import MacroTypeDefinition, Token, format_trace, traverse

log = logging.getLogger(__name__)


class ClassMacro(MacroTypeDefinition):
    def __init__(self, macro_definitions: dict):
        self.macro_definitions = macro_definitions

    def is_macro(self, token: Token) -> bool:
        return isinstance(token, dict) and ('__macro' in token or '__macro!' in token)

    def eval_macro(self, token: Token, macros: Dict[str, MacroTypeDefinition], trace: list) -> Tuple[Token, bool]:
        log.debug("%s: eval macro %s", format_trace(trace), json.dumps(token))

        if '__macro' in token:
            name = token['__macro']
            macro, extend = self.macro_definitions[name], False
        elif '__macro!' in token:
            name = token['__macro!']
            macro, extend = self.macro_definitions[name], True
        else:
            raise Exception('Illegal state')

        return traverse(macro['template'], macros, trace + [name + "(template)"])[0], extend
