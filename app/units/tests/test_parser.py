import unittest
from ..tokenizer import (Token, TokenType)
from ..parser import *

class TestParser(unittest.TestCase):
    def test_parse_empty_list(self):
        self.assertEqual([], parse([]))

    def test_parse_mismatched_parens(self):
        with self.assertRaises(ValueError):
            parse([Token(TokenType.RPAREN, ')')])

    def test_parse_multiply(self):
        tokens = [
            Token(TokenType.UNIT, 'minute'),
            Token(TokenType.MUL, '*'),
            Token(TokenType.UNIT, 'hectare'),
        ]
        expected = [
            Token(TokenType.UNIT, 'minute'),
            Token(TokenType.UNIT, 'hectare'),
            Token(TokenType.MUL, '*'),
        ]
        self.assertEqual(expected, parse(tokens))

    def test_parse_divide(self):
        tokens = [
            Token(TokenType.UNIT, 'minute'),
            Token(TokenType.DIV, '/'),
            Token(TokenType.UNIT, 'hectare'),
        ]
        expected = [
            Token(TokenType.UNIT, 'minute'),
            Token(TokenType.UNIT, 'hectare'),
            Token(TokenType.DIV, '/'),
        ]
        self.assertEqual(expected, parse(tokens))

    def test_parse_paren(self):
        tokens = [
            Token(TokenType.LPAREN, '('),
            Token(TokenType.UNIT, 'degree'),
            Token(TokenType.DIV, '/'),
            Token(TokenType.LPAREN, '('),
            Token(TokenType.UNIT, 'minute'),
            Token(TokenType.MUL, '*'),
            Token(TokenType.UNIT, 'hectare'),
            Token(TokenType.RPAREN, ')'),
            Token(TokenType.RPAREN, ')'),
        ]
        expected = [
            Token(TokenType.UNIT, 'degree'),
            Token(TokenType.UNIT, 'minute'),
            Token(TokenType.UNIT, 'hectare'),
            Token(TokenType.MUL, '*'),
            Token(TokenType.DIV, '/'),
        ]
        self.assertEqual(expected, parse(tokens))
