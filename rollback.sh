#!/bin/bash
# Script de Rollback Automatizado - DevOps App Emmanuel
# Autor: Emmanuel Rodríguez Valdés

set -e

echo "🔄 Iniciando proceso de rollback..."

# Variables
CONTAINER_NAME="devops-app-emmanuel"
BACKUP_IMAGE="devops-app-emmanuel:backup"
CURRENT_IMAGE="devops-app-emmanuel:latest"
ROLLBACK_IMAGE="devops-app-emmanuel:v1.0.0"

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para logging
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Función para verificar si un comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Verificar dependencias
check_dependencies() {
    log "Verificando dependencias..."
    
    if ! command_exists docker; then
        error "Docker no está instalado"
        exit 1
    fi
    
    if ! command_exists curl; then
        error "curl no está instalado"
        exit 1
    fi
    
    success "Dependencias verificadas"
}

# Función para verificar salud de la aplicación
check_health() {
    local url=$1
    local max_attempts=5
    local attempt=1
    
    log "Verificando salud de la aplicación en $url..."
    
    while [ $attempt -le $max_attempts ]; do
        if curl -f -s "$url" > /dev/null 2>&1; then
            success "Aplicación saludable en $url"
            return 0
        fi
        
        warning "Intento $attempt/$max_attempts falló, esperando 5 segundos..."
        sleep 5
        ((attempt++))
    done
    
    error "La aplicación no responde después de $max_attempts intentos"
    return 1
}

# Función para crear backup
create_backup() {
    log "Creando backup de la imagen actual..."
    
    if docker images | grep -q "$CURRENT_IMAGE"; then
        docker tag "$CURRENT_IMAGE" "$BACKUP_IMAGE"
        success "Backup creado: $BACKUP_IMAGE"
    else
        warning "Imagen actual no encontrada, continuando sin backup"
    fi
}

# Función para detener contenedor actual
stop_current_container() {
    log "Deteniendo contenedor actual..."
    
    if docker ps -q -f name="$CONTAINER_NAME" | grep -q .; then
        docker stop "$CONTAINER_NAME"
        success "Contenedor detenido"
    else
        warning "Contenedor no está ejecutándose"
    fi
    
    if docker ps -aq -f name="$CONTAINER_NAME" | grep -q .; then
        docker rm "$CONTAINER_NAME"
        success "Contenedor eliminado"
    fi
}

# Función para ejecutar rollback
execute_rollback() {
    log "Ejecutando rollback a versión anterior..."
    
    if ! docker images | grep -q "$ROLLBACK_IMAGE"; then
        error "Imagen de rollback no encontrada: $ROLLBACK_IMAGE"
        error "Imágenes disponibles:"
        docker images | grep devops-app-emmanuel
        exit 1
    fi
    
    docker run -d \
        --name "$CONTAINER_NAME" \
        -p 5000:5000 \
        --restart unless-stopped \
        "$ROLLBACK_IMAGE"
    
    success "Contenedor de rollback iniciado"
}

# Función para verificar rollback
verify_rollback() {
    log "Verificando rollback..."
    
    # Esperar a que el contenedor esté listo
    sleep 10
    
    # Verificar que el contenedor esté ejecutándose
    if ! docker ps | grep -q "$CONTAINER_NAME"; then
        error "El contenedor de rollback no está ejecutándose"
        docker logs "$CONTAINER_NAME"
        exit 1
    fi
    
    # Verificar health check
    if check_health "http://localhost:5000/api/health"; then
        success "Rollback verificado exitosamente"
    else
        error "Rollback falló - la aplicación no responde"
        docker logs "$CONTAINER_NAME"
        exit 1
    fi
}

# Función para mostrar información post-rollback
show_post_rollback_info() {
    log "Información post-rollback:"
    
    echo "📊 Estado del contenedor:"
    docker ps | grep "$CONTAINER_NAME"
    
    echo "📋 Logs recientes:"
    docker logs --tail 10 "$CONTAINER_NAME"
    
    echo "🔍 Información de la aplicación:"
    curl -s http://localhost:5000/api/info | python -m json.tool 2>/dev/null || echo "No se pudo obtener información"
    
    echo "💚 Health check:"
    curl -s http://localhost:5000/api/health | python -m json.tool 2>/dev/null || echo "No se pudo obtener health check"
}

# Función principal
main() {
    echo "🚀 Script de Rollback - DevOps App Emmanuel"
    echo "=========================================="
    
    check_dependencies
    create_backup
    stop_current_container
    execute_rollback
    verify_rollback
    show_post_rollback_info
    
    success "🎉 Rollback completado exitosamente"
    echo ""
    echo "📝 Próximos pasos:"
    echo "1. Monitorear la aplicación por posibles problemas"
    echo "2. Investigar la causa raíz del error original"
    echo "3. Implementar correcciones"
    echo "4. Planificar re-deploy cuando esté listo"
}

# Manejo de señales para cleanup
cleanup() {
    error "Rollback interrumpido"
    exit 1
}

trap cleanup SIGINT SIGTERM

# Ejecutar función principal
main "$@"
