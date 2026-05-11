import pandas as pd
import os
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))

from utils import procesar_columna_casos

# Configuración de rutas
ARCHIVO_ENTRADA = "datos/procesados/01_ngramas_procesados.xlsx"
ARCHIVO_SALIDA = "resultados/02_analisis_coocurrencias.xlsx"

def extraer_todos_ngramas(archivo):
    """
    Lee la hoja 'Frecuencias Globales' y extrae todos los n-gramas.
    
    Retorna: set con todos los n-gramas disponibles
    """
    ngramas_todos = set()
    
    try:
        df_freq = pd.read_excel(archivo, sheet_name='Frecuencias Globales')
        ngramas_todos.update(df_freq['N-grama'].dropna().unique())
        print(f"   ✓ {len(ngramas_todos)} n-gramas disponibles extraídos")
    except Exception as e:
        print(f"   ❌ Error leyendo Frecuencias Globales: {e}")
        return set()
    
    return ngramas_todos

def leer_frecuencias_globales(archivo):
    """
    Lee la hoja 'Frecuencias Globales' para obtener metadatos de n-gramas.
    
    Retorna: DataFrame con columnas [N-grama, Frecuencia Total, Num Casos]
    """
    try:
        df = pd.read_excel(archivo, sheet_name='Frecuencias Globales')
        return df[['N-grama', 'Frecuencia Total', 'Num Casos']].copy()
    except Exception as e:
        print(f"   ⚠️  Error leyendo metadatos: {e}")
        return pd.DataFrame()

def obtener_numero_casos_total(df_freq_global):
    """
    Extrae el número total de casos ÚNICOS en el dataset.
    """
    try:
        todos_los_casos = set()
        for casos_str in df_freq_global['Casos donde aparece']:
            if pd.notna(casos_str):
                todos_los_casos.update([c.strip() for c in str(casos_str).split(',')])
        
        if todos_los_casos:
            return len(todos_los_casos)
    except Exception as e:
        print(f"   ⚠️  Error extrayendo número de casos: {e}")
    
    return 16

def extraer_ngramas_seleccionados(archivo):
    """
    Extrae todos los n-gramas de las hojas de selección.
    
    Lee:
    - Frecuencias_seleccion: columnas N-Grama
    
    Retorna: set con todos los n-gramas seleccionados (únicos)
    """
    ngramas_seleccionados = set()
    
    try:
        # Leer Frecuencias_seleccion
        try:
            df_sel1 = pd.read_excel(archivo, sheet_name='Frecuencias_seleccion')
            for col in ['N-Grama']:
                if col in df_sel1.columns:
                    ngramas_seleccionados.update(
                        df_sel1[col].dropna().apply(lambda x: str(x).strip())
                    )
            print(f"   ✓ {len(ngramas_seleccionados)} n-gramas de Frecuencias_seleccion_1")
        except Exception as e:
            print(f"   ⚠️  Frecuencias_seleccion_1 no encontrada o vacía: {e}")
        
        
        print(f"   ✓ Total de n-gramas seleccionados: {len(ngramas_seleccionados)}")
    
    except Exception as e:
        print(f"   ❌ Error extrayendo n-gramas seleccionados: {e}")
    
    return ngramas_seleccionados

def calcular_coocurrencias_fuertes(df_detallado):
    """
    Calcula co-ocurrencias FUERTES - ALGORITMO OPTIMIZADO.
    
    Definición: Dos n-gramas que aparecen juntos en 2+ CASOS DIFERENTES y 
                en AL MENOS 2 FUENTES DIFERENTES
    
    Retorna: dict {(ngrama1, ngrama2): {'casos': set, 'fuentes': set}}
    """
    coocurrencias = defaultdict(lambda: {'casos': set(), 'fuentes': set()})
    
    try:
        print("   (Agrupando por caso-fuente...)")
        
        grupos = df_detallado.groupby(['Caso', 'Fuente'])['N-grama'].apply(list)
        
        total_grupos = len(grupos)
        print(f"   (Procesando {total_grupos} grupos caso-fuente...)")
        
        for idx, (caso_fuente, ngramas_en_grupo) in enumerate(grupos.items()):
            if idx % max(1, total_grupos // 10) == 0:
                print(f"      {idx}/{total_grupos}...")
            
            caso, fuente = caso_fuente
            ngramas_unicos = list(set(ngramas_en_grupo))
            
            for i, ng1 in enumerate(ngramas_unicos):
                for ng2 in ngramas_unicos[i+1:]:
                    key = tuple(sorted([str(ng1).strip(), str(ng2).strip()]))
                    coocurrencias[key]['casos'].add(str(caso).strip())
                    coocurrencias[key]['fuentes'].add(str(fuente).strip())
        
        coocurrencias_filtradas = {
            k: v for k, v in coocurrencias.items()
            if len(v['casos']) >= 2 and len(v['fuentes']) >= 2
        }
        
        print(f"   (Total de parejas antes de filtrar: {len(coocurrencias)})")
        print(f"   (Parejas con 2+ casos Y 2+ fuentes: {len(coocurrencias_filtradas)})")
        
    except Exception as e:
        print(f"⚠️  Error calculando co-ocurrencias fuertes: {e}")
        import traceback
        traceback.print_exc()
        return {}
    
    return coocurrencias_filtradas

def calcular_coocurrencias_debiles(df_detallado):
    """
    Calcula co-ocurrencias DÉBILES - ALGORITMO OPTIMIZADO.
    
    Definición: Dos n-gramas que aparecen juntos en 2+ CASOS DIFERENTES pero
                en LA MISMA FUENTE
    
    Retorna: dict {(ngrama1, ngrama2): {'casos': set, 'fuentes': set}}
    """
    coocurrencias = defaultdict(lambda: {'casos': set(), 'fuentes': set()})
    
    try:
        print("   (Agrupando por fuente...)")
        
        fuentes = df_detallado['Fuente'].unique()
        print(f"   (Procesando {len(fuentes)} fuentes...)")
        
        for fuente_idx, fuente in enumerate(fuentes):
            if fuente_idx % max(1, len(fuentes) // 10) == 0:
                print(f"      {fuente_idx + 1}/{len(fuentes)}...")
            
            df_fuente = df_detallado[df_detallado['Fuente'] == fuente]
            
            casos_en_fuente = df_fuente.groupby('Caso')['N-grama'].apply(list)
            
            for caso, ngramas_en_caso in casos_en_fuente.items():
                ngramas_unicos = list(set(ngramas_en_caso))
                
                for i, ng1 in enumerate(ngramas_unicos):
                    for ng2 in ngramas_unicos[i+1:]:
                        key = tuple(sorted([str(ng1).strip(), str(ng2).strip()]))
                        coocurrencias[key]['casos'].add(str(caso).strip())
                        coocurrencias[key]['fuentes'].add(str(fuente).strip())
        
        coocurrencias_filtradas = {
            k: v for k, v in coocurrencias.items()
            if len(v['casos']) >= 2 and len(v['fuentes']) == 1
        }
        
        print(f"   (Total de parejas antes de filtrar: {len(coocurrencias)})")
        print(f"   (Parejas con 2+ casos en la MISMA fuente: {len(coocurrencias_filtradas)})")
        
    except Exception as e:
        print(f"⚠️  Error calculando co-ocurrencias débiles: {e}")
        import traceback
        traceback.print_exc()
        return {}
    
    return coocurrencias_filtradas

def crear_dataframe_coocurrencias(coocurrencias_dict, df_freq_global, num_casos_total, tipo='Fuerte'):
    """
    Convierte diccionario de co-ocurrencias a DataFrame con todas las propiedades.
    """
    if not coocurrencias_dict:
        print(f"   ⚠️  No hay co-ocurrencias {tipo.lower()} para procesar")
        return pd.DataFrame()
    
    freq_dict = {}
    casos_dict = {}
    if df_freq_global is not None and len(df_freq_global) > 0:
        for _, row in df_freq_global.iterrows():
            ngrama = row['N-grama']
            freq_dict[ngrama] = row['Frecuencia Total']
            casos_dict[ngrama] = row['Num Casos']
    
    data = []
    
    for (ngrama1, ngrama2), info in coocurrencias_dict.items():
        num_casos_cooc = len(info['casos'])
        num_fuentes_cooc = len(info['fuentes'])
        pct_casos_cooc = (num_casos_cooc / num_casos_total * 100) if num_casos_total > 0 else 0
        
        freq_n1 = freq_dict.get(ngrama1, 0)
        freq_n2 = freq_dict.get(ngrama2, 0)
        
        casos_n1 = casos_dict.get(ngrama1, 0)
        casos_n2 = casos_dict.get(ngrama2, 0)
        
        max_casos = max(casos_n1, casos_n2, 1)
        fuerza_asociacion = (num_casos_cooc / max_casos * 100) if max_casos > 0 else 0
        
        casos_union = casos_n1 + casos_n2 - num_casos_cooc
        pct_casos_juntos_vs_separados = (num_casos_cooc / casos_union * 100) if casos_union > 0 else 0
        
        fila = {
            'N-grama 1': ngrama1,
            'N-grama 2': ngrama2,
            'Num Casos': num_casos_cooc,
            'Num Fuentes': num_fuentes_cooc,
            '% Casos coocurren': f"{pct_casos_cooc:.1f}%",
            'Casos donde co-ocurren': ', '.join(sorted([str(c) for c in info['casos']])),
            'Fuentes donde co-ocurren': ', '.join(sorted([str(f) for f in info['fuentes']])),
            'Freq N-grama 1': freq_n1,
            'Freq N-grama 2': freq_n2,
            'Casos N-grama 1': casos_n1,
            'Casos N-grama 2': casos_n2,
            'Fuerza de Asociación': f"{fuerza_asociacion:.1f}%",
            '% Casos Juntos vs Separados': f"{pct_casos_juntos_vs_separados:.1f}%"
        }
        data.append(fila)
    
    df = pd.DataFrame(data)
    if len(df) > 0:
        df = df.sort_values('Num Casos', ascending=False).reset_index(drop=True)
    
    return df

def filtrar_coocurrencias_por_seleccion(df_cooc, ngramas_seleccionados):
    """
    Filtra co-ocurrencias para mantener solo aquellas donde AMBOS n-gramas
    están en la selección jerárquica.
    
    Lógica:
    - Para cada fila, verificar si N-grama 1 AND N-grama 2 están en ngramas_seleccionados
    - Si alguno NO está → eliminar fila
    - Si AMBOS están → mantener fila
    
    Retorna: DataFrame filtrado
    """
    if len(ngramas_seleccionados) == 0:
        print("   ⚠️  No hay n-gramas seleccionados, devolviendo todas las co-ocurrencias")
        return df_cooc
    
    filas_antes = len(df_cooc)
    
    # Crear máscara booleana: True si AMBOS n-gramas están en la selección
    mascara = df_cooc['N-grama 1'].isin(ngramas_seleccionados) & \
              df_cooc['N-grama 2'].isin(ngramas_seleccionados)
    
    df_filtrado = df_cooc[mascara].copy().reset_index(drop=True)
    
    filas_despues = len(df_filtrado)
    filas_eliminadas = filas_antes - filas_despues
    
    print(f"   ✓ Filas antes de filtrar: {filas_antes}")
    print(f"   ✓ Filas después de filtrar: {filas_despues}")
    print(f"   ✓ Filas eliminadas: {filas_eliminadas} ({filas_eliminadas/filas_antes*100:.1f}%)")
    
    return df_filtrado

def main():
    print("=" * 80)
    print("SCRIPT 2: Análisis de co-ocurrencias (ALGORITMO OPTIMIZADO + FILTRADO RESTRICTIVO)")
    print("=" * 80)
    print("\n📖 Definiciones:")
    print("   FUERTE: 2+ casos DIFERENTES y 2+ FUENTES DIFERENTES")
    print("           → Asociación GENERALIZABLE (no es artefacto de una fuente)")
    print("   DÉBIL: 2+ casos DIFERENTES pero MISMA FUENTE")
    print("          → Asociación ESPECÍFICA DE LA FUENTE (puede ser enfoque particular)")
    print("\n🔍 Filtrado:")
    print("   Solo se mantienen co-ocurrencias donde AMBOS n-gramas están en tu selección")
    
    if not os.path.exists(ARCHIVO_ENTRADA):
        print(f"\n❌ Error: No se encontró {ARCHIVO_ENTRADA}")
        return
    
    print(f"\n📋 Extrayendo todos los n-gramas disponibles...")
    ngramas_todos = extraer_todos_ngramas(ARCHIVO_ENTRADA)
    
    if not ngramas_todos:
        print("❌ No se encontraron n-gramas en Frecuencias Globales")
        return
    
    print(f"\n📖 Leyendo datos procesados...")
    
    try:
        df_freq_global = pd.read_excel(ARCHIVO_ENTRADA, sheet_name='Frecuencias Globales')
        df_detallado = pd.read_excel(ARCHIVO_ENTRADA, sheet_name='Registro Detallado')
    except Exception as e:
        print(f"❌ Error leyendo Excel: {e}")
        return
    
    if len(df_freq_global) == 0:
        print("❌ La hoja 'Frecuencias Globales' está vacía")
        return
    
    print(f"   ✓ {len(df_freq_global)} n-gramas en Frecuencias Globales")
    print(f"   ✓ {len(df_detallado)} registros detallados")
    
    num_casos_total = obtener_numero_casos_total(df_freq_global)
    print(f"   ✓ Número total de casos: {num_casos_total}")
    
    print(f"\n📊 Estructura del Registro Detallado:")
    print(f"   Columnas: {list(df_detallado.columns)}")
    print(f"   Primeras 3 filas:")
    for idx, row in df_detallado.head(3).iterrows():
        print(f"      Caso: {row.get('Caso')}, Fuente: {row.get('Fuente')}, Nivel: {row.get('Nivel')}, N-grama: {row.get('N-grama')}")
    
    # CALCULAR CO-OCURRENCIAS
    print(f"\n🔄 Calculando co-ocurrencias FUERTES (2+ casos, 2+ fuentes)...")
    coocurrencias_fuertes = calcular_coocurrencias_fuertes(df_detallado)
    print(f"   ✓ {len(coocurrencias_fuertes)} co-ocurrencias encontradas")
    
    print(f"\n🔄 Calculando co-ocurrencias DÉBILES (2+ casos, misma fuente)...")
    coocurrencias_debiles = calcular_coocurrencias_debiles(df_detallado)
    print(f"   ✓ {len(coocurrencias_debiles)} co-ocurrencias encontradas")
    
    if len(coocurrencias_fuertes) == 0 and len(coocurrencias_debiles) == 0:
        print("\n⚠️  ADVERTENCIA: No se encontraron co-ocurrencias")
        return
    
    print(f"\n📝 Generando DataFrames...")
    df_fuertes = crear_dataframe_coocurrencias(coocurrencias_fuertes, df_freq_global, num_casos_total, 'Fuerte')
    df_debiles = crear_dataframe_coocurrencias(coocurrencias_debiles, df_freq_global, num_casos_total, 'Débil')
    
    # FILTRADO POR SELECCIÓN
    print(f"\n🔍 Leyendo n-gramas seleccionados para filtrado...")
    ngramas_seleccionados = extraer_ngramas_seleccionados(ARCHIVO_ENTRADA)
    
    if len(ngramas_seleccionados) > 0:
        print(f"\n🔍 Filtrando co-ocurrencias FUERTES (AMBOS n-gramas en selección)...")
        df_fuertes_filtrado = filtrar_coocurrencias_por_seleccion(df_fuertes, ngramas_seleccionados)
        
        print(f"\n🔍 Filtrando co-ocurrencias DÉBILES (AMBOS n-gramas en selección)...")
        df_debiles_filtrado = filtrar_coocurrencias_por_seleccion(df_debiles, ngramas_seleccionados)
    else:
        print(f"\n⚠️  No hay n-gramas seleccionados, manteniendo todas las co-ocurrencias")
        df_fuertes_filtrado = df_fuertes
        df_debiles_filtrado = df_debiles
    
    # ESCRIBIR EXCEL
    try:
        os.makedirs(os.path.dirname(ARCHIVO_SALIDA) if os.path.dirname(ARCHIVO_SALIDA) else ".", exist_ok=True)
        
        with pd.ExcelWriter(ARCHIVO_SALIDA, engine='openpyxl') as writer:
            if len(df_fuertes_filtrado) > 0:
                df_fuertes_filtrado.to_excel(writer, sheet_name='Co-ocurrencias Fuertes', index=False)
                print(f"   ✓ Hoja 'Co-ocurrencias Fuertes' ({len(df_fuertes_filtrado)} filas)")
            
            if len(df_debiles_filtrado) > 0:
                df_debiles_filtrado.to_excel(writer, sheet_name='Co-ocurrencias Débiles', index=False)
                print(f"   ✓ Hoja 'Co-ocurrencias Débiles' ({len(df_debiles_filtrado)} filas)")
            
            writer.book.create_sheet('Coocurrencias_seleccion_1')
            writer.book.create_sheet('Coocurrencias_seleccion_2')
            print(f"   ✓ Hojas 'Coocurrencias_seleccion_1' y 'Coocurrencias_seleccion_2' (vacías para selección manual)")
        
        print(f"   ✓ {ARCHIVO_SALIDA}")
    
    except Exception as e:
        print(f"   ❌ Error escribiendo Excel: {e}")
        return
    
    print(f"\n✅ Proceso completado exitosamente")
    print(f"   📁 Salida: {ARCHIVO_SALIDA}")
    print(f"\n📌 PRÓXIMOS PASOS:")
    print(f"   1. Abre {ARCHIVO_SALIDA}")
    print(f"   2. Revisa las co-ocurrencias FILTRADAS (ambos n-gramas en tu selección)")
    print(f"   3. Selecciona las co-ocurrencias que deseas incluir en el análisis visual")
    print(f"   4. Cópialas a 'Coocurrencias_seleccion_1' o 'Coocurrencias_seleccion_2'")
    print(f"   5. Ejecuta el script 02b para generar los gráficos")
    print("=" * 80)

if __name__ == "__main__":
    main()