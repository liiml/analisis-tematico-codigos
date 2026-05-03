import pandas as pd
import os
from collections import defaultdict
from utils import (
    procesar_texto_completo, extraer_ngramas, procesar_columna_casos,
    crear_contexto, limpiar_texto, lematizar_texto, quitar_stop_words
)

# Configuración de rutas
ARCHIVO_ENTRADA = "datos/brutos/Análisis temático.xlsx"
HOJA_ENTRADA = "Etiquetas"
ARCHIVO_SALIDA = "datos/procesados/01_ngrams_procesados.xlsx"

# Nombres de columnas (según especificación)
COL_ID = "ID"
COL_CASO = "Caso"
COL_FUENTE = "Fuente"
COL_NIVEL1 = "Etiqueta [Nivel 1]"
COL_NIVEL2 = "Etiqueta [Nivel 2]"
COL_NIVEL3 = "Etiqueta [Nivel 3]"
COL_CARACT = "Caracterización"
COL_CITA = "Cita"

COLUMNAS_CONTENIDO = [COL_NIVEL1, COL_NIVEL2, COL_NIVEL3, COL_CARACT]

def main():
    print("=" * 80)
    print("SCRIPT 1: Limpieza de texto y extracción de n-gramas")
    print("=" * 80)
    
    # Verificar que el archivo existe
    if not os.path.exists(ARCHIVO_ENTRADA):
        print(f"❌ Error: No se encontró {ARCHIVO_ENTRADA}")
        return
    
    # Leer Excel
    print(f"\n📖 Leyendo {ARCHIVO_ENTRADA}...")
    try:
        df = pd.read_excel(ARCHIVO_ENTRADA, sheet_name=HOJA_ENTRADA)
    except Exception as e:
        print(f"❌ Error al leer Excel: {e}")
        return
    
    print(f"   ✓ {len(df)} filas leídas")
    
    # Estructuras de datos para resultados
    ngramas_frecuencia = defaultdict(int)  # ngrama -> frecuencia total
    ngramas_casos = defaultdict(set)  # ngrama -> set de casos
    ngramas_fuentes = defaultdict(set)  # ngrama -> set de fuentes
    ngramas_detalles = []  # lista de detalles para Hoja 4
    
    # Procesar cada fila
    print(f"\n🔄 Procesando {len(df)} filas...")
    
    for idx, row in df.iterrows():
        try:
            caso_str = row[COL_CASO]
            fuente = row[COL_FUENTE]
            id_etiqueta = row[COL_ID]
            
            # Procesar casos múltiples (ej: "10,11")
            casos = procesar_columna_casos(caso_str)
            
            if not casos:
                continue
            
            # Procesar todas las columnas de contenido
            for col in COLUMNAS_CONTENIDO:
                texto_original = row[col]
                
                if pd.isna(texto_original) or not str(texto_original).strip():
                    continue
                
                # Pipeline de procesamiento
                texto_limpio = limpiar_texto(str(texto_original))
                texto_lematizado = lematizar_texto(texto_limpio)
                texto_procesado = quitar_stop_words(texto_lematizado)
                
                # Extraer n-gramas
                ngramas = extraer_ngramas(texto_procesado, min_n=1, max_n=10)
                
                # Para cada n-grama encontrado
                for ngrama in ngramas:
                    # Actualizar frecuencia y casos/fuentes
                    ngramas_frecuencia[ngrama] += 1
                    for caso in casos:
                        ngramas_casos[ngrama].add(caso)
                    ngramas_fuentes[ngrama].add(fuente)
                    
                    # Guardar detalle
                    ngramas_detalles.append({
                        'ID': id_etiqueta,
                        'N-grama': ngrama,
                        'Caso': caso_str,  # Guardar original para referencia
                        'Fuente': fuente,
                        'Nivel': col,
                        'Contexto completo': crear_contexto(row, COLUMNAS_CONTENIDO),
                        'Cita textual': row[COL_CITA] if COL_CITA in row else ""
                    })
        
        except Exception as e:
            print(f"⚠️  Error procesando fila {idx}: {e}")
            continue
    
    print(f"   ✓ {len(ngramas_frecuencia)} n-gramas únicos encontrados")
    
    # Filtrar n-gramas que aparecen al menos 2 veces
    print(f"\n🔍 Filtrando n-gramas (frecuencia >= 2)...")
    ngramas_filtrados = {
        ngrama: freq for ngrama, freq in ngramas_frecuencia.items()
        if freq >= 2
    }
    
    print(f"   ✓ {len(ngramas_filtrados)} n-gramas con frecuencia >= 2")
    
    # Obtener lista de todos los casos únicos
    casos_unicos = sorted(set(
        caso for casos_set in ngramas_casos.values()
        for caso in casos_set
    ))
    
    # Crear hojas de salida
    print(f"\n📝 Generando hojas de Excel...")
    
    # HOJA 1: Frecuencias Globales
    hoja1_data = []
    for ngrama in sorted(ngramas_filtrados.keys()):
        freq = ngramas_filtrados[ngrama]
        casos_list = sorted(list(ngramas_casos[ngrama]))
        fuentes_list = sorted(list(ngramas_fuentes[ngrama]))
        num_casos = len(casos_list)
        num_fuentes = len(fuentes_list)
        pct_casos = (num_casos / len(casos_unicos)) * 100 if casos_unicos else 0
        
        hoja1_data.append({
            'N-grama': ngrama,
            'Frecuencia Total': freq,
            'Casos donde aparece': ', '.join(casos_list),
            'Num Casos': num_casos,
            'Fuentes donde aparece': ', '.join(fuentes_list),
            'Num Fuentes': num_fuentes,
            '% Casos cubiertos': f"{pct_casos:.1f}%"
        })
    
    df_hoja1 = pd.DataFrame(hoja1_data)
    
    # HOJA 2: Matriz Casos × Porcentajes
    hoja2_data = []
    for ngrama in sorted(ngramas_filtrados.keys()):
        fila = {'N-grama': ngrama}
        
        # Contar apariciones por caso
        for caso in casos_unicos:
            # Contar detalles que pertenecen a este caso
            count = sum(1 for det in ngramas_detalles 
                       if det['N-grama'] == ngrama and caso in procesar_columna_casos(det['Caso']))
            fila[f'Caso {caso}'] = count
        
        fila['TOTAL'] = ngramas_filtrados[ngrama]
        
        # Agregar porcentajes
        total = fila['TOTAL']
        for caso in casos_unicos:
            valor = fila[f'Caso {caso}']
            pct = (valor / total * 100) if total > 0 else 0
            fila[f'% Caso {caso}'] = f"{pct:.1f}%"
        
        hoja2_data.append(fila)
    
    df_hoja2 = pd.DataFrame(hoja2_data)
    
    # HOJA 3: Matriz Fuentes × N-gramas
    fuentes_unicas = sorted(set(fuente for fuentes_set in ngramas_fuentes.values() for fuente in fuentes_set))
    
    hoja3_data = []
    for ngrama in sorted(ngramas_filtrados.keys()):
        fila = {'N-grama': ngrama}
        
        for fuente in fuentes_unicas:
            count = sum(1 for det in ngramas_detalles 
                       if det['N-grama'] == ngrama and det['Fuente'] == fuente)
            fila[fuente] = count
        
        fila['TOTAL'] = ngramas_filtrados[ngrama]
        hoja3_data.append(fila)
    
    df_hoja3 = pd.DataFrame(hoja3_data)
    
    # HOJA 4: Registro Detallado (solo con n-gramas filtrados)
    ngramas_detalles_filtrados = [
        det for det in ngramas_detalles
        if det['N-grama'] in ngramas_filtrados
    ]
    
    df_hoja4 = pd.DataFrame(ngramas_detalles_filtrados)
    df_hoja4 = df_hoja4[['ID', 'N-grama', 'Caso', 'Fuente', 'Nivel', 'Contexto completo', 'Cita textual']]
    
    # Escribir Excel con múltiples hojas
    print(f"   ✓ Escribiendo {ARCHIVO_SALIDA}...")
    
    os.makedirs(os.path.dirname(ARCHIVO_SALIDA), exist_ok=True)
    
    with pd.ExcelWriter(ARCHIVO_SALIDA, engine='openpyxl') as writer:
        df_hoja1.to_excel(writer, sheet_name='Frecuencias Globales', index=False)
        df_hoja2.to_excel(writer, sheet_name='Matriz Casos x Porcentajes', index=False)
        df_hoja3.to_excel(writer, sheet_name='Matriz Fuentes x N-gramas', index=False)
        df_hoja4.to_excel(writer, sheet_name='Registro Detallado', index=False)
    
    print(f"\n✅ Proceso completado exitosamente")
    print(f"   📁 Salida: {ARCHIVO_SALIDA}")
    print(f"   📊 Hojas generadas:")
    print(f"      - Frecuencias Globales ({len(df_hoja1)} filas)")
    print(f"      - Matriz Casos x Porcentajes ({len(df_hoja2)} filas)")
    print(f"      - Matriz Fuentes x N-gramas ({len(df_hoja3)} filas)")
    print(f"      - Registro Detallado ({len(df_hoja4)} filas)")
    print("=" * 80)

if __name__ == "__main__":
    main()
