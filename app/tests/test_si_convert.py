import unittest
from ..si_convert import *

class TestRPNTransform(unittest.TestCase):
    def test_rpn_transform_empty_list(self):
        self.assertEqual([], rpn_transform([]))

    def test_rpn_transform_mismatched_parens(self):
        with self.assertRaises(ValueError):
            rpn_transform([Token(TokenType.RPAREN, ')')])

    def test_rpn_transform_multiply(self):
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
        self.assertEqual(expected, rpn_transform(tokens))

    def test_rpn_transform_divide(self):
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
        self.assertEqual(expected, rpn_transform(tokens))

    def test_rpn_transform_paren(self):
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
        self.assertEqual(expected, rpn_transform(tokens))


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
