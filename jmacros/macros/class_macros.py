import json
import logging
from typing import Tuple

from jsonschema import validate, ValidationError

from jmacros.macros.jq_substitution import JqSubstitutionMacro
from jmacros.macros.utils import macro_eval
from jmacros.traversal import MacroTypeDefinition, Token, format_trace, traverse, MacroList

log = logging.getLogger(__name__)


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
