import unittest
import json
from app import app

class TestDevOpsApp(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index_page(self):
        """Test que la página principal carga correctamente"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Emmanuel Rodríguez Valdés', response.data)

    def test_api_info(self):
        """Test del endpoint de información"""
        response = self.app.get('/api/info')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['alumno'], 'Emmanuel Rodríguez Valdés')
        self.assertEqual(data['materia'], 'Herramientas de Automatización en DevOps')
        self.assertIn('version', data)
        self.assertIn('fecha', data)

    def test_health_check(self):
        """Test del endpoint de health check"""
        response = self.app.get('/api/health')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('timestamp', data)
        self.assertEqual(data['uptime'], 'running')

    def test_devops_tools(self):
        """Test del endpoint de herramientas DevOps"""
        response = self.app.get('/api/devops-tools')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('tools', data)
        self.assertGreater(len(data['tools']), 0)
        
        # Verificar que contiene herramientas esperadas
        tool_names = [tool['name'] for tool in data['tools']]
        self.assertIn('Docker', tool_names)
        self.assertIn('GitHub Actions', tool_names)

if __name__ == '__main__':
    unittest.main()
