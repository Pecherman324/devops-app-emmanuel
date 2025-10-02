# Pipeline de Seguridad DevSecOps - Emmanuel Rodríguez Valdés

## Descripción del Pipeline DevSecOps

El pipeline de seguridad DevSecOps integra prácticas de seguridad en cada fase del ciclo de vida del desarrollo, desde el código hasta el despliegue en producción.

## Fases del Pipeline y Herramientas de Seguridad

### 1. Fase de Desarrollo (Shift Left Security)

#### Herramientas Implementadas:
- **Bandit**: Análisis estático de código Python
- **Safety**: Verificación de vulnerabilidades en dependencias
- **Pre-commit Hooks**: Validaciones automáticas antes del commit

#### Configuración:
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 22.3.0
    hooks:
      - id: black
  - repo: https://github.com/pycqa/flake8
    rev: 4.0.1
    hooks:
      - id: flake8
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.0
    hooks:
      - id: bandit
        args: ['-r', '.', '-f', 'json', '-o', 'bandit-report.json']
```

### 2. Fase de Integración Continua (CI)

#### Herramientas de Seguridad:
- **SonarQube**: Análisis de calidad y seguridad del código
- **OWASP Dependency Check**: Escaneo de vulnerabilidades
- **Trivy**: Escaneo de vulnerabilidades en imágenes Docker
- **Snyk**: Análisis de dependencias y contenedores

#### Workflow de Seguridad:
```yaml
# .github/workflows/security.yml
name: Security Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Run Bandit Security Scan
      run: |
        pip install bandit
        bandit -r . -f json -o bandit-report.json
        bandit -r . -f txt
        
    - name: Run Safety Check
      run: |
        pip install safety
        safety check --json --output safety-report.json
        safety check
        
    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        image-ref: 'devops-app-emmanuel:latest'
        format: 'sarif'
        output: 'trivy-results.sarif'
        
    - name: Upload Trivy scan results
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: 'trivy-results.sarif'
```

### 3. Fase de Construcción (Build)

#### Herramientas de Seguridad:
- **Docker Bench Security**: Verificación de mejores prácticas
- **Hadolint**: Linting para Dockerfiles
- **Clair**: Análisis de vulnerabilidades en imágenes

#### Configuración:
```dockerfile
# Dockerfile con mejores prácticas de seguridad
FROM python:3.11-slim

# Crear usuario no-root
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Instalar dependencias de seguridad
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Configurar directorio de trabajo
WORKDIR /app

# Copiar e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY --chown=appuser:appuser . .

# Cambiar a usuario no-root
USER appuser

# Exponer puerto
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/api/health || exit 1

# Comando de inicio
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

### 4. Fase de Pruebas (Testing)

#### Herramientas de Seguridad:
- **OWASP ZAP**: Pruebas de penetración automatizadas
- **Nessus**: Escaneo de vulnerabilidades
- **Burp Suite**: Pruebas de seguridad de aplicaciones web

#### Configuración de Pruebas:
```python
# test_security.py
import unittest
import requests
from app import app

class SecurityTests(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_sql_injection_protection(self):
        """Test protección contra SQL injection"""
        response = self.app.get('/api/info?user=admin\' OR \'1\'=\'1')
        self.assertNotIn('error', response.data.decode().lower())
    
    def test_xss_protection(self):
        """Test protección contra XSS"""
        malicious_input = '<script>alert("xss")</script>'
        response = self.app.post('/api/info', data={'input': malicious_input})
        self.assertNotIn('<script>', response.data.decode())
    
    def test_https_headers(self):
        """Test headers de seguridad"""
        response = self.app.get('/')
        # Verificar headers de seguridad
        self.assertIn('X-Content-Type-Options', response.headers)
        self.assertIn('X-Frame-Options', response.headers)
```

### 5. Fase de Despliegue (Deployment)

#### Herramientas de Seguridad:
- **Vault**: Gestión de secretos
- **Kubernetes RBAC**: Control de acceso basado en roles
- **Network Policies**: Políticas de red para contenedores
- **Pod Security Standards**: Estándares de seguridad para pods

#### Configuración de Despliegue Seguro:
```yaml
# k8s-deployment-secure.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: devops-app-secure
spec:
  replicas: 3
  selector:
    matchLabels:
      app: devops-app
  template:
    metadata:
      labels:
        app: devops-app
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 2000
      containers:
      - name: devops-app
        image: devops-app-emmanuel:latest
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop:
            - ALL
        ports:
        - containerPort: 5000
        env:
        - name: FLASK_ENV
          value: "production"
        resources:
          requests:
            memory: "64Mi"
            cpu: "250m"
          limits:
            memory: "128Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /api/health
            port: 5000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /api/health
            port: 5000
          initialDelaySeconds: 5
          periodSeconds: 5
```

### 6. Fase de Monitoreo (Monitoring)

#### Herramientas de Seguridad:
- **Falco**: Detección de comportamiento anómalo
- **Sysdig**: Monitoreo de seguridad en tiempo real
- **ELK Stack**: Análisis de logs de seguridad
- **Prometheus + Grafana**: Métricas de seguridad

#### Configuración de Monitoreo:
```yaml
# falco-rules.yaml
- rule: Detect shell in container
  desc: Notice shell activity in container
  condition: >
    spawned_process and
    container and
    shell_procs and
    proc.tty != 0
  output: >
    Shell spawned in container (user=%user.name user_loginuid=%user.loginuid %container.info
    shell=%proc.name parent=%proc.pname cmdline=%proc.cmdline terminal=%proc.tty container_id=%container.id image=%container.image.repository)
  priority: WARNING
  tags: [container, shell]
```

## Riesgos Identificados y Medidas de Mitigación

### 1. Vulnerabilidades en Dependencias
**Riesgo**: Dependencias con vulnerabilidades conocidas
**Mitigación**: 
- Escaneo automático con Safety y Snyk
- Actualización automática de dependencias
- Políticas de aprobación para dependencias

### 2. Imágenes Docker Vulnerables
**Riesgo**: Imágenes base con vulnerabilidades
**Mitigación**:
- Escaneo con Trivy en cada build
- Uso de imágenes base mínimas
- Actualización regular de imágenes base

### 3. Exposición de Secretos
**Riesgo**: Credenciales expuestas en código
**Mitigación**:
- Uso de Vault para gestión de secretos
- Escaneo con GitLeaks
- Rotación automática de credenciales

### 4. Ataques de Inyección
**Riesgo**: SQL injection, XSS, etc.
**Mitigación**:
- Validación de entrada
- Escaneo con OWASP ZAP
- Pruebas de seguridad automatizadas

### 5. Acceso No Autorizado
**Riesgo**: Acceso no autorizado a recursos
**Mitigación**:
- Implementación de RBAC
- Autenticación multifactor
- Monitoreo de accesos

## Métricas de Seguridad

### KPIs de Seguridad:
- **Tiempo de detección**: < 5 minutos
- **Tiempo de respuesta**: < 30 minutos
- **Cobertura de pruebas de seguridad**: > 90%
- **Vulnerabilidades críticas**: 0
- **Vulnerabilidades de alto riesgo**: < 5

### Dashboard de Seguridad:
```yaml
# grafana-dashboard.yaml
dashboard:
  title: "DevSecOps Security Dashboard"
  panels:
    - title: "Vulnerability Trends"
      type: "graph"
      targets:
        - expr: "security_vulnerabilities_total"
    - title: "Security Test Coverage"
      type: "stat"
      targets:
        - expr: "security_test_coverage_percent"
    - title: "Failed Security Scans"
      type: "table"
      targets:
        - expr: "security_scan_failures"
```

## Automatización de Respuesta a Incidentes

### Playbook de Respuesta:
1. **Detección**: Alertas automáticas
2. **Análisis**: Clasificación de severidad
3. **Contención**: Aislamiento del sistema afectado
4. **Eradicación**: Eliminación de la amenaza
5. **Recuperación**: Restauración del servicio
6. **Lecciones aprendidas**: Documentación y mejora

### Scripts de Automatización:
```bash
#!/bin/bash
# incident-response.sh

# Detectar incidente de seguridad
if [ "$1" = "critical" ]; then
    echo "🚨 Incidente crítico detectado"
    # Aislar sistema
    kubectl scale deployment devops-app --replicas=0
    # Notificar equipo
    curl -X POST -H 'Content-type: application/json' \
        --data '{"text":"🚨 Incidente de seguridad crítico detectado"}' \
        $SLACK_WEBHOOK
fi
```

## Conclusión

El pipeline DevSecOps implementado proporciona:
- **Seguridad integrada** en cada fase del desarrollo
- **Detección temprana** de vulnerabilidades
- **Respuesta automatizada** a incidentes
- **Monitoreo continuo** de la postura de seguridad
- **Cumplimiento** con estándares de seguridad

Este enfoque garantiza que la seguridad sea una responsabilidad compartida entre desarrollo, operaciones y seguridad, resultando en aplicaciones más seguras y resilientes.
