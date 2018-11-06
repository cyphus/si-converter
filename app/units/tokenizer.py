#!/usr/bin/env python3
from collections import namedtuple
from enum import Enum
import re

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
            err = "unrecognized token at pos {} of '{}s'".format(
                    char_index, unit_str)
            raise ValueError(err)

    return tokens
