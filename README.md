# 🚗 ETL MotorLine - Sistema de Análisis de Ventas

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![Jenkins](https://img.shields.io/badge/Jenkins-Pipeline-red.svg)](https://www.jenkins.io/)
[![Flask](https://img.shields.io/badge/Flask-Dashboard-green.svg)](https://flask.palletsprojects.com/)

## 📋 Descripción
Pipeline ETL automatizado con Jenkins para el procesamiento y análisis de datos de ventas de MotorLine. Incluye dashboard web interactivo para visualización de métricas y generación de reportes en Excel.

## 🎯 Objetivos
- Automatizar la extracción, transformación y carga (ETL) de datos de ventas
- Generar reportes ejecutivos en formato Excel
- Visualizar métricas clave en dashboard web
- Enviar notificaciones automáticas por email

## 🏗️ Arquitectura del Proyecto

\\\
etl_retail/
├── extract_data.py          # Extracción de datos desde fuente
├── transform_data.py        # Limpieza y transformación
├── load_excel.py           # Generación de reportes Excel
├── send_notification.py    # Sistema de notificaciones
├── output/                 # Reportes generados
└── web_dashboard/          # Dashboard web interactivo
    ├── app.py             # Aplicación Flask
    ├── templates/         # Vistas HTML
    ├── static/           # CSS, JS, imágenes
    └── utils/            # Utilidades (Jenkins API, etc.)
\\\

## 🚀 Tecnologías Utilizadas
- **Python 3.13**: Lenguaje principal
- **Pandas**: Procesamiento de datos
- **Jenkins**: Automatización de pipeline
- **Flask**: Framework web para dashboard
- **OpenPyXL**: Generación de archivos Excel
- **Git & GitHub**: Control de versiones

## 📦 Instalación

### Prerrequisitos
- Python 3.13+
- Jenkins instalado y configurado
- Git

### Configuración del entorno

\\\ash
# Clonar el repositorio
git clone https://github.com/Lederdboy/etl-motorline-retail.git
cd etl-motorline-retail

# Instalar dependencias
pip install -r requirements_web.txt
\\\

## ⚙️ Configuración de Jenkins

### Pipeline Jenkinsfile
\\\groovy
pipeline {
    agent any
    stages {
        stage('Extract') {
            steps {
                bat 'python extract_data.py'
            }
        }
        stage('Transform') {
            steps {
                bat 'python transform_data.py'
            }
        }
        stage('Load') {
            steps {
                bat 'python load_excel.py'
            }
        }
        stage('Notify') {
            steps {
                bat 'python send_notification.py'
            }
        }
    }
}
\\\

## 📊 Dashboard Web

### Ejecutar dashboard localmente
\\\ash
cd web_dashboard
python app.py
\\\

Acceder a: \http://localhost:5000\

### Funcionalidades
- ✅ Visualización de métricas de ventas
- ✅ Gráficos interactivos
- ✅ Historial de ejecuciones
- ✅ Configuración de parámetros
- ✅ Integración con Jenkins API

## 🔄 Workflow Git

### Ramas
- \main\: Código en producción
- \development\: Desarrollo activo
- \eature/*\: Nuevas funcionalidades

### Contribuir
1. Crear rama desde \development\
2. Hacer cambios y commits
3. Push a GitHub
4. Crear Pull Request
5. Code review
6. Merge a \development\

## 👥 Equipo de Desarrollo
Proyecto desarrollado por estudiantes de CERTUS

## 📝 Licencia
Proyecto académico - CERTUS 2025

## 📧 Contacto
jkalef96@gmail.com

---
⭐ Si este proyecto te fue útil, dale una estrella en GitHub!
