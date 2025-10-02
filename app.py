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
        'profesor': 'Dr. [Nombre del Profesor]',
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

@app.route('/api/devops-tools')
def devops_tools():
    tools = [
        {
            'name': 'Docker',
            'description': 'Plataforma de contenedores para desarrollo y despliegue',
            'category': 'Contenerización'
        },
        {
            'name': 'GitHub Actions',
            'description': 'Automatización de CI/CD integrada con GitHub',
            'category': 'CI/CD'
        },
        {
            'name': 'Terraform',
            'description': 'Infraestructura como código para provisionamiento',
            'category': 'IaC'
        },
        {
            'name': 'Ansible',
            'description': 'Automatización de configuración y gestión',
            'category': 'Configuración'
        },
        {
            'name': 'Jenkins',
            'description': 'Servidor de automatización para CI/CD',
            'category': 'CI/CD'
        }
    ]
    return jsonify({'tools': tools})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
