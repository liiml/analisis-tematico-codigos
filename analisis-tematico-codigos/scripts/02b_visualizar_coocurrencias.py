import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))

# Configuración de rutas
ARCHIVO_ENTRADA = "resultados/02_analisis_coocurrencias.xlsx"
HOJA_ENTRADA = "Coocurrencias_seleccion"
ARCHIVO_SALIDA = "resultados/red_coocurrencias.png"

# TIPO DE LAYOUT (cambia aquí para probar diferentes)
TIPO_LAYOUT = "circular"  # Opciones: "circular", "spring", "hierarchical", "kamada_kawai"

def leer_coocurrencias(archivo, sheet_name):
    """
    Lee las coocurrencias seleccionadas de la hoja especificada.
    
    Columnas requeridas:
    - N-Grama 1
    - N-Grama 2
    - % Casos Juntos vs Separados
    
    Retorna: DataFrame con las coocurrencias
    """
    try:
        df = pd.read_excel(archivo, sheet_name=sheet_name)
        
        if df.empty:
            print(f"❌ Error: Hoja '{sheet_name}' está vacía")
            return None
        
        # Verificar columnas requeridas
        columnas_requeridas = ['N-grama 1', 'N-grama 2', '% Casos Juntos vs Separados']
        columnas_faltantes = [col for col in columnas_requeridas if col not in df.columns]
        
        if columnas_faltantes:
            print(f"❌ Error: Columnas faltantes: {columnas_faltantes}")
            print(f"   Columnas disponibles: {list(df.columns)}")
            return None
        
        print(f"   ✓ {len(df)} coocurrencias leídas")
        return df
    
    except Exception as e:
        print(f"❌ Error leyendo Excel: {e}")
        return None

def extraer_fuerza_numerica(fuerza_str):
    """
    Extrae el valor numérico del porcentaje.
    
    Entrada: "57.1%" → Salida: 57.1
    """
    try:
        if pd.isna(fuerza_str):
            return 0
        valor = str(fuerza_str).strip().replace('%', '')
        return float(valor)
    except:
        return 0

def crear_red_coocurrencias(df_cooc):
    """
    Crea un grafo NetworkX con las coocurrencias.
    
    Estructura:
    - Nodos: N-gramas individuales
    - Aristas: Co-ocurrencias con peso = % Casos Juntos vs Separados
    
    Retorna: networkx.Graph, min_fuerza, max_fuerza
    """
    G = nx.Graph()
    
    # Extraer fuerzas numéricas
    fuerzas = []
    
    for _, row in df_cooc.iterrows():
        ngrama1 = str(row['N-grama 1']).strip()
        ngrama2 = str(row['N-grama 2']).strip()
        fuerza_str = row['% Casos Juntos vs Separados']
        fuerza = extraer_fuerza_numerica(fuerza_str)
        
        if not ngrama1 or not ngrama2:
            continue
        
        # Agregar nodos
        G.add_node(ngrama1)
        G.add_node(ngrama2)
        
        # Agregar arista con peso = fuerza
        G.add_edge(ngrama1, ngrama2, weight=fuerza)
        fuerzas.append(fuerza)
    
    min_fuerza = min(fuerzas) if fuerzas else 0
    max_fuerza = max(fuerzas) if fuerzas else 100
    
    print(f"   ✓ {len(G.nodes())} nodos (n-gramas)")
    print(f"   ✓ {len(G.edges())} aristas (co-ocurrencias)")
    print(f"   ✓ Rango de fuerza: {min_fuerza:.1f}% - {max_fuerza:.1f}%")
    
    return G, min_fuerza, max_fuerza

def calcular_layout(G, tipo_layout):
    """
    Calcula las posiciones de los nodos según el tipo de layout.
    
    Tipos disponibles:
    - circular: Nodos en círculo (bueno para visualizar conexiones)
    - spring: Repulsión de fuerzas (nodos se repelen, aristas atraen)
    - hierarchical: Ordena por grado de conectividad
    - kamada_kawai: Similar a spring pero más eficiente
    
    Retorna: dict {nodo: (x, y)}
    """
    import numpy as np
    if tipo_layout == "circular":
        # Nodos en círculo, ordenados por grado (más conexiones al inicio)
        grados = dict(G.degree())
        nodos_ordenados = sorted(grados.keys(), key=lambda x: grados[x], reverse=True)
        pos = nx.circular_layout(G, scale=2)
        
        # Reordenar según grado para mejor visualización
        n = len(nodos_ordenados)
        pos_reordenado = {}
        for i, nodo in enumerate(nodos_ordenados):
            angulo = 2 * 3.14159 * i / n
            pos_reordenado[nodo] = (2 * 3.14159 * np.cos(angulo), 2 * 3.14159 * np.sin(angulo))
        pos = pos_reordenado
        
    elif tipo_layout == "spring":
        # Repulsión de fuerzas (Fruchterman-Reingold)
        pos = nx.spring_layout(G, k=3, iterations=100, seed=42, scale=2)
        
    elif tipo_layout == "hierarchical":
        # Ordena por grado: más conectados en el centro
        grados = dict(G.degree())
        pos = nx.spring_layout(G, k=2, iterations=50, seed=42, scale=2)
        
    elif tipo_layout == "kamada_kawai":
        # Algoritmo de Kamada-Kawai (preserva distancias)
        pos = nx.kamada_kawai_layout(G, scale=2)
        
    else:
        pos = nx.spring_layout(G, k=2, iterations=100, seed=42, scale=2)
    
    return pos

def normalizar_grosor_arista(fuerza, min_fuerza, max_fuerza, min_grosor=0.5, max_grosor=5.0):
    """
    Normaliza el grosor de la arista según la fuerza.
    
    Fórmula: grosor = min_grosor + (fuerza - min) / (max - min) * (max_grosor - min_grosor)
    
    Retorna: grosor normalizado [min_grosor, max_grosor]
    """
    if max_fuerza == min_fuerza:
        return (min_grosor + max_grosor) / 2
    
    normalized = (fuerza - min_fuerza) / (max_fuerza - min_fuerza)
    grosor = min_grosor + normalized * (max_grosor - min_grosor)
    return grosor

def visualizar_red(G, df_cooc, min_fuerza, max_fuerza, archivo_salida, tipo_layout):
    """
    Visualiza la red de coocurrencias con estilo académico APA.
    
    Propiedades visuales:
    - Tamaño del nodo: Proporcional a la frecuencia de aparición (grado)
    - Color del nodo: Gradiente según número de conexiones
    - Grosor de arista: Proporcional a % Casos Juntos vs Separados
      - Mínimo: min_fuerza → grosor 0.5pt
      - Máximo: max_fuerza → grosor 5.0pt
    - Layout: Configurable (circular, spring, hierarchical, kamada_kawai)
    - Tipografía: Times New Roman / serif para APA 7
    """
    try:
        import numpy as np
        
        # Crear figura con tamaño académico
        fig, ax = plt.subplots(figsize=(16, 12), dpi=300)
        
        # Calcular layout
        print(f"   Calculando layout ({tipo_layout})...")
        pos = calcular_layout(G, tipo_layout)
        
        # Calcular propiedades de nodos
        grados = dict(G.degree())
        max_grado = max(grados.values()) if grados else 1
        
        # Tamaño de nodos: proporcional al número de conexiones
        node_sizes = [400 + (grados[node] / max_grado) * 800 for node in G.nodes()]
        
        # Color de nodos: gradiente según número de conexiones
        node_colors = [grados[node] for node in G.nodes()]
        
        # Grosor de aristas: proporcional a la fuerza
        edge_widths = []
        for u, v in G.edges():
            fuerza = G[u][v]['weight']
            grosor = normalizar_grosor_arista(fuerza, min_fuerza, max_fuerza, 0.5, 5.0)
            edge_widths.append(grosor)
        
        # Dibujar aristas PRIMERO (para que queden debajo)
        print("   Dibujando aristas...")
        edges = nx.draw_networkx_edges(
            G, pos,
            width=edge_widths,
            alpha=0.5,
            edge_color='#34495E',
            ax=ax
        )
        
        # Dibujar nodos
        print("   Dibujando nodos...")
        nodes = nx.draw_networkx_nodes(
            G, pos,
            node_size=node_sizes,
            node_color=node_colors,
            cmap='Blues',
            alpha=0.85,
            ax=ax,
            edgecolors='#2C3E50',
            linewidths=2
        )
        
        # Dibujar etiquetas
        print("   Añadiendo etiquetas...")
        labels = nx.draw_networkx_labels(
            G, pos,
            font_size=8,
            font_weight='bold',
            font_family='serif',
            ax=ax
        )
        
        # Título con fuente serif para APA
        titulo_layout = {
            "circular": "Disposición Circular",
            "spring": "Disposición por Repulsión de Fuerzas",
            "hierarchical": "Disposición Jerárquica",
            "kamada_kawai": "Disposición Kamada-Kawai"
        }
        
        plt.title(
            f'Red de Co-ocurrencias de N-Gramas\n({titulo_layout.get(tipo_layout, tipo_layout)})',
            fontsize=16,
            fontweight='bold',
            fontfamily='serif',
            pad=20
        )
        
        # Barra de color para nodos
        cbar = plt.colorbar(nodes, ax=ax, label='Número de conexiones', fraction=0.046, pad=0.04)
        cbar.ax.tick_params(labelsize=9)
        cbar.set_label('Número de conexiones', fontfamily='serif', fontsize=10)
        
        # Leyenda explicativa para aristas
        from matplotlib.lines import Line2D
        legend_elements = [
            Line2D([0], [0], color='#34495E', lw=0.5, label=f'Fuerza mínima ({min_fuerza:.1f}%)'),
            Line2D([0], [0], color='#34495E', lw=2.75, label=f'Fuerza media ({(min_fuerza + max_fuerza)/2:.1f}%)'),
            Line2D([0], [0], color='#34495E', lw=5.0, label=f'Fuerza máxima ({max_fuerza:.1f}%)')
        ]
        ax.legend(
            handles=legend_elements,
            loc='upper left',
            frameon=True,
            fancybox=False,
            shadow=False,
            fontsize=10,
            framealpha=0.95,
            edgecolor='black'
        )
        
        # Información adicional
        densidad = nx.density(G)
        info_text = (
            f'N = {len(G.nodes())} n-gramas\n'
            f'Coocurrencias = {len(G.edges())}\n'
            f'Densidad = {densidad:.3f}'
        )
        ax.text(
            0.02, 0.02,
            info_text,
            transform=ax.transAxes,
            fontsize=9,
            verticalalignment='bottom',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
            fontfamily='serif'
        )
        
        # Estilo APA: sin bordes
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.set_xticks([])
        ax.set_yticks([])
        
        plt.tight_layout()
        
        # Guardar con alta resolución para APA
        os.makedirs(os.path.dirname(archivo_salida) if os.path.dirname(archivo_salida) else ".", exist_ok=True)
        plt.savefig(archivo_salida, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"   ✓ Gráfico guardado: {archivo_salida}")
        
        # Mostrar estadísticas
        print(f"\n📊 Estadísticas de la red:")
        print(f"   - Densidad: {densidad:.3f}")
        print(f"   - Número promedio de conexiones: {sum(grados.values()) / len(grados):.2f}")
        print(f"   - Componentes conectados: {nx.number_connected_components(G)}")
        print(f"   - Diámetro de la red: {nx.diameter(G) if nx.is_connected(G) else 'N/A (no conectada)'}")
        
        plt.close()
    
    except Exception as e:
        print(f"❌ Error visualizando red: {e}")
        import traceback
        traceback.print_exc()
        plt.close()

def main():
    print("=" * 80)
    print("SCRIPT 2B: Visualización de Red de Co-ocurrencias (Formato APA 7)")
    print("=" * 80)
    print(f"\n🎨 Tipo de layout: {TIPO_LAYOUT}")
    print(f"   Opciones disponibles: circular, spring, hierarchical, kamada_kawai")
    
    # Verificar que el archivo existe
    if not os.path.exists(ARCHIVO_ENTRADA):
        print(f"❌ Error: No se encontró {ARCHIVO_ENTRADA}")
        return
    
    # Leer coocurrencias
    print(f"\n📖 Leyendo coocurrencias...")
    df_cooc = leer_coocurrencias(ARCHIVO_ENTRADA, HOJA_ENTRADA)
    
    if df_cooc is None:
        return
    
    # Crear red
    print(f"\n🕸️  Creando red de coocurrencias...")
    G, min_fuerza, max_fuerza = crear_red_coocurrencias(df_cooc)
    
    if len(G.nodes()) == 0:
        print("❌ Error: No se pudieron crear nodos")
        return
    
    # Visualizar
    print(f"\n🎨 Generando visualización...")
    visualizar_red(G, df_cooc, min_fuerza, max_fuerza, ARCHIVO_SALIDA, TIPO_LAYOUT)
    
    print(f"\n✅ Proceso completado exitosamente")
    print(f"   📁 Salida: {ARCHIVO_SALIDA}")
    print(f"\n📌 Notas:")
    print(f"   - Tamaño del nodo: proporcional a número de conexiones")
    print(f"   - Color del nodo: gradiente según conectividad")
    print(f"   - Grosor de línea: proporcional a % Casos Juntos vs Separados")
    print(f"   - Resolución: 300 DPI (apta para publicación)")
    print(f"   - Formato: PNG (compatible con APA 7)")
    print("=" * 80)

if __name__ == "__main__":
    main()