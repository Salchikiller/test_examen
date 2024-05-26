import unittest
from app.servidor import Server

server = Server(16081)

class TestServer(unittest.TestCase):
    def test_fecha(self):
        # Forzamos el fallo de la prueba
        response = server.generate_response('FECHA')
        self.assertNotRegex(response, r'\d{4}-\d{2}-\d{2}')
    
if __name__ == '__main__':
    unittest.main()
