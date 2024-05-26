import unittest
from app.servidor import Server

server = Server(16081)

class TestServer(unittest.TestCase):
    def test_fecha(self):
        response = server.generate_response('FECHA')
        self.assertRegex(response, r'\d{4}-\d{2}-\d{2}')

    
    def test_hora(self):
        response = server.generate_response('HORA')
        self.assertRegex(response, r'\d{2}:\d{2}:\d{2}')

    def test_error(self):
        response = server.generate_response('ANY_OTHER_MESSAGE')
        self.assertEqual(response, 'ERROR')


    
if __name__ == '__main__':
    unittest.main()
