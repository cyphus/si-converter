import unittest
 
from units.app import app
 
 
class BasicTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
 
    def tearDown(self):
        pass
 
    def test_no_units(self):
        response = self.app.get('/units/si')
        self.assertEqual(response.status_code, 400)
 
    def test_simple_unit(self):
        response = self.app.get('/units/si?units=degree')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'{"multiplication_factor":0.017453292519943295,"unit_name":"rad"}\n')
 
    def test_multiple_untis(self):
        response = self.app.get('/units/si?units=(degree/(minute*hectare))')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'{"multiplication_factor":2.908882086657216e-08,"unit_name":"(rad/(s*m2))"}\n')

    def test_invalid_char(self):
        response = self.app.get('/units/si?units=^')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'{"error":"unrecognized token at pos 0 of \'^\'"}\n')

    def test_mismatched_parens(self):
        response = self.app.get('/units/si?units=(()))')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'{"error":"Syntax error: Parenthesis mismatch"}\n')

if __name__ == "__main__":
    unittest.main()
