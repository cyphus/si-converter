#!/usr/bin/env python3
from collections import deque
from .tokenizer import (Token, TokenType)

def is_operator(token):
    return token.type == TokenType.MUL or token.type == TokenType.DIV

def parse(tokens):
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
