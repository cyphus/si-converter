#!/usr/bin/env python3
from collections import deque
from .tokenizer import (Token, TokenType)

def is_operator(token):
    return token.type == TokenType.MUL or token.type == TokenType.DIV

def parse(tokens):
    """
    Returns an AST from a given list of tokens using the shunting-yard
    algorithm.
    """
    output = deque()
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
