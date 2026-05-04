import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))

from utils import procesar_columna_casos

# Configuración de rutas
ARCHIVO_ENTRADA = "datos/procesados/01_ngrams_procesados.xlsx"
ARCHIVO_SALIDA = "resultados/02_analisis_coocurrencias_filtrado.xlsx"
GRAFICO_FUERTE = "resultados/red_temas_fuerte_filtrado.png"
GRAFICO_DEBIL = "resultados/red_temas_debil_filtrado.png"

def extraer_ngramas_seleccionados(archivo):
    """
    Lee las hojas 'Frecuencias_seleccion_1' y 'Frecuencias_seleccion_2' y extrae todos los n-gramas únicos.
    Retorna set con todos los n-gramas seleccionados.
    """
    ngramas_seleccionados = set()
    
    try:
        # Leer Frecuencias_seleccion_1
        try:
            df_sel1 = pd.read_excel(archivo, sheet_name='Frecuencias_seleccion_1')
            for col in ['N-Grama [1]', 'N-Grama [2]', 'N-Grama [3]']:
                if col in df_sel1.columns:
                    ngramas_seleccionados.update(df_sel1[col].dropna().unique())
            print(f"   ✓ Frecuencias_seleccion_1: {len(df_sel1)} filas leídas")
        except Exception as e:
            print(f"   ⚠️  No se encontró 'Frecuencias_seleccion_1': {e}")
        
        # Leer Frecuencias_seleccion_2
        try:
            df_sel2 = pd.read_excel(archivo, sheet_name='Frecuencias_seleccion_2')
            for col in ['N-Grama [1]', 'N-Grama [2]', 'N-Grama [3]']:
                if col in df_sel2.columns:
                    ngramas_seleccionados.update(df_sel2[col].dropna().unique())
            print(f"   ✓ Frecuencias_seleccion_2: {len(df_sel2)} filas leídas")
        except Exception as e:
            print(f"   ⚠️  No se encontró 'Frecuencias_seleccion_2': {e}")
    
    except Exception as e:
        print(f"   ❌ Error leyendo hojas de seleccionados: {e}")
        return set()
    
    return ngramas_seleccionados

def calcular_coocurrencias_fuertes_filtrado(df_detallado, ngramas_validos):
    """
    Calcula co-ocurrencias FUERTES solo para n-gramas seleccionados.
    """
    if df_detallado is None or len(df_detallado) == 0:
        print("⚠️  ADVERTENCIA: No hay datos en 'Registro Detallado'")
        return {}
    
    coocurrencias = defaultdict(lambda: {'count': 0, 'casos': set(), 'fuentes': set()})
    
    try:
        for _, grupo in df_detallado.groupby(['ID', 'Caso', 'Fuente', 'Nivel']):
            ngramas = grupo['N-grama'].unique()
            
            # Filtrar solo los n-gramas seleccionados
            ngramas_validos_grupo = [ng for ng in ngramas if str(ng).strip() in ngramas_validos]
            
            # Generar combinaciones
            for i, ngrama1 in enumerate(ngramas_validos_grupo):
                for ngrama2 in ngramas_validos_grupo[i+1:]:
                    key = tuple(sorted([str(ngrama1).strip(), str(ngrama2).strip()]))
                    
                    coocurrencias[key]['count'] += 1
                    
                    caso_str = grupo.iloc[0]['Caso']
                    if pd.notna(caso_str):
                        coocurrencias[key]['casos'].update(procesar_columna_casos(caso_str))
                    
                    fuente = grupo.iloc[0]['Fuente']
                    if pd.notna(fuente) and str(fuente).strip():
                        coocurrencias[key]['fuentes'].add(str(fuente).strip())
    
    except Exception as e:
        print(f"⚠️  Error procesando co-ocurrencias fuertes: {e}")
        return {}
    
    return dict(coocurrencias)

def calcular_coocurrencias_debiles_filtrado(df_detallado, ngramas_validos):
    """
    Calcula co-ocurrencias DÉBILES solo para n-gramas seleccionados.
    """
    if df_detallado is None or len(df_detallado) == 0:
        print("⚠️  ADVERTENCIA: No hay datos en 'Registro Detallado'")
        return {}
    
    coocurrencias = defaultdict(lambda: {'count': 0, 'casos': set(), 'fuentes': set()})
    
    try:
        for _, grupo in df_detallado.groupby(['ID', 'Caso', 'Fuente']):
            ngramas_por_nivel = defaultdict(list)
            
            for _, row in grupo.iterrows():
                nivel = row['Nivel']
                ngrama = str(row['N-grama']).strip()
                
                # Solo agregar si está en los seleccionados
                if ngrama in ngramas_validos:
                    ngramas_por_nivel[nivel].append(ngrama)
            
            niveles = list(ngramas_por_nivel.keys())
            for i, nivel1 in enumerate(niveles):
                for nivel2 in niveles[i+1:]:
                    for ngrama1 in ngramas_por_nivel[nivel1]:
                        for ngrama2 in ngramas_por_nivel[nivel2]:
                            key = tuple(sorted([ngrama1, ngrama2]))
                            
                            coocurrencias[key]['count'] += 1
                            
                            caso_str = grupo.iloc[0]['Caso']
                            if pd.notna(caso_str):
                                coocurrencias[key]['casos'].update(procesar_columna_casos(caso_str))
                            
                            fuente = grupo.iloc[0]['Fuente']
                            if pd.notna(fuente) and str(fuente).strip():
                                coocurrencias[key]['fuentes'].add(str(fuente).strip())
    
    except Exception as e:
        print(f"⚠️  Error procesando co-ocurrencias débiles: {e}")
        return {}
    
    return dict(coocurrencias)

def crear_dataframe_coocurrencias(coocurrencias_dict, df_freq_global):
    """Convierte diccionario de co-ocurrencias a DataFrame."""
    if not coocurrencias_dict:
        print("   ⚠️  No hay co-ocurrencias para procesar")
        return pd.DataFrame()
    
    data = []
    
    for (ngrama1, ngrama2), info in coocurrencias_dict.items():
        fila = {
            'N-grama 1': ngrama1,
            'N-grama 2': ngrama2,
            'Veces juntos': info['count'],
            'Num Casos': len(info['casos']),
            'Num Fuentes': len(info['fuentes']),
            'Casos donde co-ocurren': ', '.join(sorted([str(c) for c in info['casos']])),
            'Fuentes donde co-ocurren': ', '.join(sorted([str(f) for f in info['fuentes']]))
        }
        data.append(fila)
    
    return pd.DataFrame(data)

def crear_red(coocurrencias_dict, df_freq_global, titulo):
    """Crea un grafo NetworkX visualizando co-ocurrencias."""
    G = nx.Graph()
    
    if df_freq_global is not None and len(df_freq_global) > 0:
        for _, row in df_freq_global.iterrows():
            ngrama = row['N-grama']
            freq = row['Frecuencia Total']
            num_casos = row['Num Casos']
            G.add_node(ngrama, freq=freq, num_casos=num_casos)
    
    for (ngrama1, ngrama2), info in coocurrencias_dict.items():
        if ngrama1 in G.nodes() and ngrama2 in G.nodes():
            G.add_edge(ngrama1, ngrama2, weight=info['count'])
    
    return G

def visualizar_red(G, titulo, archivo_salida, num_casos_total):
    """Visualiza la red y la guarda como imagen."""
    if len(G.nodes()) == 0:
        print(f"   ⚠️  No hay nodos para visualizar en '{titulo}'")
        return
    
    try:
        plt.figure(figsize=(16, 12))
        
        pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
        
        node_sizes = [max(G.nodes[node].get('freq', 1) * 10, 100) for node in G.nodes()]
        
        node_colors = []
        for node in G.nodes():
            num_casos = G.nodes[node].get('num_casos', 0)
            pct = (num_casos / num_casos_total * 100) if num_casos_total > 0 else 0
            node_colors.append(pct)
        
        edge_widths = [G[u][v].get('weight', 1) * 0.5 for u, v in G.edges()]
        
        nodes = nx.draw_networkx_nodes(
            G, pos,
            node_size=node_sizes,
            node_color=node_colors,
            cmap='YlOrRd',
            vmin=0,
            vmax=100,
            alpha=0.8
        )
        
        edges = nx.draw_networkx_edges(
            G, pos,
            width=edge_widths,
            alpha=0.5
        )
        
        labels = nx.draw_networkx_labels(
            G, pos,
            font_size=8,
            font_weight='bold'
        )
        
        plt.title(titulo, fontsize=16, fontweight='bold')
        plt.colorbar(nodes, label='% Casos cubiertos')
        plt.axis('off')
        plt.tight_layout()
        
        os.makedirs(os.path.dirname(archivo_salida) if os.path.dirname(archivo_salida) else ".", exist_ok=True)
        
        plt.savefig(archivo_salida, dpi=300, bbox_inches='tight')
        print(f"   ✓ Gráfico guardado: {archivo_salida}")
        plt.close()
    
    except Exception as e:
        print(f"   ❌ Error generando gráfico: {e}")
        plt.close()

def obtener_numero_casos_total(df_freq_global):
    """Extrae dinámicamente el número total de casos del DataFrame."""
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

def main():
    print("=" * 80)
    print("SCRIPT 2 (FILTRADO): Análisis de co-ocurrencias con n-gramas seleccionados")
    print("=" * 80)
    
    # Verificar que el archivo existe
    if not os.path.exists(ARCHIVO_ENTRADA):
        print(f"❌ Error: No se encontró {ARCHIVO_ENTRADA}")
        return
    
    # Extraer n-gramas seleccionados
    print(f"\n📋 Extrayendo n-gramas seleccionados...")
    ngramas_seleccionados = extraer_ngramas_seleccionados(ARCHIVO_ENTRADA)
    
    if not ngramas_seleccionados:
        print("❌ No se encontraron hojas de seleccionados o están vacías")
        return
    
    print(f"   ✓ {len(ngramas_seleccionados)} n-gramas seleccionados")
    
    # Leer datos de entrada
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
    
    print(f"   ✓ {len(df_freq_global)} n-gramas en total")
    print(f"   ✓ {len(df_detallado)} registros detallados")
    
    # Filtrar df_freq_global a solo los seleccionados
    df_freq_filtrado = df_freq_global[df_freq_global['N-grama'].isin(ngramas_seleccionados)].copy()
    print(f"   ✓ {len(df_freq_filtrado)} n-gramas después del filtrado")
    
    if len(df_freq_filtrado) == 0:
        print("❌ No se encontraron n-gramas seleccionados en Frecuencias Globales")
        return
    
    # Calcular número de casos
    num_casos_total = obtener_numero_casos_total(df_freq_filtrado)
    print(f"   ✓ Número total de casos: {num_casos_total}")
    
    # Calcular co-ocurrencias
    print(f"\n🔄 Calculando co-ocurrencias FUERTES...")
    coocurrencias_fuertes = calcular_coocurrencias_fuertes_filtrado(df_detallado, ngramas_seleccionados)
    print(f"   ✓ {len(coocurrencias_fuertes)} co-ocurrencias encontradas")
    
    print(f"\n🔄 Calculando co-ocurrencias DÉBILES...")
    coocurrencias_debiles = calcular_coocurrencias_debiles_filtrado(df_detallado, ngramas_seleccionados)
    print(f"   ✓ {len(coocurrencias_debiles)} co-ocurrencias encontradas")
    
    if len(coocurrencias_fuertes) == 0 and len(coocurrencias_debiles) == 0:
        print("\n⚠️  ADVERTENCIA: No se encontraron co-ocurrencias")
        return
    
    # Crear DataFrames
    print(f"\n📝 Generando Excel de co-ocurrencias...")
    df_fuertes = crear_dataframe_coocurrencias(coocurrencias_fuertes, df_freq_filtrado)
    df_debiles = crear_dataframe_coocurrencias(coocurrencias_debiles, df_freq_filtrado)
    
    # Escribir Excel
    try:
        os.makedirs(os.path.dirname(ARCHIVO_SALIDA) if os.path.dirname(ARCHIVO_SALIDA) else ".", exist_ok=True)
        
        with pd.ExcelWriter(ARCHIVO_SALIDA, engine='openpyxl') as writer:
            if len(df_fuertes) > 0:
                df_fuertes.to_excel(writer, sheet_name='Co-ocurrencias Fuertes', index=False)
                print(f"   ✓ Hoja 'Co-ocurrencias Fuertes' ({len(df_fuertes)} filas)")
            
            if len(df_debiles) > 0:
                df_debiles.to_excel(writer, sheet_name='Co-ocurrencias Débiles', index=False)
                print(f"   ✓ Hoja 'Co-ocurrencias Débiles' ({len(df_debiles)} filas)")
        
        print(f"   ✓ {ARCHIVO_SALIDA}")
    
    except Exception as e:
        print(f"   ❌ Error escribiendo Excel: {e}")
        return
    
    # Crear gráficos
    print(f"\n📊 Generando gráficos de redes...")
    
    if len(coocurrencias_fuertes) > 0:
        G_fuerte = crear_red(coocurrencias_fuertes, df_freq_filtrado, "Red FUERTE")
        visualizar_red(G_fuerte, "Red de Co-ocurrencias FUERTES (Filtrada)", GRAFICO_FUERTE, num_casos_total)
    
    if len(coocurrencias_debiles) > 0:
        G_debil = crear_red(coocurrencias_debiles, df_freq_filtrado, "Red DÉBIL")
        visualizar_red(G_debil, "Red de Co-ocurrencias DÉBILES (Filtrada)", GRAFICO_DEBIL, num_casos_total)
    
    print(f"\n✅ Proceso completado exitosamente")
    print(f"   📁 Salida: {ARCHIVO_SALIDA}")
    print("=" * 80)

if __name__ == "__main__":
    main()
