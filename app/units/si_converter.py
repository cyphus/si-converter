#!/usr/bin/env python3
from .tokenizer import (Token, TokenType)
from .units import UNITS

def si_unit_lookup_table(units=UNITS):
    """
    Creates a lookup table from all possible input unit names and symbols to
    their corresponding SI unit.
    """
    return {
        **{ u.name: (u.si_equivalent, u.coefficient) for u in units
            if u.name is not None},
        **{ u.symbol: (u.si_equivalent, u.coefficient) for u in units }
    }

def si_convert(tokens):
    """
    Converts all unit tokens to their SI equivalent with the appropriate
    multiplication factor. All other tokens are left unmodified.
    """
    si_tokens = []
    si_units = si_unit_lookup_table()
    for token in tokens:
        if token.type != TokenType.UNIT:
            si_tokens.append(token)
            continue
        si_text, si_coefficient = si_units[token.text]
        si_tokens.append(Token(TokenType.UNIT, si_text, si_coefficient))
    return si_tokens
