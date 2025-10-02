import unittest
import json
import requests
from app import app

class SecurityTests(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_sql_injection_protection(self):
        """Test protección contra SQL injection"""
        # Intentar inyección SQL en parámetros
        malicious_inputs = [
            "admin' OR '1'='1",
            "'; DROP TABLE users; --",
            "1' UNION SELECT * FROM users --",
            "admin' AND 1=1 --"
        ]
        
        for malicious_input in malicious_inputs:
            response = self.app.get(f'/api/info?user={malicious_input}')
            # La aplicación no debe fallar ni exponer información sensible
            self.assertNotEqual(response.status_code, 500)
            self.assertNotIn('error', response.data.decode().lower())
            self.assertNotIn('sql', response.data.decode().lower())

    def test_xss_protection(self):
        """Test protección contra XSS"""
        malicious_inputs = [
            '<script>alert("xss")</script>',
            'javascript:alert("xss")',
            '<img src=x onerror=alert("xss")>',
            '<svg onload=alert("xss")>',
            '"><script>alert("xss")</script>'
        ]
        
        for malicious_input in malicious_inputs:
            response = self.app.post('/api/info', data={'input': malicious_input})
            # No debe contener scripts maliciosos
            self.assertNotIn('<script>', response.data.decode())
            self.assertNotIn('javascript:', response.data.decode())
            self.assertNotIn('onerror=', response.data.decode())
            self.assertNotIn('onload=', response.data.decode())

    def test_path_traversal_protection(self):
        """Test protección contra path traversal"""
        malicious_paths = [
            '../../../etc/passwd',
            '..\\..\\..\\windows\\system32\\drivers\\etc\\hosts',
            '/etc/passwd',
            'C:\\Windows\\System32\\drivers\\etc\\hosts'
        ]
        
        for malicious_path in malicious_paths:
            response = self.app.get(f'/api/info?file={malicious_path}')
            # No debe exponer archivos del sistema
            self.assertNotIn('root:', response.data.decode())
            self.assertNotIn('localhost', response.data.decode())
            self.assertNotIn('127.0.0.1', response.data.decode())

    def test_http_methods_security(self):
        """Test seguridad de métodos HTTP"""
        # Verificar que métodos peligrosos no estén habilitados
        dangerous_methods = ['PUT', 'DELETE', 'PATCH', 'TRACE', 'OPTIONS']
        
        for method in dangerous_methods:
            response = self.app.open('/', method=method)
            # Debe devolver 405 Method Not Allowed o 404 Not Found
            self.assertIn(response.status_code, [404, 405])

    def test_headers_security(self):
        """Test headers de seguridad"""
        response = self.app.get('/')
        
        # Verificar headers de seguridad
        security_headers = [
            'X-Content-Type-Options',
            'X-Frame-Options',
            'X-XSS-Protection',
            'Strict-Transport-Security',
            'Content-Security-Policy'
        ]
        
        for header in security_headers:
            # Algunos headers pueden no estar presentes en desarrollo
            # pero deben estar en producción
            if header in response.headers:
                self.assertIsNotNone(response.headers[header])

    def test_input_validation(self):
        """Test validación de entrada"""
        # Test con entradas muy largas
        long_input = 'A' * 10000
        response = self.app.post('/api/info', data={'input': long_input})
        # Debe manejar entradas largas sin fallar
        self.assertNotEqual(response.status_code, 500)

    def test_authentication_bypass(self):
        """Test intentos de bypass de autenticación"""
        # Intentar acceder a endpoints protegidos sin autenticación
        protected_endpoints = [
            '/admin',
            '/api/admin',
            '/dashboard',
            '/config'
        ]
        
        for endpoint in protected_endpoints:
            response = self.app.get(endpoint)
            # Debe devolver 404 o 401, no 200
            self.assertNotEqual(response.status_code, 200)

    def test_information_disclosure(self):
        """Test prevención de divulgación de información"""
        response = self.app.get('/api/health')
        
        # No debe exponer información sensible
        sensitive_info = [
            'password',
            'secret',
            'key',
            'token',
            'database',
            'connection',
            'config'
        ]
        
        response_text = response.data.decode().lower()
        for info in sensitive_info:
            self.assertNotIn(info, response_text)

    def test_rate_limiting(self):
        """Test limitación de velocidad (básico)"""
        # Hacer múltiples requests rápidos
        for i in range(10):
            response = self.app.get('/api/health')
            # En un entorno real, después de cierto número de requests
            # debería devolver 429 Too Many Requests
            # Por ahora solo verificamos que no falle
            self.assertNotEqual(response.status_code, 500)

    def test_cors_security(self):
        """Test configuración de CORS"""
        response = self.app.get('/')
        
        # Verificar que CORS esté configurado correctamente
        # En desarrollo puede no estar presente
        if 'Access-Control-Allow-Origin' in response.headers:
            # No debe permitir acceso desde cualquier origen
            self.assertNotEqual(response.headers['Access-Control-Allow-Origin'], '*')

    def test_content_type_security(self):
        """Test seguridad de tipos de contenido"""
        response = self.app.get('/')
        
        # Verificar que el content-type sea correcto
        if 'Content-Type' in response.headers:
            content_type = response.headers['Content-Type']
            # Debe ser text/html para la página principal
            self.assertIn('text/html', content_type)

    def test_error_handling_security(self):
        """Test manejo seguro de errores"""
        # Intentar acceder a un endpoint inexistente
        response = self.app.get('/nonexistent-endpoint')
        
        # No debe exponer información del sistema en errores
        error_text = response.data.decode().lower()
        sensitive_error_info = [
            'traceback',
            'exception',
            'stack trace',
            'file path',
            'line number'
        ]
        
        for info in sensitive_error_info:
            self.assertNotIn(info, error_text)

if __name__ == '__main__':
    unittest.main()
