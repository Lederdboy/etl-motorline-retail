"""
ETL MotorLine - Módulo de Extracción de Datos
Autor: Equipo CERTUS
Fecha: Noviembre 2025
Descripción: Extrae datos de ventas desde la base de datos
"""

import mysql.connector
import pandas as pd
import os
from datetime import datetime

print("="*80)
print("EXTRACT - Extraccion de datos desde MySQL")
print("="*80)

# Configuracion de conexion MySQL
config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'BD_VEHICULOS',
    'port': 3307
}

workspace = os.getcwd()
archivo_salida = os.path.join(workspace, 'ventas_raw.csv')

try:
    print(f"[INFO] Conectando a MySQL en localhost:3307...")
    conexion = mysql.connector.connect(**config)
    cursor = conexion.cursor()
    
    print(f"[OK] Conexion exitosa a BD_VEHICULOS")
    
    # Query completa con todos los JOINs necesarios
    query = """
    SELECT 
        v.ID_Venta,
        v.Fecha_Venta,
        c.ID_Cliente,
        c.Nombre AS Cliente_Nombre,
        c.Apellidos AS Cliente_Apellidos,
        c.Tipo_Documento,
        c.Nro_Documento,
        c.Telefono AS Cliente_Telefono,
        c.Email AS Cliente_Email,
        c.Direccion AS Cliente_Direccion,
        c.Tipo_Cliente,
        c.Score_Crediticio,
        m.ID_Modelo,
        m.Nombre_Modelo,
        ma.ID_Marca,
        ma.Nombre AS Marca,
        ma.Pais_Origen,
        veh.ID_Vehiculo,
        veh.VIN,
        veh.Ano_Vehiculo,
        veh.Motor,
        veh.Potencia_HP,
        veh.Cilindraje,
        tv.Nombre_Tipo AS Tipo_Vehiculo,
        col.Nombre_Color AS Color,
        ev.Descripcion_Estado AS Estado_Vehiculo,
        v.Precio_Vent_sinIGV,
        v.IGV,
        v.Precio_venta_real,
        v.Costo_Vehiculo,
        v.Estado_Venta,
        s.ID_Sucursal,
        s.Nombre_Sucursal,
        s.Direccion AS Sucursal_Direccion,
        e.ID_Empleado,
        e.Nombre AS Vendedor_Nombre,
        e.Apellidos AS Vendedor_Apellidos,
        e.Cargo AS Vendedor_Cargo,
        mp.ID_MetodoPago,
        mp.Descripcion AS Metodo_Pago,
        vmp.Monto AS Monto_Pago
    FROM Venta v
    LEFT JOIN Cliente c ON v.ID_Cliente = c.ID_Cliente
    LEFT JOIN Modelo m ON v.ID_Modelo = m.ID_Modelo
    LEFT JOIN Marca ma ON m.ID_Marca = ma.ID_Marca
    LEFT JOIN Vehiculo veh ON v.ID_Vehiculo = veh.ID_Vehiculo
    LEFT JOIN Tipo_Vehiculo tv ON veh.ID_TipoVehiculo = tv.ID_TipoVehiculo
    LEFT JOIN Color col ON veh.ID_Color = col.ID_Color
    LEFT JOIN Estado_Vehiculo ev ON veh.ID_EstadoVehiculo = ev.ID_EstadoVehiculo
    LEFT JOIN Sucursal s ON v.ID_Sucursal = s.ID_Sucursal
    LEFT JOIN Empleado e ON v.ID_Empleado = e.ID_Empleado
    LEFT JOIN Venta_MetodoPago vmp ON v.ID_Venta = vmp.ID_Venta
    LEFT JOIN Metodo_Pago mp ON vmp.ID_MetodoPago = mp.ID_MetodoPago
    ORDER BY v.Fecha_Venta DESC, v.ID_Venta
    """
    
    print(f"[INFO] Ejecutando consulta SQL...")
    df = pd.read_sql(query, conexion)
    
    print(f"[OK] Datos extraidos: {len(df)} registros")
    print(f"[OK] Total de columnas: {len(df.columns)}")
    
    # Guardar CSV crudo
    df.to_csv(archivo_salida, index=False, encoding='utf-8-sig')
    
    print(f"[OK] CSV crudo generado: {archivo_salida}")
    print(f"")
    print(f"Columnas extraidas:")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i:2d}. {col}")
    
    # Mostrar preview de primeros 3 registros
    print(f"")
    print(f"Preview de datos:")
    print(df[['ID_Venta', 'Fecha_Venta', 'Cliente_Nombre', 'Marca', 'Nombre_Modelo', 'Precio_venta_real']].head(3))
    
    cursor.close()
    conexion.close()
    print(f"")
    print(f"[OK] Extraccion completada exitosamente")
    print("="*80)
    
except mysql.connector.Error as err:
    print(f"[ERROR] Error de MySQL: {err}")
    print(f"[INFO] Verifica que:")
    print(f"  - MySQL este corriendo en puerto 3307")
    print(f"  - La base de datos BD_VEHICULOS exista")
    print(f"  - Usuario 'root' tenga acceso sin password")
    exit(1)
    
except Exception as e:
    print(f"[ERROR] Error inesperado: {e}")
    import traceback
    traceback.print_exc()
    exit(1)