import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import glob
from datetime import datetime

print("="*80)
print("NOTIFY - Enviando notificacion por email")
print("="*80)

# Configuracion de email
email_destino = "gibaja.eustaquio@gmail.com"
email_remitente = "jkalef96@gmail.com"  # TU EMAIL REAL
password = "wflg cocn oevy yiis"  # App Password de Gmail

workspace = os.getcwd()

# ===== NUEVA LÓGICA: Buscar archivo más reciente en carpeta output =====
output_dir = os.path.join(workspace, 'output')
patron_archivo = os.path.join(output_dir, 'MotorLine_Reporte_Ventas_*.xlsx')
archivos_excel = glob.glob(patron_archivo)

if not archivos_excel:
    print(f"[ERROR] No se encontro ningun archivo Excel en: {output_dir}")
    print(f"[INFO] Asegurate de ejecutar load_excel.py primero")
    exit(1)

# Obtener el archivo más reciente
archivo_excel = max(archivos_excel, key=os.path.getctime)
nombre_archivo = os.path.basename(archivo_excel)
print(f"[INFO] Archivo encontrado: {nombre_archivo}")
# ========================================================================

try:
    # Verificar que existe el archivo Excel
    if not os.path.exists(archivo_excel):
        print(f"[ERROR] No se encuentra el archivo Excel: {archivo_excel}")
        print(f"[INFO] Asegurate de ejecutar load_excel.py primero")
        exit(1)
    
    print(f"[INFO] Preparando email...")
    
    # Crear mensaje
    msg = MIMEMultipart()
    msg['From'] = email_remitente
    msg['To'] = email_destino
    msg['Subject'] = f"Pipeline ETL Completado - MotorLine S.A.C. ({datetime.now().strftime('%d/%m/%Y %H:%M')})"
    
    # Cuerpo del email en HTML
    html = f"""
    <html>
      <head>
        <style>
          body {{ font-family: Arial, sans-serif; }}
          .header {{ background-color: #366092; color: white; padding: 20px; text-align: center; }}
          .content {{ padding: 20px; }}
          .success {{ color: #28a745; font-weight: bold; }}
          .info {{ background-color: #f8f9fa; padding: 15px; border-left: 4px solid #366092; margin: 10px 0; }}
          .footer {{ background-color: #f1f1f1; padding: 10px; text-align: center; font-size: 12px; }}
          table {{ border-collapse: collapse; width: 100%; margin: 15px 0; }}
          th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
          th {{ background-color: #366092; color: white; }}
        </style>
      </head>
      <body>
        <div class="header">
          <h1>MotorLine S.A.C.</h1>
          <h2>Pipeline ETL - Reporte de Ventas</h2>
        </div>
        
        <div class="content">
          <p class="success">✅ El pipeline ETL se ha ejecutado exitosamente!</p>
          
          <div class="info">
            <h3>📋 Informacion del Proceso:</h3>
            <ul>
              <li><strong>Fecha de ejecucion:</strong> {datetime.now().strftime('%d/%m/%Y')}</li>
              <li><strong>Hora de ejecucion:</strong> {datetime.now().strftime('%H:%M:%S')}</li>
              <li><strong>Archivo generado:</strong> {nombre_archivo}</li>
              <li><strong>Estado:</strong> <span style="color: #28a745;">COMPLETADO</span></li>
            </ul>
          </div>
          
          <h3>🔄 Etapas Ejecutadas:</h3>
          <table>
            <tr>
              <th>Etapa</th>
              <th>Descripcion</th>
              <th>Estado</th>
            </tr>
            <tr>
              <td>1. EXTRACT</td>
              <td>Extraccion de datos desde MySQL</td>
              <td style="color: #28a745;">✓ OK</td>
            </tr>
            <tr>
              <td>2. TRANSFORM</td>
              <td>Limpieza y transformacion de datos</td>
              <td style="color: #28a745;">✓ OK</td>
            </tr>
            <tr>
              <td>3. LOAD</td>
              <td>Generacion de Excel con reportes</td>
              <td style="color: #28a745;">✓ OK</td>
            </tr>
            <tr>
              <td>4. NOTIFY</td>
              <td>Notificacion por email</td>
              <td style="color: #28a745;">✓ OK</td>
            </tr>
          </table>
          
          <h3>📁 Archivos Generados:</h3>
          <ul>
            <li><strong>ventas_raw.csv</strong> - Datos crudos extraidos de BD (40 registros × 44 columnas)</li>
            <li><strong>ventas_clean.csv</strong> - Datos limpios y transformados (40 registros × 61 columnas)</li>
            <li><strong>{nombre_archivo}</strong> - Reporte final (ADJUNTO)</li>
          </ul>
          
          <div class="info">
            <p><strong>📊 El archivo Excel adjunto contiene:</strong></p>
            <ul>
              <li><strong>Hoja 1:</strong> Datos completos de ventas (40 registros, 61 columnas)</li>
              <li><strong>Hoja 2:</strong> Resumen ejecutivo y estadisticas (9 métricas principales)</li>
              <li><strong>Hoja 3:</strong> Dashboard con 4 graficos interactivos:
                <ul>
                  <li>📈 Ventas Mensuales (Línea)</li>
                  <li>📊 Ventas por Sucursal (Barras)</li>
                  <li>🏆 Top 10 Modelos Vendidos (Barras Horizontales)</li>
                  <li>🥧 Distribución Métodos de Pago (Circular)</li>
                </ul>
              </li>
            </ul>
          </div>
          
          <p>Para cualquier consulta, contacte al administrador del sistema.</p>
        </div>
        
        <div class="footer">
          <p>Este es un mensaje automatico generado por el Pipeline ETL de MotorLine S.A.C.</p>
          <p>Sistema: Jenkins 2.400+ | Python 3.13 | MySQL 8.0 | Openpyxl 3.1.5</p>
          <p>No responder a este correo</p>
        </div>
      </body>
    </html>
    """
    
    msg.attach(MIMEText(html, 'html'))
    
    # Adjuntar archivo Excel
    print(f"[INFO] Adjuntando archivo Excel...")
    with open(archivo_excel, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
    
    encoders.encode_base64(part)
    part.add_header(
        'Content-Disposition',
        f'attachment; filename= {nombre_archivo}'
    )
    msg.attach(part)
    
    print(f"[INFO] Conectando a Gmail SMTP...")
    
    # ENVIO REAL ACTIVADO
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_remitente, password)
    
    text = msg.as_string()
    server.sendmail(email_remitente, email_destino, text)
    server.quit()
    
    print(f"")
    print(f"[OK] Email enviado exitosamente!")
    print(f"")
    print(f"DETALLES DEL EMAIL:")
    print(f"  De: {email_remitente}")
    print(f"  Para: {email_destino}")
    print(f"  Asunto: Pipeline ETL Completado - MotorLine S.A.C.")
    print(f"  Adjunto: {nombre_archivo} ({os.path.getsize(archivo_excel) / 1024:.2f} KB)")
    print(f"  Ubicacion: {archivo_excel}")
    print(f"")
    print("="*80)
    
except Exception as e:
    print(f"[ERROR] Error al preparar/enviar email: {e}")
    import traceback
    traceback.print_exc()
    exit(1)