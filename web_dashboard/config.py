import os

class Config:
    # Flask
    SECRET_KEY = 'motorline-etl-2025-secret-key-change-in-production'
    DEBUG = True

    # Jenkins (sin token)
    JENKINS_URL = "http://localhost:8081/jenkins"
    JENKINS_USER = "lederdboy"          # dejar vacío si Jenkins está abierto
    JENKINS_PASSWORD = "Lederdboy?2005"      # o usa tu contraseña real si tienes login habilitado
    JENKINS_JOB = "etl_retail"

    # Rutas del proyecto
    BASE_DIR = r"C:\Windows\System32\config\systemprofile\.jenkins\workspace\etl_retail"
    OUTPUT_DIR = os.path.join(BASE_DIR, "output")
    CSV_RAW = os.path.join(BASE_DIR, "ventas_raw.csv")
    CSV_CLEAN = os.path.join(BASE_DIR, "ventas_clean.csv")

    # Email por defecto
    EMAIL_DESTINO = "locopisado3@gmail.com"
    EMAIL_REMITENTE = "jkalef96@gmail.com"

    # Paginación
    REPORTES_POR_PAGINA = 10
