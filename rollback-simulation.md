# Simulación de Rollback - DevOps App Emmanuel

## Escenario de Error Simulado

### 1. Error Introducido Intencionalmente

Se introduce un error en el código para simular un fallo en producción:

```python
# Error simulado en app.py - línea problemática
@app.route('/api/error-simulation')
def error_simulation():
    # Error intencional: división por cero
    result = 1 / 0
    return jsonify({'result': result})
```

### 2. Proceso de Rollback

#### Paso 1: Detección del Error
- Monitoreo detecta error 500 en `/api/error-simulation`
- Alertas automáticas se activan
- Equipo de desarrollo es notificado

#### Paso 2: Análisis del Error
```bash
# Verificar logs del contenedor
docker logs devops-app-emmanuel

# Verificar estado del contenedor
docker ps -a

# Verificar health check
curl http://localhost:5000/api/health
```

#### Paso 3: Rollback Manual
```bash
# 1. Detener contenedor actual
docker stop devops-app-emmanuel

# 2. Eliminar contenedor problemático
docker rm devops-app-emmanuel

# 3. Rollback a versión anterior (tag específico)
docker run -d -p 5000:5000 --name devops-app-emmanuel devops-app-emmanuel:v1.0.0

# 4. Verificar que el rollback fue exitoso
curl http://localhost:5000/api/health
```

#### Paso 4: Rollback Automatizado con Docker Compose
```yaml
# docker-compose.rollback.yml
version: '3.8'
services:
  web:
    image: devops-app-emmanuel:v1.0.0  # Versión anterior estable
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - PORT=5000
    restart: unless-stopped
```

```bash
# Ejecutar rollback con docker-compose
docker-compose -f docker-compose.rollback.yml up -d

# Verificar estado
docker-compose -f docker-compose.rollback.yml ps
```

### 3. Script de Rollback Automatizado

```bash
#!/bin/bash
# rollback.sh

set -e

echo "🔄 Iniciando proceso de rollback..."

# Variables
CONTAINER_NAME="devops-app-emmanuel"
BACKUP_IMAGE="devops-app-emmanuel:backup"
CURRENT_IMAGE="devops-app-emmanuel:latest"

# 1. Crear backup de la imagen actual
echo "📦 Creando backup de la imagen actual..."
docker tag $CURRENT_IMAGE $BACKUP_IMAGE

# 2. Detener y eliminar contenedor actual
echo "🛑 Deteniendo contenedor actual..."
docker stop $CONTAINER_NAME || true
docker rm $CONTAINER_NAME || true

# 3. Rollback a versión anterior
echo "⏪ Ejecutando rollback..."
docker run -d -p 5000:5000 --name $CONTAINER_NAME devops-app-emmanuel:v1.0.0

# 4. Verificar rollback
echo "✅ Verificando rollback..."
sleep 10
if curl -f http://localhost:5000/api/health; then
    echo "✅ Rollback exitoso - Aplicación funcionando"
else
    echo "❌ Rollback falló - Revisar logs"
    docker logs $CONTAINER_NAME
    exit 1
fi

echo "🎉 Rollback completado exitosamente"
```

### 4. Rollback con GitHub Actions

```yaml
# .github/workflows/rollback.yml
name: Rollback Production

on:
  workflow_dispatch:
    inputs:
      version:
        description: 'Versión a la cual hacer rollback'
        required: true
        default: 'v1.0.0'

jobs:
  rollback:
    runs-on: ubuntu-latest
    environment: production
    steps:
    - name: Rollback to version ${{ github.event.inputs.version }}
      run: |
        echo "🔄 Rolling back to version ${{ github.event.inputs.version }}"
        # Comandos de rollback específicos del entorno
        # kubectl rollout undo deployment/devops-app
        # o
        # docker service update --image devops-app-emmanuel:${{ github.event.inputs.version }} devops-app
```

### 5. Monitoreo Post-Rollback

```bash
# Verificar métricas después del rollback
curl http://localhost:5000/api/health
curl http://localhost:5000/api/info

# Monitorear logs
docker logs -f devops-app-emmanuel

# Verificar rendimiento
ab -n 100 -c 10 http://localhost:5000/
```

### 6. Lecciones Aprendidas

1. **Backup Automático**: Siempre mantener backups de versiones estables
2. **Monitoreo Continuo**: Implementar alertas automáticas
3. **Rollback Rápido**: Tener procesos de rollback automatizados
4. **Comunicación**: Notificar a stakeholders sobre el rollback
5. **Post-Mortem**: Analizar la causa raíz del error

### 7. Mejoras para el Futuro

- Implementar blue-green deployments
- Usar feature flags para rollbacks graduales
- Automatizar más el proceso de rollback
- Mejorar el monitoreo y alertas
- Implementar circuit breakers
