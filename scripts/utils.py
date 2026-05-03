import unicodedata
import re
import spacy
from typing import List, Set, Tuple

# Cargar modelo de spaCy para español
try:
    nlp = spacy.load("es_core_news_sm")
except OSError:
    print("Descargando modelo de spaCy...")
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "es_core_news_sm"])
    nlp = spacy.load("es_core_news_sm")

# Stop-words en español (determinantes, preposiciones, conjunciones, verbos auxiliares)
# Con variación de género: o, a, x
STOP_WORDS = {
    # Determinantes
    "el", "la", "los", "las", "un", "una", "unos", "unas",
    "este", "esta", "estos", "estas", "estx", "estxs",
    "ese", "esa", "esos", "esas", "esx", "esxs",
    "aquel", "aquella", "aquellos", "aquellas", "aquelx", "aquelxs",
    
    # Preposiciones
    "de", "a", "en", "por", "para", "con", "sin", "entre", "durante",
    "ante", "bajo", "cabe", "desde", "hacia", "hasta", "mediante", "sobre", "tras",
    
    # Conjunciones
    "y", "o", "pero", "mas", "sino", "que", "quien", "como", "si", "aunque",
    "porque", "pues", "luego", "conque", "ni",
    
    # Verbos auxiliares
    "es", "esta", "son", "estan", "estoy", "estamos", "estais",
    "ser", "estar", "haber", "he", "has", "ha", "hemos", "habeis", "han",
    "soy", "eres", "somos", "sois",
    
    # Pronombres comunes
    "yo", "tu", "el", "ella", "nosotros", "nosotras", "vosotros", "vosotras",
    "ellos", "ellas", "me", "te", "se", "nos", "os", "mi", "mio", "tuyo",
    "suyo", "nuestro", "vuestro",
    
    # Otros comunes
    "muy", "mas", "menos", "poco", "mucho", "todo", "otro", "mismo",
    "tal", "cual", "cuando", "donde", "cuanto",
}

def quitar_tildes(texto: str) -> str:
    """Elimina tildes y diacríticos del texto."""
    nfkd = unicodedata.normalize('NFKD', texto)
    return ''.join([c for c in nfkd if not unicodedata.combining(c)])

def limpiar_texto(texto: str) -> str:
    """
    Limpia el texto:
    - Quita caracteres especiales ([ ] { } -)
    - Convierte a minúsculas
    - Quita tildes
    - Normaliza espacios
    """
    if not isinstance(texto, str) or pd.isna(texto):
        return ""
    
    # Quitar caracteres especiales: [ ] { } - etc.
    texto = re.sub(r'[\[\]{}]', ' ', texto)
    texto = re.sub(r'[-–—]', ' ', texto)
    
    # Convertir a minúsculas
    texto = texto.lower()
    
    # Quitar tildes
    texto = quitar_tildes(texto)
    
    # Normalizar espacios múltiples
    texto = re.sub(r'\s+', ' ', texto).strip()
    
    return texto

def lematizar_texto(texto: str) -> str:
    """
    Lematiza el texto usando spaCy.
    Convierte plurales a singulares, verbos conjugados a infinitivos, etc.
    """
    if not texto:
        return ""
    
    doc = nlp(texto)
    lemmas = [token.lemma_ for token in doc]
    return ' '.join(lemmas)

def quitar_stop_words(texto: str) -> str:
    """Elimina stop-words del texto."""
    palabras = texto.split()
    palabras_filtradas = [p for p in palabras if p not in STOP_WORDS]
    return ' '.join(palabras_filtradas)

def procesar_texto_completo(texto: str) -> str:
    """
    Pipeline completo de procesamiento:
    1. Limpieza
    2. Lematización
    3. Quitar stop-words
    """
    texto = limpiar_texto(texto)
    texto = lematizar_texto(texto)
    texto = quitar_stop_words(texto)
    return texto

def extraer_ngramas(texto: str, min_n: int = 1, max_n: int = 5) -> List[str]:
    """
    Extrae n-gramas de un texto.
    min_n: mínimo número de palabras en el n-grama (default: 1)
    max_n: máximo número de palabras en el n-grama (default: 5)
    
    Retorna lista de n-gramas únicos encontrados en el texto.
    """
    palabras = texto.split()
    
    if not palabras:
        return []
    
    ngramas = set()
    
    for n in range(min_n, min(max_n + 1, len(palabras) + 1)):
        for i in range(len(palabras) - n + 1):
            ngrama = ' '.join(palabras[i:i+n])
            # Solo agregar si no es solo stop-words
            if ngrama.strip():
                ngramas.add(ngrama)
    
    return list(ngramas)

def procesar_columna_casos(casos_str: str) -> List[str]:
    """
    Convierte una columna de Caso con posibles múltiples valores.
    Entrada: "10,11" o "5" o "1, 2, 3"
    Salida: ["10", "11"] o ["5"] o ["1", "2", "3"]
    """
    if pd.isna(casos_str):
        return []
    
    casos_str = str(casos_str).strip()
    casos = [c.strip() for c in casos_str.split(',')]
    return [c for c in casos if c]

def crear_contexto(fila: dict, columnas: List[str]) -> str:
    """
    Crea una cadena de contexto a partir de múltiples columnas.
    Entrada: fila (dict), columnas (lista de nombres de columnas)
    Salida: string con formato "Col1: valor1 | Col2: valor2 | ..."
    """
    contexto_partes = []
    for col in columnas:
        valor = fila.get(col, "")
        if pd.notna(valor) and str(valor).strip():
            contexto_partes.append(f"{col}: {valor}")
    
    return " | ".join(contexto_partes)

# Importar pandas al final
import pandas as pd
