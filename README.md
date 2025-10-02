# DevOps App - Emmanuel Rodríguez Valdés

## Descripción del Proyecto

Este proyecto implementa una aplicación web Flask con un pipeline completo de DevOps y DevSecOps, incluyendo automatización CI/CD, contenerización con Docker, y prácticas de seguridad integradas.

## Información del Proyecto

- **Materia**: Herramientas de Automatización en DevOps
- **Profesor**: Dr. Froylan Alonso Pérez
- **Alumno**: Emmanuel Rodríguez Valdés
- **Versión**: 1.0.0
- **Fecha**: 2025-10-02

## Características

### Aplicación Web
- Framework Flask con diseño moderno
- API REST con endpoints de información y health check
- Interfaz web responsiva con Bootstrap
- Endpoints de seguridad y monitoreo

### Contenerización
- Dockerfile optimizado para producción
- Docker Compose para orquestación local
- Nginx como proxy reverso
- Health checks automatizados

### CI/CD Pipeline
- GitHub Actions para automatización
- Análisis de código con Bandit, Safety, Flake8
- Escaneo de vulnerabilidades con Trivy
- Despliegue automatizado a staging y producción

### Seguridad (DevSecOps)
- Pipeline de seguridad integrado
- Pruebas de seguridad automatizadas
- Escaneo de dependencias y secretos
- Monitoreo de vulnerabilidades

## Estructura del Proyecto

```
proyecto-final-emmanuel/
├── app.py                          # Aplicación Flask principal
├── requirements.txt                # Dependencias de Python
├── Dockerfile                      # Configuración de Docker
├── docker-compose.yml              # Orquestación con Docker Compose
├── nginx.conf                      # Configuración de Nginx
├── test_app.py                     # Pruebas unitarias
├── test_security.py                # Pruebas de seguridad
├── rollback.sh                     # Script de rollback automatizado
├── .github/
│   └── workflows/
│       ├── ci.yml                  # Pipeline CI/CD principal
│       └── security.yml            # Pipeline de seguridad
├── templates/
│   └── index.html                  # Plantilla HTML principal
├── devsecops-pipeline.md           # Documentación del pipeline DevSecOps
├── rollback-simulation.md          # Simulación de rollback
├── cicd-diagram.md                 # Diagrama del flujo CI/CD
└── README.md                       # Este archivo
```

## Instalación y Uso

### Prerrequisitos
- Python 3.11+
- Docker y Docker Compose
- Git

### Instalación Local

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd proyecto-final-emmanuel
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Ejecutar la aplicación**
```bash
python app.py
```

4. **Acceder a la aplicación**
- URL: http://localhost:5000
- API: http://localhost:5000/api/info
- Health Check: http://localhost:5000/api/health

### Instalación con Docker

1. **Construir la imagen**
```bash
docker build -t devops-app-emmanuel .
```

2. **Ejecutar el contenedor**
```bash
docker run -d -p 5000:5000 --name devops-app-emmanuel devops-app-emmanuel
```

3. **Usar Docker Compose**
```bash
docker-compose up -d
```

## API Endpoints

### Información de la Aplicación
```http
GET /api/info
```
Respuesta:
```json
{
  "materia": "Herramientas de Automatización en DevOps",
  "profesor": "Dr. Froylan Alonso Pérez",
  "alumno": "Emmanuel Rodríguez Valdés",
  "fecha": "2025-10-02 03:37:30",
  "version": "1.0.0",
  "descripcion": "Aplicación web para demostrar automatización DevOps"
}
```

### Health Check
```http
GET /api/health
```
Respuesta:
```json
{
  "status": "healthy",
  "timestamp": "2025-10-02T03:37:30.152838",
  "uptime": "running"
}
```

### Herramientas DevOps
```http
GET /api/devops-tools
```
Respuesta:
```json
{
  "tools": [
    {
      "name": "Docker",
      "description": "Plataforma de contenedores para desarrollo y despliegue",
      "category": "Contenerización"
    },
    {
      "name": "GitHub Actions",
      "description": "Automatización de CI/CD integrada con GitHub",
      "category": "CI/CD"
    }
  ]
}
```

## Pipeline CI/CD

### Fases del Pipeline

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

3. **Security Scan**
   - Análisis de seguridad del código
   - Escaneo de vulnerabilidades
   - Verificación de secretos
   - Pruebas de seguridad

4. **Deployment**
   - Deploy a staging
   - Deploy a producción
   - Health checks
   - Monitoreo

### Workflows

- **ci.yml**: Pipeline principal de CI/CD
- **security.yml**: Pipeline de seguridad DevSecOps

## Seguridad (DevSecOps)

### Herramientas de Seguridad
- **Bandit**: Análisis estático de código Python
- **Safety**: Verificación de vulnerabilidades en dependencias
- **Trivy**: Escaneo de vulnerabilidades en imágenes Docker
- **OWASP ZAP**: Pruebas de penetración automatizadas
- **Snyk**: Análisis de dependencias y contenedores

### Pruebas de Seguridad
- Protección contra SQL injection
- Protección contra XSS
- Validación de entrada
- Headers de seguridad
- Manejo seguro de errores

## Rollback y Recuperación

### Script de Rollback
```bash
./rollback.sh
```

### Proceso de Rollback
1. Detección del error
2. Análisis del impacto
3. Ejecución del rollback
4. Verificación del estado
5. Notificación del equipo

## Monitoreo

### Health Checks
- Endpoint `/api/health` para verificación de estado
- Monitoreo de contenedores con Docker
- Alertas automáticas en caso de fallos

### Métricas
- Tiempo de respuesta
- Disponibilidad
- Errores por minuto
- Uso de recursos

## Desarrollo

### Ejecutar Pruebas
```bash
# Pruebas unitarias
python -m pytest test_app.py -v

# Pruebas de seguridad
python -m pytest test_security.py -v

# Todas las pruebas
python -m pytest -v
```

### Análisis de Código
```bash
# Bandit (seguridad)
bandit -r app.py

# Safety (dependencias)
safety check

# Flake8 (calidad)
flake8 app.py
```

## Contribución

1. Fork el proyecto
2. Crear una rama para la feature (`git checkout -b feature/nueva-feature`)
3. Commit los cambios (`git commit -am 'Agregar nueva feature'`)
4. Push a la rama (`git push origin feature/nueva-feature`)
5. Crear un Pull Request

## Licencia

Este proyecto es parte de un trabajo académico para la materia "Herramientas de Automatización en DevOps".

## Contacto

- **Alumno**: Emmanuel Rodríguez Valdés
- **Materia**: Herramientas de Automatización en DevOps
- **Fecha**: 2025-10-02

## Agradecimientos

- Dr. Froylan Alonso Pérez por la guía y enseñanza
- Comunidad de DevOps por las mejores prácticas
- Herramientas open source utilizadas en el proyecto
