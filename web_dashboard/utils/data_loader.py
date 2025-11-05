import pandas as pd
import os
import glob
from datetime import datetime
from config import Config

class DataLoader:
    
    @staticmethod
    def get_kpis():
        """Obtiene KPIs principales desde ventas_clean.csv"""
        try:
            if not os.path.exists(Config.CSV_CLEAN):
                return None
            
            df = pd.read_csv(Config.CSV_CLEAN, encoding='utf-8-sig')
            
            return {
                'total_ventas': len(df),
                'ingresos_totales': f"S/. {df['Precio_venta_real'].sum():,.2f}",
                'ticket_promedio': f"S/. {df['Precio_venta_real'].mean():,.2f}",
                'margen_promedio': f"{df['Porcentaje_Margen'].mean():.2f}%",
                'ventas_rentables': f"{df['Venta_Rentable'].sum()} ({df['Venta_Rentable'].sum()/len(df)*100:.1f}%)",
                'clientes_unicos': df['ID_Cliente'].nunique(),
                'vendedores_activos': df['ID_Empleado'].nunique(),
                'sucursales_activas': df['ID_Sucursal'].nunique()
            }
        except Exception as e:
            print(f"Error al cargar KPIs: {e}")
            return None
    
    @staticmethod
    def get_ventas_mensuales():
        """Obtiene serie temporal de ventas mensuales"""
        try:
            if not os.path.exists(Config.CSV_CLEAN):
                return None
            
            df = pd.read_csv(Config.CSV_CLEAN, encoding='utf-8-sig')
            
            ventas_mes = df.groupby(['Anio_Venta', 'Mes_Venta', 'Mes_Nombre'])['Precio_venta_real'].sum().reset_index()
            ventas_mes = ventas_mes.sort_values(['Anio_Venta', 'Mes_Venta'])
            
            return {
                'labels': ventas_mes['Mes_Nombre'].tolist(),
                'values': ventas_mes['Precio_venta_real'].tolist()
            }
        except:
            return None
    
    @staticmethod
    def get_ventas_por_sucursal():
        """Obtiene ventas por sucursal"""
        try:
            if not os.path.exists(Config.CSV_CLEAN):
                return None
            
            df = pd.read_csv(Config.CSV_CLEAN, encoding='utf-8-sig')
            
            ventas_suc = df.groupby('Nombre_Sucursal')['Precio_venta_real'].sum().reset_index()
            ventas_suc = ventas_suc.sort_values('Precio_venta_real', ascending=False)
            
            return {
                'labels': ventas_suc['Nombre_Sucursal'].tolist(),
                'values': ventas_suc['Precio_venta_real'].tolist()
            }
        except:
            return None
    
    @staticmethod
    def get_reportes_generados():
        """Lista todos los reportes Excel generados"""
        try:
            patron = os.path.join(Config.OUTPUT_DIR, 'MotorLine_Reporte_Ventas_*.xlsx')
            archivos = glob.glob(patron)
            
            reportes = []
            for archivo in sorted(archivos, key=os.path.getctime, reverse=True):
                nombre = os.path.basename(archivo)
                timestamp_str = nombre.replace('MotorLine_Reporte_Ventas_', '').replace('.xlsx', '')
                
                try:
                    fecha = datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')
                    fecha_formato = fecha.strftime('%d/%m/%Y %H:%M:%S')
                except:
                    fecha_formato = timestamp_str
                
                reportes.append({
                    'nombre': nombre,
                    'ruta': archivo,
                    'fecha': fecha_formato,
                    'tamanio': f"{os.path.getsize(archivo) / 1024:.2f} KB"
                })
            
            return reportes
        except:
            return []