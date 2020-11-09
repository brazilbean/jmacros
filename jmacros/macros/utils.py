import json
import logging
from copy import deepcopy

from jmacros.traversal import Token, MacroList, format_trace

log = logging.getLogger(__name__)


def macro_eval(fun):
    def eval_macro(self, token: Token, macros: MacroList, trace: list):
        log.debug("%s: evaluating as %s: %s", format_trace(trace), self.__class__.__name__, json.dumps(token))
        return fun(self, deepcopy(token), macros, trace)
    return eval_macro


