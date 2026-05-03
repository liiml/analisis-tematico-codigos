# Análisis Temático de Códigos: N-gramas y Co-ocurrencias

Sistema automatizado para análisis de etiquetas codificadas usando procesamiento de lenguaje natural, extracción de n-gramas y visualización de redes temáticas.

---

## 📋 Descripción

Este proyecto analiza un archivo Excel con etiquetas codificadas en múltiples niveles (16 casos, 13 fuentes) y:

1. **Limpia y procesa** el texto (lematización, eliminación de tildes, stop-words)
2. **Extrae n-gramas** que se repiten 2+ veces
3. **Calcula co-ocurrencias** dentro de la misma fila (fuertes y débiles)
4. **Genera reportes Excel** con tablas de frecuencias y análisis
5. **Visualiza redes temáticas** como gráficos

---

## 🚀 Instalación

### Requisitos
- Python 3.8+
- pip

### Pasos

1. **Clona o descarga el repositorio**

2. **Instala dependencias**
```bash
pip install -r requirements.txt
python -m spacy download es_core_news_sm
```

3. **Prepara tu Excel**
   - Coloca el archivo `Análisis temático.xlsx` en `datos/brutos/`
   - Asegúrate de que tiene la hoja `Etiquetas`

---

## 📊 Estructura de archivos

```
analisis-tematico-codigos/
├── datos/
│   ├── brutos/                          # Tu Excel original
│   │   └── Análisis temático.xlsx
│   └── procesados/                      # Generado por Script 1
│       └── 01_ngrams_procesados.xlsx
├── scripts/
│   ├── utils.py                         # Funciones compartidas
│   ├── 01_limpiar_y_extraer_ngramas.py # Script 1
│   └── 02_analizar_coocurrencias.py    # Script 2
├── resultados/                          # Generado por Script 2
│   ├── 02_analisis_coocurrencias.xlsx
│   ├── red_temas_fuerte.png
│   └── red_temas_debil.png
├── requirements.txt
└── README.md
```

---

## 🔄 Flujo de ejecución

### Paso 1: Extracción de N-gramas

```bash
python scripts/01_limpiar_y_extraer_ngramas.py
```

**Genera:** `datos/procesados/01_ngrams_procesados.xlsx`

**Hojas:**
- **Frecuencias Globales**: N-grama, frecuencia total, casos/fuentes cubiertos
- **Matriz Casos × Porcentajes**: Desglose por caso + porcentajes
- **Matriz Fuentes × N-gramas**: Desglose por fuente
- **Registro Detallado**: Todas las apariciones con contexto y cita

---

### Paso 2: Análisis de Co-ocurrencias

```bash
python scripts/02_analizar_coocurrencias.py
```

**Genera:** 
- `resultados/02_analisis_coocurrencias.xlsx`
- `resultados/red_temas_fuerte.png`
- `resultados/red_temas_debil.png`

**Hojas:**
- **Co-ocurrencias Fuertes**: Aparecen en la misma columna (más directo)
- **Co-ocurrencias Débiles**: Aparecen en diferentes columnas (más tentativo)

---

## 📖 Especificaciones de procesamiento

### Limpieza de texto
- ✅ Quita caracteres especiales: `[ ] { } -`
- ✅ Convierte a minúsculas
- ✅ Elimina tildes y diacríticos
- ✅ Normaliza espacios

### Lematización
- ✅ Plurales → Singulares
- ✅ Verbos conjugados → Infinitivos
- ✅ Usando spaCy (modelo: `es_core_news_sm`)

### Stop-words eliminados
- Determinantes: el, la, los, las, un, una, unos, unas, este, ese, aquel...
- Preposiciones: de, a, en, por, para, con, sin, entre, durante...
- Conjunciones: y, o, pero, que, quien, como, si...
- Verbos auxiliares: es, está, ser, estar, haber...
- **Con variación de género:** o, a, x (participado, participada, participadx)

### Umbral de repetición
- Mínimo: 2 apariciones (en filas diferentes)
- Máximo: Sin límite
- Casos múltiples: Si Caso="10,11", se cuenta en ambos

---

## 📊 Interpretación de resultados

### Hoja "Frecuencias Globales"
```
N-grama: participación
Frecuencia Total: 245
Casos donde aparece: 1, 3, 5, 8, 12, 14
Num Casos: 6/16 (37.5%)
```
→ **"Participación es un tema presente en 6 de 16 casos"**

### Hoja "Matriz Casos × Porcentajes"
```
N-grama: empoderamiento
Caso 1: 5 (2.6%)
Caso 2: 78 (41.3%)
Caso 3: 12 (6.3%)
```
→ **"Empoderamiento es principalmente característico del Caso 2"**

### Red de Co-ocurrencias
- **Tamaño del nodo**: Frecuencia del n-grama
- **Color del nodo**: % de casos cubiertos (azul=transversal, naranja=específico)
- **Grosor de arista**: Frecuencia de co-ocurrencia

---

## ⚙️ Personalización

### Cambiar umbral de repetición
En `01_limpiar_y_extraer_ngramas.py`, línea ~XX:
```python
if freq >= 2:  # Cambiar aquí
```

### Cambiar stop-words
En `scripts/utils.py`, modifica el conjunto `STOP_WORDS`:
```python
STOP_WORDS = {
    "el", "la", "los", "las",
    # Agregar más...
}
```

### Cambiar rango de n-gramas
En `01_limpiar_y_extraer_ngramas.py`:
```python
ngramas = extraer_ngramas(texto_procesado, min_n=1, max_n=10)
```

---

## 🐛 Troubleshooting

### Error: "No se encontró Análisis temático.xlsx"
→ Verifica que el archivo está en `datos/brutos/` con ese nombre exacto

### Error: "No module named 'spacy'"
→ Ejecuta: `pip install -r requirements.txt`

### Error: "Modelo es_core_news_sm no encontrado"
→ Ejecuta: `python -m spacy download es_core_news_sm`

### Los n-gramas no se ven
→ Verifica que el Excel tiene datos en las columnas de etiquetas
→ Comprueba que los nombres de columnas coinciden en `utils.py`

---

## 📝 Notas

- Los scripts modifican solo archivos de salida; el Excel original no se toca
- Los gráficos se generan con alta resolución (300 dpi)
- Todo el procesamiento es determinista (misma entrada = mismo resultado)

---

## 📧 Soporte

Si encuentras problemas, revisa:
1. Los nombres exactos de columnas en tu Excel
2. Que el Excel tiene datos en todas las columnas esperadas
3. Los logs de ejecución de los scripts

