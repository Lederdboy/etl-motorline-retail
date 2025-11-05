import pandas as pd
import os
from datetime import datetime

print("="*80)
print("TRANSFORM - Limpieza y transformacion de datos")
print("="*80)

workspace = os.getcwd()
archivo_entrada = os.path.join(workspace, 'ventas_raw.csv')
archivo_salida = os.path.join(workspace, 'ventas_clean.csv')

try:
    print(f"[INFO] Leyendo CSV crudo: {archivo_entrada}")
    df = pd.read_csv(archivo_entrada, encoding='utf-8-sig')
    
    print(f"[OK] Registros leidos: {len(df)}")
    print(f"[INFO] Iniciando transformaciones...")
    
    # 1. LIMPIAR DATOS NULOS Y ESPACIOS
    print(f"  [1/8] Limpiando espacios en blanco...")
    columnas_texto = ['Cliente_Nombre', 'Cliente_Apellidos', 'Vendedor_Nombre', 
                      'Vendedor_Apellidos', 'Nombre_Modelo', 'Marca', 'Cliente_Email',
                      'Cliente_Direccion', 'Nombre_Sucursal', 'Metodo_Pago']
    
    for col in columnas_texto:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
            df[col] = df[col].replace('nan', '')
            df[col] = df[col].replace('None', '')
    
    # 2. CREAR NOMBRES COMPLETOS
    print(f"  [2/8] Creando nombres completos...")
    df['Cliente_NombreCompleto'] = (df['Cliente_Nombre'] + ' ' + df['Cliente_Apellidos']).str.strip()
    df['Vendedor_NombreCompleto'] = (df['Vendedor_Nombre'] + ' ' + df['Vendedor_Apellidos']).str.strip()
    df['Vehiculo_Completo'] = (df['Marca'] + ' ' + df['Nombre_Modelo'] + ' ' + df['Ano_Vehiculo'].astype(str)).str.strip()
    
    # 3. CONVERTIR FECHAS
    print(f"  [3/8] Procesando fechas...")
    df['Fecha_Venta'] = pd.to_datetime(df['Fecha_Venta'])
    df['Anio_Venta'] = df['Fecha_Venta'].dt.year
    df['Mes_Venta'] = df['Fecha_Venta'].dt.month
    df['Mes_Nombre'] = df['Fecha_Venta'].dt.strftime('%B')
    df['Trimestre'] = df['Fecha_Venta'].dt.quarter
    df['Dia_Semana'] = df['Fecha_Venta'].dt.day_name()
    
    # 4. CALCULAR METRICAS FINANCIERAS
    print(f"  [4/8] Calculando metricas financieras...")
    df['Margen_Ganancia'] = df['Precio_venta_real'] - df['Costo_Vehiculo']
    df['Porcentaje_Margen'] = ((df['Margen_Ganancia'] / df['Costo_Vehiculo']) * 100).round(2)
    
    # Validar IGV (18%)
    df['IGV_Calculado'] = (df['Precio_Vent_sinIGV'] * 0.18).round(2)
    df['IGV_Correcto'] = (df['IGV'] == df['IGV_Calculado'])
    
    # 5. CATEGORIZAR VENTAS
    print(f"  [5/8] Categorizando ventas...")
    # Categorizar por monto
    def categorizar_venta(precio):
        if precio < 50000:
            return 'Economico'
        elif precio < 100000:
            return 'Medio'
        elif precio < 200000:
            return 'Premium'
        else:
            return 'Lujo'
    
    df['Categoria_Precio'] = df['Precio_venta_real'].apply(categorizar_venta)
    
    # Categorizar por score crediticio
    def categorizar_score(score):
        if pd.isna(score):
            return 'Sin Score'
        elif score < 400:
            return 'Bajo'
        elif score < 600:
            return 'Medio'
        elif score < 750:
            return 'Bueno'
        else:
            return 'Excelente'
    
    df['Categoria_Score'] = df['Score_Crediticio'].apply(categorizar_score)
    
    # 6. LIMPIAR VALORES NULOS
    print(f"  [6/8] Manejando valores nulos...")
    df['Cliente_Email'] = df['Cliente_Email'].fillna('Sin email')
    df['Cliente_Telefono'] = df['Cliente_Telefono'].fillna('Sin telefono')
    df['Metodo_Pago'] = df['Metodo_Pago'].fillna('Efectivo')
    df['Monto_Pago'] = df['Monto_Pago'].fillna(df['Precio_venta_real'])
    
    # 7. AGREGAR INDICADORES
    print(f"  [7/8] Agregando indicadores de negocio...")
    # Venta rentable (margen > 10%)
    df['Venta_Rentable'] = df['Porcentaje_Margen'] > 10
    
    # Cliente frecuente (score > 700)
    df['Cliente_Premium'] = df['Score_Crediticio'] > 700
    
    # Venta grande (precio > promedio)
    precio_promedio = df['Precio_venta_real'].mean()
    df['Venta_Grande'] = df['Precio_venta_real'] > precio_promedio
    
    # 8. ORDENAR DATOS
    print(f"  [8/8] Ordenando datos...")
    df = df.sort_values(by=['Fecha_Venta', 'Precio_venta_real'], ascending=[False, False])
    
    # Resetear indices
    df = df.reset_index(drop=True)
    
    # Guardar CSV limpio
    df.to_csv(archivo_salida, index=False, encoding='utf-8-sig')
    
    print(f"")
    print(f"[OK] Transformaciones completadas")
    print(f"[OK] Registros procesados: {len(df)}")
    print(f"[OK] Total columnas: {len(df.columns)}")
    print(f"[OK] CSV limpio guardado: {archivo_salida}")
    
    # ESTADISTICAS
    print(f"")
    print(f"ESTADISTICAS DE TRANSFORMACION:")
    print(f"  - Ventas totales: {len(df)}")
    print(f"  - Clientes unicos: {df['ID_Cliente'].nunique()}")
    print(f"  - Sucursales activas: {df['ID_Sucursal'].nunique()}")
    print(f"  - Vendedores activos: {df['ID_Empleado'].nunique()}")
    print(f"  - Marcas vendidas: {df['Marca'].nunique()}")
    print(f"  - Precio promedio: S/. {df['Precio_venta_real'].mean():,.2f}")
    print(f"  - Margen promedio: {df['Porcentaje_Margen'].mean():.2f}%")
    print(f"  - Ventas rentables: {df['Venta_Rentable'].sum()} ({df['Venta_Rentable'].sum()/len(df)*100:.1f}%)")
    
    print(f"")
    print(f"NUEVAS COLUMNAS CREADAS:")
    nuevas_columnas = ['Cliente_NombreCompleto', 'Vendedor_NombreCompleto', 'Vehiculo_Completo',
                       'Anio_Venta', 'Mes_Venta', 'Mes_Nombre', 'Trimestre', 'Dia_Semana',
                       'Margen_Ganancia', 'Porcentaje_Margen', 'IGV_Calculado', 'IGV_Correcto',
                       'Categoria_Precio', 'Categoria_Score', 'Venta_Rentable', 'Cliente_Premium', 'Venta_Grande']
    
    for i, col in enumerate(nuevas_columnas, 1):
        print(f"  {i:2d}. {col}")
    
    print("="*80)
    
except FileNotFoundError:
    print(f"[ERROR] No se encuentra el archivo {archivo_entrada}")
    print(f"[INFO] Asegurate de ejecutar extract_data.py primero")
    exit(1)
    
except Exception as e:
    print(f"[ERROR] Error al transformar: {e}")
    import traceback
    traceback.print_exc()
    exit(1)