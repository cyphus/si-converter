import unittest
from ..tokenizer import *

class TestTokenizer(unittest.TestCase):
    def test_tokenize_empty_string(self):
        self.assertEqual([], tokenize(''))

    def test_tokenize_invalid_string(self):
        with self.assertRaises(ValueError):
            tokenize('%')

    def test_tokenize_single_unit(self):
        self.assertEqual([Token(TokenType.UNIT, 's')], tokenize('s'))

    def test_tokenize_multiply(self):
        expected = [
            Token(TokenType.UNIT, 'minute'),
            Token(TokenType.MUL, '*'),
            Token(TokenType.UNIT, 'hectare'),
        ]
        self.assertEqual(expected, tokenize('minute*hectare'))

    def test_tokenize_divide(self):
        expected = [
            Token(TokenType.UNIT, 'minute'),
            Token(TokenType.DIV, '/'),
            Token(TokenType.UNIT, 'hectare'),
        ]
        self.assertEqual(expected, tokenize('minute/hectare'))

    def test_tokenize_paren(self):
        expected = [
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
        self.assertEqual(expected, tokenize('(degree/(minute*hectare))'))
