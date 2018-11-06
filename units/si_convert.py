#!/usr/bin/env python3
from collections import deque, namedtuple
from enum import Enum
import re
from units.units import UNITS, si_unit_lookup_table

TokenType = Enum('TokenType', 'LPAREN RPAREN UNIT MUL DIV')

Token = namedtuple('Token', 'type text coefficient')
Token.__new__.__defaults__ = (None,)

TOKEN_REGEXES = {
    re.compile(r'[a-zA-Z]+'): TokenType.UNIT,
    re.compile(r'\('): TokenType.LPAREN,
    re.compile(r'\)'): TokenType.RPAREN,
    re.compile(r'\*'): TokenType.MUL,
    re.compile(r'/'): TokenType.DIV,
}


def convert_units(unit_str):
    """
    High level function to take a unit string and return its SI converted
    representation and multiplication factor.
    """
    tokens = tokenize(unit_str)
    si_tokens = si_convert(tokens)
    rpn_tokens = rpn_transform(si_tokens)
    return {
        "unit_name": ''.join(t.text for t in si_tokens),
        "multiplication_factor": coefficient(rpn_tokens),
    }


def tokenize(unit_str):
    """
    Returns a list of Tokens from the given unit string.
    """
    tokens = []
    char_index = 0
    while char_index < len(unit_str):
        for regex, token_type in TOKEN_REGEXES.items():
            # match only matches against the start of the string
            match = re.match(regex, unit_str[char_index:])
            if match is not None:
                token_text = match.group(0)
                tokens.append(Token(token_type, token_text))
                char_index += len(token_text)
                break
        else:
            # unrecognized token, raise exception
            err = "unrecognized token at pos {} of '{}'".format(
                    char_index, unit_str)
            raise ValueError(err)
    return tokens

def si_convert(tokens):
    """
    Converts all unit tokens to their SI equivalent with the appropriate
    multiplication factor. All other tokens are left unmodified.
    """
    si_tokens = []
    # TODO cache this on startup
    si_units = si_unit_lookup_table()
    for token in tokens:
        if token.type != TokenType.UNIT:
            si_tokens.append(token)
            continue
        si_text, si_coefficient = si_units[token.text]
        si_tokens.append(Token(TokenType.UNIT, si_text, si_coefficient))
    return si_tokens

def is_operator(token):
    """
    Returns true if the given token is an operator.
    """
    return token.type == TokenType.MUL or token.type == TokenType.DIV

def rpn_transform(tokens):
    """
    Transforms the given list of tokens into reverse polish notation using the
    shunting-yard algorithm. Linear complexity O(n).
    """
    # output queue
    output = deque()
    # operators stack
    operators = []
    for token in tokens:
        if token.type == TokenType.UNIT:
            output.append(token)
        elif is_operator(token):
            while len(operators) and operators[-1].type != TokenType.LPAREN:
                output.append(operators.pop())
            operators.append(token)
        elif token.type == TokenType.LPAREN:
            operators.append(token)
        elif token.type == TokenType.RPAREN:
            while len(operators) and operators[-1].type != TokenType.LPAREN:
                output.append(operators.pop())
            if not len(operators):
                # no matching LPAREN found, syntax error
                raise ValueError("Syntax error: Parenthesis mismatch")
            operators.pop()
    while len(operators) > 0:
        output.append(operators.pop())

    return [token for token in output]

def coefficient(rpn_tokens):
    """
    Returns the multiplication factor of the units by applying all unit
    operations on the given rpn_tokens.
    """
    values = []
    for token in rpn_tokens:
        if token.type == TokenType.UNIT:
            values.append(token.coefficient)
        elif token.type == TokenType.MUL:
            if len(values) < 2:
                raise ValueError("Not enough operands to satisfy operation")
            values.append(values.pop() * values.pop())
        elif token.type == TokenType.DIV:
            if len(values) < 2:
                raise ValueError("Not enough operands to satisfy operation")
            right, left = values.pop(), values.pop()
            values.append(left / right)
    return values.pop()
