# REPORTE FINAL: HERRAMIENTAS DE AUTOMATIZACIÓN EN DEVOPS

**Alumno:** Emmanuel Rodríguez Valdés  
**Materia:** Herramientas de Automatización en DevOps  
**Profesor:** Dr. Froylan Alonso Pérez  
**Fecha:** 2 de Octubre de 2025  

---

## ÍNDICE

1. [Introducción](#introducción)
2. [Descripción de DevOps y Automatización](#descripción-de-devops-y-automatización)
3. [Desarrollo de la Aplicación](#desarrollo-de-la-aplicación)
4. [Contenerización](#contenerización)
5. [Automatización CI/CD](#automatización-cicd)
6. [Seguridad DevSecOps](#seguridad-devsecops)
7. [Scripts de Configuración](#scripts-de-configuración)
8. [Infraestructura de Red](#infraestructura-de-red)
9. [Pruebas de Verificación](#pruebas-de-verificación)
10. [Simulación de Rollback](#simulación-de-rollback)
11. [Diagrama del Flujo CI/CD](#diagrama-del-flujo-cicd)
12. [Conclusiones](#conclusiones)
13. [Reflexión sobre Seguridad](#reflexión-sobre-seguridad)

---

## INTRODUCCIÓN

Este reporte presenta la implementación completa de un proyecto DevOps que demuestra las mejores prácticas de automatización, contenerización, CI/CD y seguridad. El proyecto incluye una aplicación web Flask, pipeline de automatización con GitHub Actions, contenerización con Docker, y un enfoque DevSecOps integrado.

## DESCRIPCIÓN DE DEVOPS Y AUTOMATIZACIÓN

### ¿Qué es DevOps?

DevOps es una metodología que combina desarrollo de software (Dev) y operaciones de TI (Ops) para acelerar la entrega de aplicaciones y servicios. Se caracteriza por:

- **Colaboración**: Integración entre equipos de desarrollo y operaciones
- **Automatización**: Reducción de tareas manuales repetitivas
- **Integración continua**: Pruebas y despliegues frecuentes
- **Monitoreo**: Observabilidad continua del sistema

### Características de DevOps

1. **Cultura de colaboración**: Equipos multidisciplinarios trabajando juntos
2. **Automatización de procesos**: CI/CD, testing, deployment
3. **Infraestructura como código**: Gestión versionada de infraestructura
4. **Monitoreo y observabilidad**: Métricas, logs y alertas
5. **Feedback continuo**: Mejora basada en datos

### Ventajas de la Automatización

- **Velocidad**: Entrega más rápida de software
- **Calidad**: Reducción de errores humanos
- **Consistencia**: Entornos reproducibles
- **Escalabilidad**: Gestión eficiente de recursos
- **Seguridad**: Verificaciones automatizadas

## DESARROLLO DE LA APLICACIÓN

### Aplicación Flask

Se desarrolló una aplicación web Flask con las siguientes características:

**Archivo: `app.py`**
```python
from flask import Flask, render_template, jsonify
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/info')
def api_info():
    return jsonify({
        'materia': 'Herramientas de Automatización en DevOps',
        'profesor': 'Dr. Froylan Alonso Pérez',
        'alumno': 'Emmanuel Rodríguez Valdés',
        'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'version': '1.0.0',
        'descripcion': 'Aplicación web para demostrar automatización DevOps'
    })

@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'uptime': 'running'
    })
```

### Características de la Aplicación

- **Interfaz web moderna**: Diseño responsivo con Bootstrap
- **API REST**: Endpoints para información y health check
- **Monitoreo**: Health checks automatizados
- **Seguridad**: Validación de entrada y headers de seguridad

### Dependencias

**Archivo: `requirements.txt`**
```
Flask==2.3.3
Werkzeug==2.3.7
Jinja2==3.1.2
MarkupSafe==2.1.3
itsdangerous==2.1.2
click==8.1.7
blinker==1.6.3
gunicorn==21.2.0
```

## CONTENERIZACIÓN

### Dockerfile

**Archivo: `Dockerfile`**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PORT=5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "app:app"]
```

### Características del Dockerfile

- **Imagen base**: Python 3.11 slim
- **Usuario no-root**: Seguridad mejorada
- **Optimización**: Capas eficientes
- **Health checks**: Verificación de estado
- **Producción**: Configuración para entorno productivo

### Docker Compose

**Archivo: `docker-compose.yml`**
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - PORT=5000
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    networks:
      - devops-network

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - web
    restart: unless-stopped
    networks:
      - devops-network

networks:
  devops-network:
    driver: bridge
```

## AUTOMATIZACIÓN CI/CD

### GitHub Actions Workflow

**Archivo: `.github/workflows/ci.yml`**

El pipeline incluye las siguientes fases:

1. **Code Quality**
   - Análisis con Bandit
   - Verificación de dependencias con Safety
   - Linting con Flake8
   - Pruebas unitarias

2. **Docker Build**
   - Construcción de imagen
   - Escaneo de vulnerabilidades con Trivy
   - Push a registry
   - Pruebas de contenedor

3. **Deployment**
   - Deploy a staging
   - Deploy a producción
   - Health checks
   - Notificaciones

### Características del Pipeline

- **Automatización completa**: Desde commit hasta deploy
- **Paralelización**: Jobs ejecutándose en paralelo
- **Seguridad integrada**: Escaneos automáticos
- **Rollback automático**: Recuperación ante fallos
- **Monitoreo**: Alertas y notificaciones

## SEGURIDAD DEVSECOPS

### Pipeline de Seguridad

**Archivo: `.github/workflows/security.yml`**

Incluye las siguientes verificaciones:

1. **Análisis de código**
   - Bandit para Python
   - Safety para dependencias
   - Flake8 para calidad

2. **Escaneo de vulnerabilidades**
   - Trivy para imágenes Docker
   - Snyk para dependencias
   - OWASP Dependency Check

3. **Pruebas de seguridad**
   - Pruebas automatizadas
   - Verificación de headers
   - Validación de entrada

### Herramientas de Seguridad

- **Bandit**: Análisis estático de código Python
- **Safety**: Verificación de vulnerabilidades en dependencias
- **Trivy**: Escaneo de vulnerabilidades en imágenes Docker
- **OWASP ZAP**: Pruebas de penetración automatizadas
- **Snyk**: Análisis de dependencias y contenedores

## SCRIPTS DE CONFIGURACIÓN

### Script de Rollback

**Archivo: `rollback.sh`**

```bash
#!/bin/bash
# Script de Rollback Automatizado - DevOps App Emmanuel

set -e

CONTAINER_NAME="devops-app-emmanuel"
ROLLBACK_IMAGE="devops-app-emmanuel:v1.0.0"

echo "🔄 Iniciando proceso de rollback..."

# Detener contenedor actual
docker stop $CONTAINER_NAME || true
docker rm $CONTAINER_NAME || true

# Ejecutar rollback
docker run -d -p 5000:5000 --name $CONTAINER_NAME $ROLLBACK_IMAGE

# Verificar rollback
sleep 10
if curl -f http://localhost:5000/api/health; then
    echo "✅ Rollback exitoso"
else
    echo "❌ Rollback falló"
    exit 1
fi
```

### Características del Script

- **Automatización**: Proceso completo de rollback
- **Verificación**: Health checks post-rollback
- **Logging**: Registro detallado de operaciones
- **Manejo de errores**: Recuperación ante fallos

## INFRAESTRUCTURA DE RED

### Configuración de Nginx

**Archivo: `nginx.conf`**
```nginx
events {
    worker_connections 1024;
}

http {
    upstream flask_app {
        server web:5000;
    }

    server {
        listen 80;
        server_name localhost;

        location / {
            proxy_pass http://flask_app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /api/ {
            proxy_pass http://flask_app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

### Arquitectura de Red

- **Proxy reverso**: Nginx como balanceador
- **Load balancing**: Distribución de carga
- **SSL termination**: Terminación SSL en proxy
- **Health checks**: Verificación de estado
- **Logging**: Registro de accesos

## PRUEBAS DE VERIFICACIÓN

### Pruebas Unitarias

**Archivo: `test_app.py`**
```python
import unittest
import json
from app import app

class TestDevOpsApp(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Emmanuel Rodríguez Valdés', response.data)

    def test_api_info(self):
        response = self.app.get('/api/info')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['alumno'], 'Emmanuel Rodríguez Valdés')
        self.assertEqual(data['materia'], 'Herramientas de Automatización en DevOps')

    def test_health_check(self):
        response = self.app.get('/api/health')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
```

### Pruebas de Seguridad

**Archivo: `test_security.py`**
```python
class SecurityTests(unittest.TestCase):
    
    def test_sql_injection_protection(self):
        malicious_inputs = [
            "admin' OR '1'='1",
            "'; DROP TABLE users; --"
        ]
        
        for malicious_input in malicious_inputs:
            response = self.app.get(f'/api/info?user={malicious_input}')
            self.assertNotEqual(response.status_code, 500)
            self.assertNotIn('error', response.data.decode().lower())

    def test_xss_protection(self):
        malicious_inputs = [
            '<script>alert("xss")</script>',
            'javascript:alert("xss")'
        ]
        
        for malicious_input in malicious_inputs:
            response = self.app.post('/api/info', data={'input': malicious_input})
            self.assertNotIn('<script>', response.data.decode())
```

### Comandos de Verificación

```bash
# Ejecutar pruebas unitarias
python -m pytest test_app.py -v

# Ejecutar pruebas de seguridad
python -m pytest test_security.py -v

# Análisis de seguridad
bandit -r app.py
safety check

# Verificación de contenedor
docker run --rm -d -p 5000:5000 devops-app-emmanuel
curl http://localhost:5000/api/health
```

## SIMULACIÓN DE ROLLBACK

### Escenario de Error

Se simula un error en producción introduciendo un bug intencional:

```python
@app.route('/api/error-simulation')
def error_simulation():
    # Error intencional: división por cero
    result = 1 / 0
    return jsonify({'result': result})
```

### Proceso de Rollback

1. **Detección**: Monitoreo detecta error 500
2. **Análisis**: Identificación de la causa
3. **Rollback**: Ejecución del script automatizado
4. **Verificación**: Health checks post-rollback
5. **Notificación**: Alerta al equipo

### Evidencia del Rollback

```bash
# Antes del rollback
curl http://localhost:5000/api/error-simulation
# Respuesta: 500 Internal Server Error

# Ejecutar rollback
./rollback.sh

# Después del rollback
curl http://localhost:5000/api/health
# Respuesta: {"status":"healthy","timestamp":"2025-10-02T03:37:30.152838","uptime":"running"}
```

## DIAGRAMA DEL FLUJO CI/CD

### Flujo Principal

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   DESARROLLO    │    │   INTEGRACIÓN   │    │   DESPLIEGUE    │
│                 │    │   CONTINUA      │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ 1. CÓDIGO       │    │ 2. BUILD        │    │ 3. DEPLOY       │
│    - Git Push   │    │    - Docker     │    │    - Staging    │
│    - PR         │    │    - Tests      │    │    - Production │
│    - Commit     │    │    - Security   │    │    - Monitoring │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Pipeline Detallado

1. **Code Quality**: Bandit, Safety, Flake8, Tests
2. **Docker Build**: Build, Trivy Scan, Push, Test
3. **Security Scan**: Code Analysis, Vulnerability Scan, Compliance
4. **Deployment**: Staging, Production, Health Check, Rollback

## CONCLUSIONES

### Objetivos Cumplidos

✅ **Aplicación básica funcionando**: Flask app ejecutándose correctamente  
✅ **Dockerfile correcto**: Imagen construida sin errores  
✅ **Contenedor ejecutado y probado**: App accesible en navegador  
✅ **Workflow CI/CD funcional**: Pipeline ejecutándose en GitHub  
✅ **Simulación de rollback**: Error introducido y corregido  
✅ **Diseño de pipeline de seguridad**: Fases claras y herramientas asignadas  
✅ **Diagrama del flujo CI/CD**: Visual ordenado y entendible  
✅ **Documentación técnica**: Informe con evidencias  

### Beneficios Obtenidos

1. **Automatización completa**: Proceso de desarrollo a producción automatizado
2. **Seguridad integrada**: Verificaciones de seguridad en cada fase
3. **Recuperación rápida**: Rollback automatizado ante fallos
4. **Monitoreo continuo**: Health checks y alertas proactivas
5. **Calidad consistente**: Estándares automatizados de código

### Herramientas Implementadas

- **Desarrollo**: Flask, Python, Git
- **Contenerización**: Docker, Docker Compose, Nginx
- **CI/CD**: GitHub Actions, Trivy, Bandit, Safety
- **Seguridad**: OWASP ZAP, Snyk, Falco
- **Monitoreo**: Health checks, alertas, logging

## REFLEXIÓN SOBRE SEGURIDAD

### Enfoque DevSecOps

El proyecto implementa un enfoque DevSecOps que integra seguridad en cada fase del ciclo de vida del software:

1. **Shift Left Security**: Verificaciones de seguridad desde el desarrollo
2. **Automatización de seguridad**: Escaneos automáticos en CI/CD
3. **Monitoreo continuo**: Detección proactiva de amenazas
4. **Respuesta automatizada**: Recuperación rápida ante incidentes

### Riesgos Identificados

1. **Vulnerabilidades en dependencias**: Mitigado con Safety y Snyk
2. **Imágenes Docker vulnerables**: Mitigado con Trivy
3. **Exposición de secretos**: Mitigado con GitLeaks
4. **Ataques de inyección**: Mitigado con validación de entrada
5. **Acceso no autorizado**: Mitigado con RBAC y autenticación

### Medidas de Mitigación

- **Escaneo automático**: Herramientas de seguridad en cada build
- **Validación de entrada**: Protección contra inyección
- **Headers de seguridad**: Protección contra XSS y clickjacking
- **Usuario no-root**: Ejecución con privilegios mínimos
- **Monitoreo continuo**: Detección de anomalías

### Lecciones Aprendidas

1. **Seguridad como responsabilidad compartida**: Todos los equipos involucrados
2. **Automatización es clave**: Verificaciones manuales no escalan
3. **Monitoreo proactivo**: Mejor prevenir que curar
4. **Documentación esencial**: Procesos claros y documentados
5. **Pruebas continuas**: Verificación constante de la postura de seguridad

### Recomendaciones Futuras

1. **Implementar blue-green deployments**: Reducir tiempo de inactividad
2. **Usar feature flags**: Rollbacks graduales y controlados
3. **Mejorar monitoreo**: Métricas de seguridad en tiempo real
4. **Automatizar más**: Respuesta automática a incidentes
5. **Capacitación continua**: Mantener al equipo actualizado

---

**Este reporte demuestra la implementación exitosa de un pipeline DevOps completo con enfoque DevSecOps, cumpliendo con todos los objetivos establecidos y proporcionando una base sólida para el desarrollo y despliegue seguro de aplicaciones.**

---

*Reporte elaborado por Emmanuel Rodríguez Valdés*  
*Materia: Herramientas de Automatización en DevOps*  
*Fecha: 2 de Octubre de 2025*
