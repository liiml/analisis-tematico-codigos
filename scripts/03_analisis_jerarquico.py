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
ARCHIVO_SALIDA = "resultados/03_analisis_jerarquico.xlsx"
GRAFICO_JERARQUICO_1 = "resultados/red_jerarquica_seleccionados_1.png"
GRAFICO_JERARQUICO_2 = "resultados/red_jerarquica_seleccionados_2.png"

def leer_seleccionados_con_jerarquia(archivo, sheet_name):
    """
    Lee hoja de seleccionados y extrae relaciones jerárquicas.
    Retorna lista de diccionarios con jerarquía.
    """
    try:
        df = pd.read_excel(archivo, sheet_name=sheet_name)
        jerarquias = []
        
        for idx, row in df.iterrows():
            ngrama_1 = row.get('N-Grama [1]', '')
            ngrama_2 = row.get('N-Grama [2]', '')
            ngrama_3 = row.get('N-Grama [3]', '')
            
            # Convertir NaN a None
            if pd.isna(ngrama_1):
                ngrama_1 = None
            else:
                ngrama_1 = str(ngrama_1).strip()
            
            if pd.isna(ngrama_2):
                ngrama_2 = None
            else:
                ngrama_2 = str(ngrama_2).strip()
            
            if pd.isna(ngrama_3):
                ngrama_3 = None
            else:
                ngrama_3 = str(ngrama_3).strip()
            
            # Obtener metadatos si están disponibles
            freq = 0
            if 'Frecuencia Total' in df.columns:
                freq_val = row.get('Frecuencia Total', 0)
                if pd.notna(freq_val):
                    freq = int(freq_val) if isinstance(freq_val, (int, float)) else 0
            
            pct_casos = '0%'
            if '% Casos' in df.columns:
                pct_val = row.get('% Casos', '0%')
                if pd.notna(pct_val):
                    pct_casos = str(pct_val).strip()
            
            jerarquias.append({
                'nivel_1': ngrama_1,
                'nivel_2': ngrama_2,
                'nivel_3': ngrama_3,
                'frecuencia': freq,
                'pct_casos': pct_casos
            })
        
        return jerarquias
    
    except Exception as e:
        print(f"   ⚠️  Error leyendo {sheet_name}: {e}")
        return []

def crear_grafo_jerarquico(jerarquias):
    """
    Crea grafo dirigido con estructura jerárquica.
    Nivel 1 → Nivel 2 → Nivel 3
    """
    G = nx.DiGraph()
    
    for jer in jerarquias:
        # Agregar nodos
        if jer.get('nivel_1'):
            G.add_node(jer['nivel_1'], level=1, tipo='principal', freq=jer.get('frecuencia', 0))
        
        if jer.get('nivel_2'):
            G.add_node(jer['nivel_2'], level=2, tipo='secundario')
        
        if jer.get('nivel_3'):
            G.add_node(jer['nivel_3'], level=3, tipo='terciario')
        
        # Agregar aristas (relaciones padre-hijo)
        if jer.get('nivel_1') and jer.get('nivel_2'):
            G.add_edge(jer['nivel_1'], jer['nivel_2'], relation='principal_secundario')
        
        if jer.get('nivel_2') and jer.get('nivel_3'):
            G.add_edge(jer['nivel_2'], jer['nivel_3'], relation='secundario_terciario')
    
    return G

def visualizar_jerarquia(G, titulo, archivo_salida):
    """Visualiza la estructura jerárquica."""
    if len(G.nodes()) == 0:
        print(f"   ⚠️  No hay nodos para visualizar")
        return
    
    try:
        plt.figure(figsize=(18, 12))
        
        # Usar layout jerárquico (spring layout mejorado)
        pos = nx.spring_layout(G, k=3, iterations=50, seed=42)
        
        # Colorear por nivel
        node_colors = []
        color_map = {1: '#FF6B6B', 2: '#4ECDC4', 3: '#45B7D1'}
        for node in G.nodes():
            level = G.nodes[node].get('level', 1)
            node_colors.append(color_map.get(level, '#95E1D3'))
        
        # Tamaño de nodo por nivel
        node_sizes = []
        size_map = {1: 3000, 2: 2000, 3: 1500}
        for node in G.nodes():
            level = G.nodes[node].get('level', 1)
            node_sizes.append(size_map.get(level, 1500))
        
        # Dibujar grafo
        nx.draw_networkx_nodes(
            G, pos,
            node_size=node_sizes,
            node_color=node_colors,
            alpha=0.9
        )
        
        nx.draw_networkx_edges(
            G, pos,
            edge_color='gray',
            arrows=True,
            arrowsize=20,
            arrowstyle='->',
            width=2,
            alpha=0.6,
            connectionstyle='arc3,rad=0.1'
        )
        
        nx.draw_networkx_labels(
            G, pos,
            font_size=8,
            font_weight='bold'
        )
        
        plt.title(titulo, fontsize=16, fontweight='bold')
        
        # Leyenda
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='#FF6B6B', label='Nivel 1: Principal (≥50% casos)'),
            Patch(facecolor='#4ECDC4', label='Nivel 2: Secundario'),
            Patch(facecolor='#45B7D1', label='Nivel 3: Terciario')
        ]
        plt.legend(handles=legend_elements, loc='upper left')
        
        plt.axis('off')
        plt.tight_layout()
        
        os.makedirs(os.path.dirname(archivo_salida) if os.path.dirname(archivo_salida) else ".", exist_ok=True)
        plt.savefig(archivo_salida, dpi=300, bbox_inches='tight')
        print(f"   ✓ Gráfico guardado: {archivo_salida}")
        plt.close()
    
    except Exception as e:
        print(f"   ❌ Error visualizando jerarquía: {e}")
        plt.close()

def crear_matriz_relaciones_jerarquicas(jerarquias):
    """
    Crea matriz que muestra relaciones padre-hijo.
    """
    data = []
    
    for jer in jerarquias:
        data.append({
            'N-Grama Principal (1)': jer.get('nivel_1', ''),
            'N-Grama Secundario (2)': jer.get('nivel_2', ''),
            'N-Grama Terciario (3)': jer.get('nivel_3', ''),
            'Frecuencia': jer.get('frecuencia', 0),
            '% Casos': jer.get('pct_casos', '0%')
        })
    
    return pd.DataFrame(data)

def main():
    print("=" * 80)
    print("SCRIPT 3: Análisis Jerárquico de N-Gramas")
    print("=" * 80)
    
    # Verificar que el archivo existe
    if not os.path.exists(ARCHIVO_ENTRADA):
        print(f"❌ Error: No se encontró {ARCHIVO_ENTRADA}")
        return
    
    # Leer jerarquías de seleccionados_1
    print(f"\n📋 Leyendo jerarquías de Seleccionados_1...")
    jerarquias_1 = leer_seleccionados_con_jerarquia(ARCHIVO_ENTRADA, 'seleccionados_1')
    print(f"   ✓ {len(jerarquias_1)} jerarquías leídas")
    
    # Leer jerarquías de seleccionados_2
    print(f"\n📋 Leyendo jerarquías de Seleccionados_2...")
    jerarquias_2 = leer_seleccionados_con_jerarquia(ARCHIVO_ENTRADA, 'seleccionados_2')
    print(f"   ✓ {len(jerarquias_2)} jerarquías leídas")
    
    if len(jerarquias_1) == 0 and len(jerarquias_2) == 0:
        print("❌ No se encontraron jerarquías en las hojas de seleccionados")
        return
    
    # Crear grafos jerárquicos
    print(f"\n🌳 Creando estructuras jerárquicas...")
    G_1 = crear_grafo_jerarquico(jerarquias_1)
    G_2 = crear_grafo_jerarquico(jerarquias_2)
    
    print(f"   ✓ Grafo Seleccionados_1: {len(G_1.nodes())} nodos, {len(G_1.edges())} aristas")
    print(f"   ✓ Grafo Seleccionados_2: {len(G_2.nodes())} nodos, {len(G_2.edges())} aristas")
    
    # Crear DataFrames para Excel
    print(f"\n📝 Generando matrices de relaciones...")
    df_jerarquias_1 = crear_matriz_relaciones_jerarquicas(jerarquias_1)
    df_jerarquias_2 = crear_matriz_relaciones_jerarquicas(jerarquias_2)
    
    # Escribir Excel
    print(f"   ✓ Escribiendo {ARCHIVO_SALIDA}...")
    
    try:
        os.makedirs(os.path.dirname(ARCHIVO_SALIDA) if os.path.dirname(ARCHIVO_SALIDA) else ".", exist_ok=True)
        
        with pd.ExcelWriter(ARCHIVO_SALIDA, engine='openpyxl') as writer:
            if len(df_jerarquias_1) > 0:
                df_jerarquias_1.to_excel(writer, sheet_name='Jerarquía Seleccionados_1', index=False)
                print(f"      ✓ Hoja 'Jerarquía Seleccionados_1' ({len(df_jerarquias_1)} filas)")
            
            if len(df_jerarquias_2) > 0:
                df_jerarquias_2.to_excel(writer, sheet_name='Jerarquía Seleccionados_2', index=False)
                print(f"      ✓ Hoja 'Jerarquía Seleccionados_2' ({len(df_jerarquias_2)} filas)")
    
    except Exception as e:
        print(f"   ❌ Error escribiendo Excel: {e}")
        return
    
    # Visualizar grafos jerárquicos
    print(f"\n📊 Generando visualizaciones jerárquicas...")
    
    if len(G_1.nodes()) > 0:
        visualizar_jerarquia(G_1, "Estructura Jerárquica - Seleccionados_1 (≥50% casos)", GRAFICO_JERARQUICO_1)
    
    if len(G_2.nodes()) > 0:
        visualizar_jerarquia(G_2, "Estructura Jerárquica - Seleccionados_2 (<50% casos)", GRAFICO_JERARQUICO_2)
    
    print(f"\n✅ Análisis jerárquico completado")
    print(f"   📁 Salidas:")
    print(f"      - {ARCHIVO_SALIDA}")
    if len(G_1.nodes()) > 0:
        print(f"      - {GRAFICO_JERARQUICO_1}")
    if len(G_2.nodes()) > 0:
        print(f"      - {GRAFICO_JERARQUICO_2}")
    print("=" * 80)

if __name__ == "__main__":
    main()
