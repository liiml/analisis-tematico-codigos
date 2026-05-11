from collections import defaultdict
import unicodedata
import re
import spacy
from typing import List, Set, Tuple
import pandas as pd

# Cargar modelo de spaCy para español
try:
    nlp = spacy.load("es_core_news_sm")
except OSError:
    print("Descargando modelo de spaCy...")
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "es_core_news_sm"])
    nlp = spacy.load("es_core_news_sm")

# Stop-words en español
STOP_WORDS = {
    # Determinantes
    "el", "la", "los", "las", "un", "una", "unos", "unas",
    "este", "esta", "estos", "estas",
    "ese", "esa", "esos", "esas",
    "alguno", "alguna", "algunos", "algunas"
    
    # Preposiciones
    "de", "a", "en", "por", "para", "con", "sin", "entre", "durante",
    "ante", "bajo", "cabe", "desde", "hacia", "hasta", "mediante", "sobre", "tras",
    
    # Conjunciones
    "y", "o", "pero", "mas", "sino", "que", "quien", "como", "si", "aunque",
    "porque", "pues", "luego", "conque", "ni",
    
    # Verbos auxiliares
    "es", "está", "son", "estan", "estoy", "estamos", "estais",
    "ser", "estar", "haber", "he", "has", "ha", "hemos", "habeis", "han",
    "soy", "eres", "somos", "sois",
    
    # Pronombres comunes
    "yo", "tu", "el", "ella", "nosotros", "nosotras", "vosotros", "vosotras",
    "ellos", "ellas", "me", "te", "se", "nos", "os", "mi", "mio", "tuyo",
    "suyo", "nuestro", "vuestro",
    
    # Otros comunes
    "muy", "mas", "menos", "poco", "mucho", "todo", "otro", "mismo",
    "tal", "cual", "cuando", "donde", "cuanto"
}

def quitar_tildes(texto: str) -> str:
    """Elimina tildes y diacríticos del texto."""
    nfkd = unicodedata.normalize('NFKD', texto)
    return ''.join([c for c in nfkd if not unicodedata.combining(c)])

def limpiar_texto(texto: str) -> str:
    """
    Limpia el texto de forma exhaustiva:
    1. Convierte a minúsculas
    2. Quita tildes
    3. Reemplaza TODOS los caracteres especiales por espacios
    4. Normaliza espacios múltiples (repite hasta que no haya dobles)
    5. Trim (quita espacios al inicio y final)
    """
    if not isinstance(texto, str) or pd.isna(texto):
        return ""
    
    # PASO 1: Convertir a minúsculas
    texto = texto.lower()
    
    # PASO 2: Quitar tildes y diacríticos
    texto = quitar_tildes(texto)
    
    # PASO 3: Reemplazar TODOS los caracteres especiales por espacios
    # Solo mantiene: a-z, 0-9 y espacios
    texto = re.sub(r'[^a-z0-9\s]', ' ', texto)
    
    # PASO 4: Normalizar espacios múltiples (repetir hasta que no haya dobles)
    while '  ' in texto:
        texto = texto.replace('  ', ' ')
    
    # PASO 5: Trim
    texto = texto.strip()
    
    return texto

def lematizar_texto(texto: str) -> str:
    """Lematiza el texto usando spaCy."""
    if not texto:
        return ""
    
    doc = nlp(texto)
    lemmas = [token.lemma_ for token in doc]
    return ' '.join(lemmas)

def quitar_stop_words(texto: str) -> str:
    """Elimina stop-words del texto."""
    palabras = texto.split()
    palabras_filtradas = [p for p in palabras if p not in STOP_WORDS]
    
    # Normalizar espacios después de quitar stop-words
    texto_sin_sw = ' '.join(palabras_filtradas)
    
    # Limpiar espacios múltiples si quedaron
    while '  ' in texto_sin_sw:
        texto_sin_sw = texto_sin_sw.replace('  ', ' ')
    
    return texto_sin_sw.strip()

def procesar_texto_completo(texto: str) -> str:
    """Pipeline completo de procesamiento."""
    texto = limpiar_texto(texto)
    texto = lematizar_texto(texto)
    texto = quitar_stop_words(texto)
    return texto

def extraer_ngramas(texto: str, min_n: int = 1, max_n: int = 5) -> List[str]:
    """Extrae n-gramas de un texto."""
    palabras = texto.split()
    
    if not palabras:
        return []
    
    ngramas = set()
    
    for n in range(min_n, min(max_n + 1, len(palabras) + 1)):
        for i in range(len(palabras) - n + 1):
            ngrama = ' '.join(palabras[i:i+n])
            if ngrama.strip():
                ngramas.add(ngrama)
    
    return list(ngramas)

def procesar_columna_casos(casos_str: str) -> List[str]:
    """
    Procesa la columna Caso, separando múltiples valores.
    Maneja separadores: coma (,), punto (.), espacios y combinaciones.
    
    Ejemplos:
    - "10" → ["10"]
    - "10,11" → ["10", "11"]
    - "10.11" → ["10", "11"]
    - "10, 11" → ["10", "11"]
    - "10 11" → ["10", "11"]
    - "10.11, 13" → ["10", "11", "13"]
    """
    if pd.isna(casos_str):
        return []
    
    casos_str = str(casos_str).strip()
    
    if not casos_str:
        return []
    
    # Reemplazar puntos y comas por espacios para separar
    casos_str = casos_str.replace(',', ' ')
    casos_str = casos_str.replace('.', ' ')
    
    # Normalizar espacios múltiples
    casos_str = re.sub(r'\s+', ' ', casos_str)
    
    # Dividir por espacios
    casos_raw = casos_str.split()
    casos = []
    
    for caso in casos_raw:
        caso_limpio = caso.strip()
        if caso_limpio and caso_limpio.isdigit():  # Solo agregar si es número
            casos.append(caso_limpio)
    
    # Eliminar duplicados y ordenar numéricamente
    try:
        casos_ordenados = sorted(list(set(casos)), key=lambda x: int(x))
    except ValueError:
        casos_ordenados = sorted(list(set(casos)))
    
    return casos_ordenados

def crear_contexto(fila: dict, columnas: List[str]) -> str:
    """Crea una cadena de contexto a partir de múltiples columnas."""
    contexto_partes = []
    for col in columnas:
        valor = fila.get(col, "")
        if pd.notna(valor) and str(valor).strip():
            valor_limpio = limpiar_texto(str(valor))
            if valor_limpio:
                contexto_partes.append(f"{col}: {valor_limpio}")
    
    return " | ".join(contexto_partes)
def calcular_coocurrencias_fuertes(df_detallado):
    coocurrencias = defaultdict(lambda: defaultdict(int))
    
    for _, row in df_detallado.iterrows():
        ngrama = row['N-grama']
        caso = row['Caso']
        fuente = row['Fuente']
        nivel = row['Nivel']
        
        # Verificar si el n-grama ya ha aparecido en el mismo nivel y caso
        if (ngrama, nivel, caso) in coocurrencias:
            coocurrencias[(ngrama, nivel, caso)][(fuente, caso)] += 1
        else:
            coocurrencias[(ngrama, nivel, caso)] = defaultdict(int)
            coocurrencias[(ngrama, nivel, caso)][(fuente, caso)] = 1
    
    return coocurrencias

def calcular_coocurrencias_debiles(df_detallado):
    coocurrencias = defaultdict(lambda: defaultdict(int))
    
    for _, row in df_detallado.iterrows():
        ngrama = row['N-grama']
        caso = row['Caso']
        fuente = row['Fuente']
        nivel = row['Nivel']
        
        # Verificar si el n-grama ya ha aparecido en un nivel diferente pero en el mismo caso
        if (ngrama, caso) in coocurrencias:
            coocurrencias[(ngrama, caso)][(nivel, fuente)] += 1
        else:
            coocurrencias[(ngrama, caso)] = defaultdict(int)
            coocurrencias[(ngrama, caso)][(nivel, fuente)] = 1
    
    return coocurrencias