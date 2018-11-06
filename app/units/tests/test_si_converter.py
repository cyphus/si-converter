import unittest
from ..tokenizer import (Token, TokenType)
from ..si_converter import *

class TestSIConverter(unittest.TestCase):
    def test_convert_empty_list(self):
        self.assertEqual([], si_convert([]))

    def test_convert_non_units(self):
        tokens = [
            Token(TokenType.LPAREN, '('),
            Token(TokenType.MUL, '*'),
            Token(TokenType.DIV, '/'),
            Token(TokenType.RPAREN, ')'),
        ]
        self.assertEqual(tokens, si_convert(tokens))

    def test_convert_units(self):
        tokens = [
            Token(TokenType.UNIT, 'minute'),
            Token(TokenType.MUL, '*'),
            Token(TokenType.UNIT, 'hectare'),
        ]
        expected = [
            Token(TokenType.UNIT, 's', 60),
            Token(TokenType.MUL, '*'),
            Token(TokenType.UNIT, 'm2', 10000),
        ]
        self.assertEqual(expected, si_convert(tokens))
