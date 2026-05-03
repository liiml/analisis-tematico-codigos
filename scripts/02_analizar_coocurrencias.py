import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os
from collections import defaultdict
from utils import procesar_columna_casos

# Configuración de rutas
ARCHIVO_ENTRADA = "datos/procesados/01_ngrams_procesados.xlsx"
ARCHIVO_SALIDA_COOCURRENCIAS = "resultados/02_analisis_coocurrencias.xlsx"
GRAFICO_FUERTE = "resultados/red_temas_fuerte.png"
GRAFICO_DEBIL = "resultados/red_temas_debil.png"

def calcular_coocurrencias_fuertes(df_entrada):
    """
    Calcula co-ocurrencias FUERTES (misma columna, misma fila).
    Retorna lista de tuplas: (ngrama1, ngrama2, frecuencia, casos, fuentes)
    """
    df_detallado = pd.read_excel(ARCHIVO_ENTRADA, sheet_name='Registro Detallado')
    
    coocurrencias = defaultdict(lambda: {'count': 0, 'casos': set(), 'fuentes': set()})
    
    # Agrupar por fila original (misma ID, Caso, Fuente, Nivel)
    for _, grupo in df_detallado.groupby(['ID', 'Caso', 'Fuente', 'Nivel']):
        ngramas = grupo['N-grama'].unique()
        
        # Generar todas las combinaciones de n-gramas en esta fila
        for i, ngrama1 in enumerate(ngramas):
            for ngrama2 in ngramas[i+1:]:
                # Ordenar para evitar duplicados (a,b) y (b,a)
                key = tuple(sorted([ngrama1, ngrama2]))
                
                coocurrencias[key]['count'] += 1
                coocurrencias[key]['casos'].update(procesar_columna_casos(grupo.iloc[0]['Caso']))
                coocurrencias[key]['fuentes'].add(grupo.iloc[0]['Fuente'])
    
    return coocurrencias

def calcular_coocurrencias_debiles(df_entrada):
    """
    Calcula co-ocurrencias DÉBILES (diferentes columnas, misma fila).
    Retorna lista de tuplas: (ngrama1, ngrama2, frecuencia, casos, fuentes)
    """
    df_detallado = pd.read_excel(ARCHIVO_ENTRADA, sheet_name='Registro Detallado')
    
    coocurrencias = defaultdict(lambda: {'count': 0, 'casos': set(), 'fuentes': set()})
    
    # Agrupar por fila original (misma ID, Caso, Fuente)
    for _, grupo in df_detallado.groupby(['ID', 'Caso', 'Fuente']):
        ngramas_por_nivel = defaultdict(list)
        
        # Agrupar n-gramas por nivel
        for _, row in grupo.iterrows():
            nivel = row['Nivel']
            ngrama = row['N-grama']
            ngramas_por_nivel[nivel].append(ngrama)
        
        # Generar co-ocurrencias entre diferentes niveles
        niveles = list(ngramas_por_nivel.keys())
        for i, nivel1 in enumerate(niveles):
            for nivel2 in niveles[i+1:]:
                for ngrama1 in ngramas_por_nivel[nivel1]:
                    for ngrama2 in ngramas_por_nivel[nivel2]:
                        key = tuple(sorted([ngrama1, ngrama2]))
                        
                        coocurrencias[key]['count'] += 1
                        coocurrencias[key]['casos'].update(procesar_columna_casos(grupo.iloc[0]['Caso']))
                        coocurrencias[key]['fuentes'].add(grupo.iloc[0]['Fuente'])
    
    return coocurrencias

def crear_dataframe_coocurrencias(coocurrencias_dict, df_freq_global):
    """
    Convierte diccionario de co-ocurrencias a DataFrame con porcentajes.
    """
    data = []
    
    # Obtener lista de casos y fuentes únicos del Excel
    df_freq = pd.read_excel(ARCHIVO_ENTRADA, sheet_name='Frecuencias Globales')
    
    todos_los_casos = set()
    todos_las_fuentes = set()
    
    for casos_str in df_freq['Casos donde aparece']:
        todos_los_casos.update([c.strip() for c in str(casos_str).split(',')])
    
    for fuentes_str in df_freq['Fuentes donde aparece']:
        todos_las_fuentes.update([f.strip() for f in str(fuentes_str).split(',')])
    
    casos_sorted = sorted(list(todos_los_casos))
    fuentes_sorted = sorted(list(todos_las_fuentes))
    
    for (ngrama1, ngrama2), info in coocurrencias_dict.items():
        fila = {
            'N-grama 1': ngrama1,
            'N-grama 2': ngrama2,
            'Veces juntos': info['count'],
            'Casos donde co-ocurren': ', '.join(sorted(info['casos'])),
            'Fuentes donde co-ocurren': ', '.join(sorted(info['fuentes']))
        }
        
        # Agregar porcentajes por caso
        total = info['count']
        for caso in casos_sorted:
            count_caso = sum(1 for c in info['casos'] if c == caso)
            pct = (count_caso / total * 100) if total > 0 else 0
            fila[f'% {caso}'] = f"{pct:.1f}%"
        
        # Agregar porcentajes por fuente
        for fuente in fuentes_sorted:
            count_fuente = sum(1 for f in info['fuentes'] if f == fuente)
            pct = (count_fuente / len(info['fuentes']) * 100) if info['fuentes'] else 0
            fila[f'% {fuente}'] = f"{pct:.1f}%"
        
        data.append(fila)
    
    return pd.DataFrame(data)

def crear_red(coocurrencias_dict, df_freq_global, titulo):
    """
    Crea un grafo NetworkX visualizando co-ocurrencias.
    """
    G = nx.Graph()
    
    # Agregar nodos (n-gramas) con atributos
    for _, row in df_freq_global.iterrows():
        ngrama = row['N-grama']
        freq = row['Frecuencia Total']
        num_casos = row['Num Casos']
        G.add_node(ngrama, freq=freq, num_casos=num_casos)
    
    # Agregar aristas (co-ocurrencias)
    for (ngrama1, ngrama2), info in coocurrencias_dict.items():
        G.add_edge(ngrama1, ngrama2, weight=info['count'])
    
    return G

def visualizar_red(G, titulo, archivo_salida):
    """
    Visualiza la red y la guarda como imagen.
    """
    plt.figure(figsize=(16, 12))
    
    # Layout de fuerza (spring layout)
    pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
    
    # Calcular tamaño de nodos basado en frecuencia
    node_sizes = [G.nodes[node].get('freq', 1) * 10 for node in G.nodes()]
    
    # Calcular color de nodos basado en % casos cubiertos
    node_colors = []
    for node in G.nodes():
        num_casos = G.nodes[node].get('num_casos', 0)
        # Suponemos que hay 16 casos en total
        pct = (num_casos / 16) * 100
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
    
    plt.savefig(archivo_salida, dpi=300, bbox_inches='tight')
    print(f"   ✓ Gráfico guardado: {archivo_salida}")
    plt.close()

def main():
    print("=" * 80)
    print("SCRIPT 2: Análisis de co-ocurrencias y visualización")
    print("=" * 80)
    
    # Verificar que el archivo existe
    if not os.path.exists(ARCHIVO_ENTRADA):
        print(f"❌ Error: No se encontró {ARCHIVO_ENTRADA}")
        print(f"   Ejecuta primero: python 01_limpiar_y_extraer_ngramas.py")
        return
    
    # Leer datos de entrada
    print(f"\n📖 Leyendo datos procesados...")
    df_freq_global = pd.read_excel(ARCHIVO_ENTRADA, sheet_name='Frecuencias Globales')
    print(f"   ✓ {len(df_freq_global)} n-gramas leídos")
    
    # Calcular co-ocurrencias
    print(f"\n🔄 Calculando co-ocurrencias FUERTES (misma columna)...")
    coocurrencias_fuertes = calcular_coocurrencias_fuertes(df_freq_global)
    print(f"   ✓ {len(coocurrencias_fuertes)} co-ocurrencias encontradas")
    
    print(f"\n🔄 Calculando co-ocurrencias DÉBILES (diferente columna)...")
    coocurrencias_debiles = calcular_coocurrencias_debiles(df_freq_global)
    print(f"   ✓ {len(coocurrencias_debiles)} co-ocurrencias encontradas")
    
    # Crear DataFrames
    print(f"\n📝 Generando Excel de co-ocurrencias...")
    df_fuertes = crear_dataframe_coocurrencias(coocurrencias_fuertes, df_freq_global)
    df_debiles = crear_dataframe_coocurrencias(coocurrencias_debiles, df_freq_global)
    
    # Escribir Excel
    os.makedirs(os.path.dirname(ARCHIVO_SALIDA_COOCURRENCIAS), exist_ok=True)
    
    with pd.ExcelWriter(ARCHIVO_SALIDA_COOCURRENCIAS, engine='openpyxl') as writer:
        df_fuertes.to_excel(writer, sheet_name='Co-ocurrencias Fuertes', index=False)
        df_debiles.to_excel(writer, sheet_name='Co-ocurrencias Débiles', index=False)
    
    print(f"   ✓ {ARCHIVO_SALIDA_COOCURRENCIAS}")
    
    # Crear gráficos
    print(f"\n📊 Generando gráficos de redes...")
    
    G_fuerte = crear_red(coocurrencias_fuertes, df_freq_global, "Red de Co-ocurrencias FUERTES (misma columna)")
    visualizar_red(G_fuerte, "Red de Co-ocurrencias FUERTES", GRAFICO_FUERTE)
    
    G_debil = crear_red(coocurrencias_debiles, df_freq_global, "Red de Co-ocurrencias DÉBILES (diferente columna)")
    visualizar_red(G_debil, "Red de Co-ocurrencias DÉBILES", GRAFICO_DEBIL)
    
    print(f"\n✅ Proceso completado exitosamente")
    print(f"   📁 Salidas:")
    print(f"      - {ARCHIVO_SALIDA_COOCURRENCIAS}")
    print(f"      - {GRAFICO_FUERTE}")
    print(f"      - {GRAFICO_DEBIL}")
    print("=" * 80)

if __name__ == "__main__":
    main()
