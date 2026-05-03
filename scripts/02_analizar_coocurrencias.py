import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os
import sys
from collections import defaultdict
from pathlib import Path

# Agregar el directorio actual al path para importar utils
sys.path.insert(0, os.path.dirname(__file__))

from utils import procesar_columna_casos

# Configuración de rutas
ARCHIVO_ENTRADA = "datos/procesados/01_ngrams_procesados.xlsx"
ARCHIVO_SALIDA_COOCURRENCIAS = "resultados/02_analisis_coocurrencias.xlsx"
GRAFICO_FUERTE = "resultados/red_temas_fuerte.png"
GRAFICO_DEBIL = "resultados/red_temas_debil.png"

def calcular_coocurrencias_fuertes(df_detallado):
    """
    Calcula co-ocurrencias FUERTES (misma columna, misma fila).
    Retorna diccionario: {(ngrama1, ngrama2): {'count': int, 'casos': set, 'fuentes': set}}
    """
    if df_detallado is None or len(df_detallado) == 0:
        print("⚠️  ADVERTENCIA: No hay datos en 'Registro Detallado'")
        return {}
    
    coocurrencias = defaultdict(lambda: {'count': 0, 'casos': set(), 'fuentes': set()})
    
    # Agrupar por fila original (misma ID, Caso, Fuente, Nivel)
    try:
        for _, grupo in df_detallado.groupby(['ID', 'Caso', 'Fuente', 'Nivel']):
            ngramas = grupo['N-grama'].unique()
            
            # Generar todas las combinaciones de n-gramas en esta fila
            for i, ngrama1 in enumerate(ngramas):
                for ngrama2 in ngramas[i+1:]:
                    # Ordenar para evitar duplicados (a,b) y (b,a)
                    key = tuple(sorted([str(ngrama1), str(ngrama2)]))
                    
                    coocurrencias[key]['count'] += 1
                    
                    # Procesar casos de forma segura
                    caso_str = grupo.iloc[0]['Caso']
                    if pd.notna(caso_str):
                        coocurrencias[key]['casos'].update(procesar_columna_casos(caso_str))
                    
                    # Procesar fuente de forma segura
                    fuente = grupo.iloc[0]['Fuente']
                    if pd.notna(fuente) and str(fuente).strip():
                        coocurrencias[key]['fuentes'].add(str(fuente).strip())
    
    except Exception as e:
        print(f"⚠️  Error procesando co-ocurrencias fuertes: {e}")
        return {}
    
    return dict(coocurrencias)

def calcular_coocurrencias_debiles(df_detallado):
    """
    Calcula co-ocurrencias DÉBILES (diferentes columnas, misma fila).
    Retorna diccionario: {(ngrama1, ngrama2): {'count': int, 'casos': set, 'fuentes': set}}
    """
    if df_detallado is None or len(df_detallado) == 0:
        print("⚠️  ADVERTENCIA: No hay datos en 'Registro Detallado'")
        return {}
    
    coocurrencias = defaultdict(lambda: {'count': 0, 'casos': set(), 'fuentes': set()})
    
    # Agrupar por fila original (misma ID, Caso, Fuente)
    try:
        for _, grupo in df_detallado.groupby(['ID', 'Caso', 'Fuente']):
            ngramas_por_nivel = defaultdict(list)
            
            # Agrupar n-gramas por nivel
            for _, row in grupo.iterrows():
                nivel = row['Nivel']
                ngrama = row['N-grama']
                ngramas_por_nivel[nivel].append(str(ngrama))
            
            # Generar co-ocurrencias entre diferentes niveles
            niveles = list(ngramas_por_nivel.keys())
            for i, nivel1 in enumerate(niveles):
                for nivel2 in niveles[i+1:]:
                    for ngrama1 in ngramas_por_nivel[nivel1]:
                        for ngrama2 in ngramas_por_nivel[nivel2]:
                            key = tuple(sorted([ngrama1, ngrama2]))
                            
                            coocurrencias[key]['count'] += 1
                            
                            # Procesar casos de forma segura
                            caso_str = grupo.iloc[0]['Caso']
                            if pd.notna(caso_str):
                                coocurrencias[key]['casos'].update(procesar_columna_casos(caso_str))
                            
                            # Procesar fuente de forma segura
                            fuente = grupo.iloc[0]['Fuente']
                            if pd.notna(fuente) and str(fuente).strip():
                                coocurrencias[key]['fuentes'].add(str(fuente).strip())
    
    except Exception as e:
        print(f"⚠️  Error procesando co-ocurrencias débiles: {e}")
        return {}
    
    return dict(coocurrencias)

def crear_dataframe_coocurrencias(coocurrencias_dict, df_freq_global):
    """
    Convierte diccionario de co-ocurrencias a DataFrame con porcentajes.
    """
    if not coocurrencias_dict:
        print("   ⚠️  No hay co-ocurrencias para procesar")
        return pd.DataFrame()
    
    data = []
    
    # Obtener lista de casos y fuentes únicos del Excel
    todos_los_casos = set()
    todos_las_fuentes = set()
    
    try:
        for casos_str in df_freq_global['Casos donde aparece']:
            if pd.notna(casos_str):
                todos_los_casos.update([c.strip() for c in str(casos_str).split(',')])
        
        for fuentes_str in df_freq_global['Fuentes donde aparece']:
            if pd.notna(fuentes_str):
                todos_las_fuentes.update([f.strip() for f in str(fuentes_str).split(',')])
    
    except Exception as e:
        print(f"   ⚠️  Error extrayendo casos/fuentes: {e}")
        todos_los_casos = set()
        todos_las_fuentes = set()
    
    casos_sorted = sorted(list(todos_los_casos))
    fuentes_sorted = sorted(list(todos_las_fuentes))
    
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
        
        # Agregar porcentajes por caso (si hay casos definidos)
        if casos_sorted:
            total_casos_unicos = len(todos_los_casos)
            for caso in casos_sorted:
                count_caso = sum(1 for c in info['casos'] if str(c) == str(caso))
                pct = (count_caso / info['count'] * 100) if info['count'] > 0 else 0
                fila[f'% Caso {caso}'] = f"{pct:.1f}%"
        
        # Agregar porcentajes por fuente (si hay fuentes definidas)
        if fuentes_sorted and info['fuentes']:
            for fuente in fuentes_sorted:
                count_fuente = sum(1 for f in info['fuentes'] if str(f) == str(fuente))
                pct = (count_fuente / len(info['fuentes']) * 100) if info['fuentes'] else 0
                fila[f'% Fuente {fuente}'] = f"{pct:.1f}%"
        
        data.append(fila)
    
    return pd.DataFrame(data)

def crear_red(coocurrencias_dict, df_freq_global, titulo):
    """
    Crea un grafo NetworkX visualizando co-ocurrencias.
    """
    G = nx.Graph()
    
    # Agregar nodos (n-gramas) con atributos
    if df_freq_global is not None and len(df_freq_global) > 0:
        for _, row in df_freq_global.iterrows():
            ngrama = row['N-grama']
            freq = row['Frecuencia Total']
            num_casos = row['Num Casos']
            G.add_node(ngrama, freq=freq, num_casos=num_casos)
    
    # Agregar aristas (co-ocurrencias)
    for (ngrama1, ngrama2), info in coocurrencias_dict.items():
        if ngrama1 in G.nodes() and ngrama2 in G.nodes():
            G.add_edge(ngrama1, ngrama2, weight=info['count'])
    
    return G

def visualizar_red(G, titulo, archivo_salida, num_casos_total):
    """
    Visualiza la red y la guarda como imagen.
    num_casos_total: número total de casos para calcular porcentaje
    """
    if len(G.nodes()) == 0:
        print(f"   ⚠️  No hay nodos para visualizar en '{titulo}'")
        return
    
    try:
        plt.figure(figsize=(16, 12))
        
        # Layout de fuerza (spring layout)
        pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
        
        # Calcular tamaño de nodos basado en frecuencia
        node_sizes = [max(G.nodes[node].get('freq', 1) * 10, 100) for node in G.nodes()]
        
        # Calcular color de nodos basado en % casos cubiertos
        node_colors = []
        for node in G.nodes():
            num_casos = G.nodes[node].get('num_casos', 0)
            pct = (num_casos / num_casos_total * 100) if num_casos_total > 0 else 0
            node_colors.append(pct)
        
        # Calcular grosor de aristas basado en peso
        edge_widths = [G[u][v].get('weight', 1) * 0.5 for u, v in G.edges()]
        
        # Dibujar red
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
        
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(archivo_salida) if os.path.dirname(archivo_salida) else ".", exist_ok=True)
        
        plt.savefig(archivo_salida, dpi=300, bbox_inches='tight')
        print(f"   ✓ Gráfico guardado: {archivo_salida}")
        plt.close()
    
    except Exception as e:
        print(f"   ❌ Error generando gráfico: {e}")
        plt.close()

def obtener_numero_casos_total(df_freq_global):
    """
    Extrae dinámicamente el número total de casos del DataFrame.
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
    
    return 16  # Valor por defecto

def main():
    print("=" * 80)
    print("SCRIPT 2: Análisis de co-ocurrencias y visualización")
    print("=" * 80)
    
    # Verificar que el archivo existe
    if not os.path.exists(ARCHIVO_ENTRADA):
        print(f"❌ Error: No se encontró {ARCHIVO_ENTRADA}")
        print(f"   Ejecuta primero: python scripts/01_limpiar_y_extraer_ngramas.py")
        return
    
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
    
    if len(df_detallado) == 0:
        print("⚠️  ADVERTENCIA: La hoja 'Registro Detallado' está vacía")
        print("   No se pueden calcular co-ocurrencias")
        return
    
    print(f"   ✓ {len(df_freq_global)} n-gramas leídos")
    print(f"   ✓ {len(df_detallado)} registros detallados leídos")
    
    # Calcular número de casos únicos (dinámicamente)
    num_casos_total = obtener_numero_casos_total(df_freq_global)
    print(f"   ✓ Número total de casos: {num_casos_total}")
    
    # Calcular co-ocurrencias
    print(f"\n🔄 Calculando co-ocurrencias FUERTES (misma columna)...")
    coocurrencias_fuertes = calcular_coocurrencias_fuertes(df_detallado)
    print(f"   ✓ {len(coocurrencias_fuertes)} co-ocurrencias encontradas")
    
    print(f"\n🔄 Calculando co-ocurrencias DÉBILES (diferente columna)...")
    coocurrencias_debiles = calcular_coocurrencias_debiles(df_detallado)
    print(f"   ✓ {len(coocurrencias_debiles)} co-ocurrencias encontradas")
    
    if len(coocurrencias_fuertes) == 0 and len(coocurrencias_debiles) == 0:
        print("\n⚠️  ADVERTENCIA: No se encontraron co-ocurrencias")
        print("   Verifica que los datos en 'Registro Detallado' son válidos")
        return
    
    # Crear DataFrames
    print(f"\n📝 Generando Excel de co-ocurrencias...")
    df_fuertes = crear_dataframe_coocurrencias(coocurrencias_fuertes, df_freq_global)
    df_debiles = crear_dataframe_coocurrencias(coocurrencias_debiles, df_freq_global)
    
    # Escribir Excel
    try:
        os.makedirs(os.path.dirname(ARCHIVO_SALIDA_COOCURRENCIAS) if os.path.dirname(ARCHIVO_SALIDA_COOCURRENCIAS) else ".", exist_ok=True)
        
        with pd.ExcelWriter(ARCHIVO_SALIDA_COOCURRENCIAS, engine='openpyxl') as writer:
            if len(df_fuertes) > 0:
                df_fuertes.to_excel(writer, sheet_name='Co-ocurrencias Fuertes', index=False)
                print(f"   ✓ Hoja 'Co-ocurrencias Fuertes' ({len(df_fuertes)} filas)")
            else:
                print(f"   ⚠️  Hoja 'Co-ocurrencias Fuertes' vacía (0 filas)")
            
            if len(df_debiles) > 0:
                df_debiles.to_excel(writer, sheet_name='Co-ocurrencias Débiles', index=False)
                print(f"   ✓ Hoja 'Co-ocurrencias Débiles' ({len(df_debiles)} filas)")
            else:
                print(f"   ⚠️  Hoja 'Co-ocurrencias Débiles' vacía (0 filas)")
        
        print(f"   ✓ {ARCHIVO_SALIDA_COOCURRENCIAS}")
    
    except Exception as e:
        print(f"   ❌ Error escribiendo Excel: {e}")
        return
    
    # Crear gráficos
    print(f"\n📊 Generando gráficos de redes...")
    
    if len(coocurrencias_fuertes) > 0:
        G_fuerte = crear_red(coocurrencias_fuertes, df_freq_global, "Red de Co-ocurrencias FUERTES")
        visualizar_red(G_fuerte, "Red de Co-ocurrencias FUERTES (misma columna)", GRAFICO_FUERTE, num_casos_total)
    else:
        print("   ⚠️  No hay co-ocurrencias fuertes para graficar")
    
    if len(coocurrencias_debiles) > 0:
        G_debil = crear_red(coocurrencias_debiles, df_freq_global, "Red de Co-ocurrencias DÉBILES")
        visualizar_red(G_debil, "Red de Co-ocurrencias DÉBILES (diferente columna)", GRAFICO_DEBIL, num_casos_total)
    else:
        print("   ⚠️  No hay co-ocurrencias débiles para graficar")
    
    print(f"\n✅ Proceso completado exitosamente")
    print(f"   📁 Salidas:")
    print(f"      - {ARCHIVO_SALIDA_COOCURRENCIAS}")
    if len(coocurrencias_fuertes) > 0:
        print(f"      - {GRAFICO_FUERTE}")
    if len(coocurrencias_debiles) > 0:
        print(f"      - {GRAFICO_DEBIL}")
    print("=" * 80)

if __name__ == "__main__":
    main()
