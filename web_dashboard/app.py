from flask import Flask, render_template, request, redirect, url_for, flash, send_file, jsonify
import os
from datetime import datetime
from config import Config
from utils.jenkins_api import JenkinsAPI
from utils.data_loader import DataLoader
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)
app.config.from_object(Config)

jenkins = JenkinsAPI()
data_loader = DataLoader()

@app.route('/')
def dashboard():
    """Dashboard principal"""
    kpis = data_loader.get_kpis()
    ventas_mensuales = data_loader.get_ventas_mensuales()
    ventas_sucursal = data_loader.get_ventas_por_sucursal()
    reportes = data_loader.get_reportes_generados()
    last_build = jenkins.get_last_build_info()
    
    return render_template('dashboard.html',
                         kpis=kpis,
                         ventas_mensuales=ventas_mensuales,
                         ventas_sucursal=ventas_sucursal,
                         reportes=reportes,
                         last_build=last_build)

@app.route('/historial')
def historial():
    """Página de historial"""
    history = jenkins.get_build_history(20)
    builds = history.get('builds', [])
    
    # Formatear timestamps
    for build in builds:
        try:
            timestamp = build['timestamp'] / 1000
            build['timestamp'] = datetime.fromtimestamp(timestamp).strftime('%d/%m/%Y %H:%M:%S')
        except:
            build['timestamp'] = 'N/A'
    
    reportes = data_loader.get_reportes_generados()
    
    return render_template('historial.html', builds=builds, reportes=reportes)

@app.route('/configuracion')
def configuracion():
    """Página de configuración"""
    return render_template('configuracion.html', config=Config)

@app.route('/configuracion/email', methods=['POST'])
def guardar_configuracion_email():
    """Guardar configuración de email"""
    email_destino = request.form.get('email_destino')
    email_remitente = request.form.get('email_remitente')
    
    # Actualizar config (en producción, guardar en BD o archivo)
    Config.EMAIL_DESTINO = email_destino
    Config.EMAIL_REMITENTE = email_remitente
    
    flash('Configuración de email guardada exitosamente', 'success')
    return redirect(url_for('configuracion'))

@app.route('/api/ejecutar-etl', methods=['POST'])
def ejecutar_etl():
    """API para ejecutar el pipeline ETL"""
    result = jenkins.trigger_build()
    return jsonify(result)

@app.route('/descargar/<filename>')
def descargar_reporte(filename):
    """Descargar un reporte Excel"""
    try:
        filepath = os.path.join(Config.OUTPUT_DIR, filename)
        
        if not os.path.exists(filepath):
            flash('Archivo no encontrado', 'danger')
            return redirect(url_for('dashboard'))
        
        return send_file(filepath, as_attachment=True)
    
    except Exception as e:
        flash(f'Error al descargar archivo: {str(e)}', 'danger')
        return redirect(url_for('dashboard'))

if __name__ == '__main__':
    # Crear carpeta output si no existe
    os.makedirs(Config.OUTPUT_DIR, exist_ok=True)
    
    print("="*80)
    print("MOTORLINE S.A.C. - DASHBOARD ETL")
    print("="*80)
    print(f"Dashboard disponible en: http://localhost:5000")
    print(f"Jenkins URL: {Config.JENKINS_URL}")
    print(f"Output Dir: {Config.OUTPUT_DIR}")
    print("="*80)
    
    app.run(debug=True, host='0.0.0.0', port=5000)