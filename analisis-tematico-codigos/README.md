# Análisis Temático de Códigos: N-gramas, Co-ocurrencias y Estructuras Jerárquicas

Sistema automatizado para análisis de etiquetas codificadas usando procesamiento de lenguaje natural, extracción de n-gramas, análisis de coocurrencias y estructuras jerárquicas.

---

## 📋 Descripción General

Este proyecto analiza un archivo Excel con etiquetas codificadas en múltiples niveles y:

1. **Limpia y procesa** el texto (lematización, eliminación de tildes, stop-words)
2. **Extrae n-gramas** únicos que se repiten 2+ veces
3. **Genera selecciones jerárquicas** (n-gramas principales + subordinados por nivel)
4. **Calcula co-ocurrencias** (fuertes y débiles)
5. **Analiza estructuras jerárquicas** con visualizaciones
6. **Genera reportes Excel** con tablas de frecuencias, matrices y análisis
7. **Visualiza redes temáticas** como gráficos de red

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

3. **Estructura de carpetas**
```
proyecto/
├── datos/
│   ├── brutos/
│   │   └── Análisis temático.xlsx       (ENTRADA: tu Excel original)
│   └── procesados/
│       └── 01_ngrams_procesados.xlsx    (SALIDA del Script 1)
├── resultados/
│   ├── 01b_analisis_jerarquico.xlsx     (SALIDA del Script 1B)
│   ├── 02_analisis_coocurrencias.xlsx   (SALIDA del Script 2)
│   └── *.png                            (Gráficos)
├── scripts/
│   ├── 01_limpiar_y_extraer_ngramas.py
│   ├── 01b_analisis_jerarquico.py
│   ├── 02_analizar_coocurrencias.py
│   ├── 02b_visualizar_coocurrencias.py
│   └── utils.py
└── README.md
```

---

## 📊 Flujo de Ejecución

```
PASO 1: 01_limpiar_y_extraer_ngramas.py
  ├─ Lee: datos/brutos/Análisis temático.xlsx
  ├─ Procesa: Limpia texto, extrae n-gramas
  └─ Genera: datos/procesados/01_ngrams_procesados.xlsx
              ├─ Frecuencias Globales
              ├─ Matriz Casos x Porcentajes
              ├─ Matriz Fuentes x N-gramas
              ├─ Registro Detallado
              ├─ Frecuencias_seleccion_1 (vacía para seleccionar)
              └─ Frecuencias_seleccion_2 (vacía para seleccionar)

                        ↓

PASO 2: 01b_analisis_jerarquico.py
  ├─ Lee: Frecuencias_seleccion_1 y _2 del Excel anterior
  ├─ Analiza: Relaciones jerárquicas entre n-gramas
  └─ Genera: resultados/01b_analisis_jerarquico.xlsx
              ├─ Jerarquía Seleccionados_1 (gráfico jerárquico)
              └─ Jerarquía Seleccionados_2 (gráfico jerárquico)

                        ↓

PASO 3: 02_analizar_coocurrencias.py
  ├─ Lee: 01_ngrams_procesados.xlsx (Registro Detallado)
  ├─ Calcula: Co-ocurrencias fuertes y débiles
  └─ Genera: resultados/02_analisis_coocurrencias.xlsx
              ├─ Co-ocurrencias Fuertes
              ├─ Co-ocurrencias Débiles
              ├─ Coocurrencias_seleccion_1 (vacía para seleccionar)
              └─ Coocurrencias_seleccion_2 (vacía para seleccionar)

        [AQUÍ SELECCIONAS MANUALMENTE LAS COOCURRENCIAS]

                        ↓

PASO 4: 02b_visualizar_coocurrencias.py
  ├─ Lee: Coocurrencias_seleccion_1 y _2
  ├─ Genera: Gráficos de redes (PNG)
  └─ Produce: red_coocurrencias_fuerte_seleccion_1.png
              red_coocurrencias_debil_seleccion_1.png
              red_coocurrencias_fuerte_seleccion_2.png
              red_coocurrencias_debil_seleccion_2.png
```

---

## 📈 Variables Calculadas por Script

### **SCRIPT 1: `01_limpiar_y_extraer_ngramas.py`**

#### **Entrada:**
- Archivo: `datos/brutos/Análisis temático.xlsx`
- Columnas requeridas:
  - `ID`: Identificador único
  - `Caso`: Número del caso (ej: 1, 2, 3...)
  - `Fuente`: Origen del dato (ej: Entrevista, Documento...)
  - `Etiqueta [Nivel 1]`: Categoría principal
  - `Etiqueta [Nivel 2]`: Subcategoría
  - `Etiqueta [Nivel 3]`: Subsubcategoría
  - `Caracterización`: Descripción adicional
  - `Cita`: Texto original

#### **Procesamiento:**
1. **Limpieza de texto**:
   - Elimina caracteres especiales: `[ ] { } -`
   - Convierte a minúsculas
   - Quita tildes y diacríticos (café → cafe)
   - Normaliza espacios múltiples

2. **Lematización** (con spaCy):
   - Plurales → Singulares: `códigos` → `código`
   - Verbos conjugados → Infinitivo: `analizar` → `analizar`
   - Adjetivos → Raíz: `rápido` → `rápido`

3. **Eliminación de stop-words**:
   - Determinantes: el, la, los, las, un, una...
   - Preposiciones: de, a, en, por, para, con...
   - Conjunciones: y, o, pero, que...
   - Verbos auxiliares: es, está, son, están...
   - Pronombres: yo, tu, el, ella, nosotros...
   - Otros comunes: muy, más, menos, poco, mucho...

4. **Extracción de n-gramas**:
   - Se extraen todas las combinaciones de 1 a 5 palabras
   - Ejemplo: "análisis temático de códigos" genera:
     - Unigramas: "análisis", "temático", "códigos"
     - Bigramas: "análisis temático", "temático códigos"
     - Trigramas: "análisis temático códigos"
     - etc.

5. **Filtrado**:
   - Solo se conservan n-gramas que aparecen **2+ veces** en todo el dataset

#### **Salida: `01_ngrams_procesados.xlsx`**

**Hoja 1: Frecuencias Globales**

| Variable | Cálculo | Ejemplo | Explicación |
|----------|---------|---------|-------------|
| **N-grama** | Texto procesado | "análisis temático" | El n-grama único identificado |
| **Frecuencia Total** | Conteo directo | 15 | **Número total de veces que aparece** el n-grama en todos los datos (contando cada aparici  n en cada nivel, caso y fuente) |
| **Casos donde aparece** | Lista ÚNICA de casos | "1, 3, 5, 7, 8" | **IDs de los casos** en que el n-grama aparece al menos 1 vez (sin importar cuántas veces) |
| **Num Casos** | Conteo de ÚNICOS | 5 | **Cantidad de casos diferentes** que contienen el n-grama (de 16 total posibles) |
| **Fuentes donde aparece** | Lista ÚNICA de fuentes | "Entrevista, Documento" | **Nombres de las fuentes** donde aparece el n-grama (sin repetir) |
| **Num Fuentes** | Conteo de ÚNICOS | 2 | **Cantidad de fuentes diferentes** que contienen el n-grama |
| **% Casos cubiertos** | (Num Casos / 16) × 100 | 31.3% | **Porcentaje del total de 16 casos** que contienen este n-grama |

**Hoja 2: Matriz Casos × Porcentajes**

| Variable | Cálculo | Ejemplo | Explicación |
|----------|---------|---------|-------------|
| **N-grama** | Identificador | "análisis" | El n-grama |
| **Caso X** | Conteo por caso | 3 | **Número de veces** que el n-grama aparece específicamente en el Caso X |
| **% Caso X** | (Caso X / Frecuencia Total) × 100 | 20% | **Porcentaje de las apariciones totales** que corresponden al Caso X |
| **TOTAL** | Suma de todos los casos | 15 | Equivalente a Frecuencia Total (verificación) |

**Hoja 3: Matriz Fuentes × N-gramas**

| Variable | Cálculo | Ejemplo | Explicación |
|----------|---------|---------|-------------|
| **N-grama** | Identificador | "análisis" | El n-grama |
| **Fuente X** | Conteo por fuente | 5 | **Número de veces** que el n-grama aparece en la Fuente X (ej: Entrevistas) |
| **TOTAL** | Suma de todas las fuentes | 15 | Equivalente a Frecuencia Total (verificación) |

**Hoja 4: Registro Detallado**

| Variable | Tipo | Ejemplo | Explicación |
|----------|------|---------|-------------|
| **ID** | String | "E_001_1" | Identificador único de la etiqueta original |
| **N-grama** | String | "análisis temático" | El n-grama extraído |
| **Caso** | String | "5" o "5,6" | ID(s) del caso(s) de donde viene este registro |
| **Fuente** | String | "Entrevista" | Origen del dato |
| **Nivel** | String | "Etiqueta [Nivel 1]" | En qué nivel de la jerarquía fue encontrado |
| **Contexto completo** | String | "Etiqueta [Nivel 1]: ... \| Etiqueta [Nivel 2]: ..." | Todas las etiquetas del registro para contexto |
| **Cita textual** | String | "El análisis temático..." | Texto original sin procesar |

**Hojas 5 y 6: Frecuencias_seleccion_1 y Frecuencias_seleccion_2**
- Inicialmente **vacías**
- **Tú copias manualmente** los n-gramas que quieres que sea analizados jerárquicamente
- Estructura: Copiados desde "Frecuencias Globales"

---

### **SCRIPT 1B: `01b_analisis_jerarquico.py`**

#### **Entrada:**
- Archivo: `01_ngrams_procesados.xlsx`
- Lee: `Frecuencias_seleccion_1` y `Frecuencias_seleccion_2`

#### **Procesamiento:**

**Definición de Jerarquía:**
- **Nivel 1 (Principal)**: N-gramas que aparecen en ≥50% de los casos
- **Nivel 2 (Secundario)**: N-gramas que aparecen en 25-50% de los casos
- **Nivel 3 (Terciario)**: N-gramas que aparecen en <25% de los casos

**Relaciones jerárquicas:**
- Nivel 1 → Nivel 2 → Nivel 3 (estructura padre-hijo)
- Se visualiza como árbol vertical

#### **Salida: `01b_analisis_jerarquico.xlsx`**

**Hoja 1: Jerarquía Seleccionados_1 y Hoja 2: Jerarquía Seleccionados_2**

| Variable | Cálculo | Ejemplo | Explicación |
|----------|---------|---------|-------------|
| **N-Grama Principal (1)** | De input | "análisis temático" | N-grama de Nivel 1 (raíz del árbol) |
| **N-Grama Secundario (2)** | De input | "análisis cualitativo" | N-grama de Nivel 2 (hijo directo) |
| **N-Grama Terciario (3)** | De input | "análisis de contenido" | N-grama de Nivel 3 (nieto) |
| **Frecuencia** | De Frecuencias Globales | 12 | Frecuencia Total del n-grama de Nivel 1 |
| **% Casos** | De Frecuencias Globales | "75.0%" | % Casos cubiertos del n-grama de Nivel 1 |

**Gráficos generados:**
- `red_jerarquica_seleccionados_1.png`: Árbol jerárquico vertical (Selección 1)
- `red_jerarquica_seleccionados_2.png`: Árbol jerárquico vertical (Selección 2)

---

### **SCRIPT 2: `02_analizar_coocurrencias.py`**

#### **Entrada:**
- Archivo: `01_ngrams_procesados.xlsx`
- Lee: `Frecuencias Globales` y `Registro Detallado`

#### **Procesamiento:**

**Tipo 1: Co-ocurrencias FUERTES**
- **Definición**: N-gramas que aparecen **en el MISMO NIVEL y MISMO CASO**
- **Ejemplo**: Si en Caso 5, Nivel 1, aparecen "análisis" y "temático" en registros diferentes → **Co-ocurrencia fuerte**
- **Agrupación**: `GROUP BY [Caso, Fuente, Nivel]`

**Tipo 2: Co-ocurrencias DÉBILES**
- **Definición**: N-gramas que aparecen **en DIFERENTES NIVELES pero MISMO CASO**
- **Ejemplo**: Si en Caso 5 aparece "análisis" en Nivel 1 y "temático" en Nivel 2 → **Co-ocurrencia débil**
- **Agrupación**: `GROUP BY [Caso, Fuente]`

#### **Salida: `02_analisis_coocurrencias.xlsx`**

**Hoja 1: Co-ocurrencias Fuertes y Hoja 2: Co-ocurrencias Débiles**

| Variable | Cálculo | Ejemplo | Explicación |
|----------|---------|---------|-------------|
| **N-grama 1** | Identificador | "análisis" | Primer n-grama de la pareja (orden alfabético) |
| **N-grama 2** | Identificador | "temático" | Segundo n-grama de la pareja (orden alfabético) |
| **Veces juntos** | Conteo directo | 8 | **Número total de veces** que ambos n-gramas aparecen juntos en el mismo contexto (nivel/caso) |
| **Num Casos** | Conteo ÚNICO | 5 | **Número de casos diferentes** en que la pareja co-ocurre (de 16 total) |
| **Num Fuentes** | Conteo ÚNICO | 2 | **Número de fuentes diferentes** en que la pareja co-ocurre |
| **Casos donde co-ocurren** | Lista ÚNICA | "1, 3, 5, 7, 9" | IDs de los casos en que ambos aparecen juntos |
| **Fuentes donde co-ocurren** | Lista ÚNICA | "Entrevista, Documento" | Nombres de las fuentes en que aparecen juntos |
| **Freq N-grama 1** | De Frecuencias Globales | 15 | Frecuencia Total del primer n-grama (apariciones totales, con o sin el otro) |
| **Freq N-grama 2** | De Frecuencias Globales | 12 | Frecuencia Total del segundo n-grama (apariciones totales, con o sin el otro) |
| **% Casos coocurren** | (Num Casos / 16) × 100 | 31.3% | **Porcentaje del total de casos** donde ambos aparecen juntos |
| **Fuerza de Asociación** | (Veces juntos / MAX(Freq N1, Freq N2)) × 100 | 53.3% | **Qué porcentaje del n-grama más frecuente co-ocurre con el otro** (mide dependencia relativa) |
| **% Casos Juntos vs Separados** | (Num Casos coocurren / (Casos N1 + Casos N2 - Num Casos coocurren)) × 100 | 62.5% | **De los casos que tienen AL MENOS uno de los dos, qué % tiene AMBOS** (mide asociación) |

**Interpretación de Fuerza de Asociación:**
- **> 80%**: Muy fuerte - El n-grama más frecuente casi siempre va con el otro
- **50-80%**: Fuerte - Aparecen juntos frecuentemente
- **20-50%**: Moderada - Aparecen juntos ocasionalmente
- **< 20%**: Débil - Raramente aparecen juntos

**Hojas 3 y 4: Coocurrencias_seleccion_1 y Coocurrencias_seleccion_2**
- Inicialmente **vacías**
- **Tú copias manualmente** las coocurrencias que quieres visualizar
- Se usan en Script 2B para generar gráficos

---

### **SCRIPT 2B: `02b_visualizar_coocurrencias.py`**

#### **Entrada:**
- Archivo: `02_analisis_coocurrencias.xlsx`
- Lee: `Coocurrencias_seleccion_1` y `Coocurrencias_seleccion_2`
- También consulta: `01_ngrams_procesados.xlsx` para metadatos

#### **Procesamiento:**

**Para cada selección y tipo (fuerte/débil):**
1. Lee las coocurrencias seleccionadas
2. Crea un grafo de red donde:
   - **Nodos** = N-gramas individuales
   - **Aristas** = Co-ocurrencias (conexiones entre n-gramas)
   - **Tamaño del nodo** ∝ Frecuencia del n-grama
   - **Ancho de arista** ∝ Veces juntos
   - **Color del nodo** = % de casos que cubre

#### **Salida: Gráficos PNG**

- `red_coocurrencias_fuerte_seleccion_1.png`
- `red_coocurrencias_debil_seleccion_1.png`
- `red_coocurrencias_fuerte_seleccion_2.png`
- `red_coocurrencias_debil_seleccion_2.png`

**Propiedades visuales:**
- **Nodo grande**: N-grama muy frecuente
- **Nodo rojo**: Cubre muchos casos (>50%)
- **Nodo azul**: Cubre pocos casos (<25%)
- **Arista gruesa**: Co-ocurrencia frecuente
- **Arista delgada**: Co-ocurrencia rara
- **Proximidad**: Nodos conectados frecuentemente aparecen cerca

---

## 🧮 Fórmulas Principales

### **Para N-Gramas:**

```
Frecuencia Total = Σ(apariciones del n-grama en todos los registros)

Num Casos = |{casos únicos donde aparece el n-grama}|

% Casos cubiertos = (Num Casos / Total de casos en dataset) × 100
                   = (Num Casos / 16) × 100

Num Fuentes = |{fuentes únicas donde aparece el n-grama}|
```

### **Para Co-ocurrencias:**

```
Veces juntos = Σ(ocasiones donde ambos n-gramas co-ocurren en el mismo contexto)

Num Casos (coocurrencia) = |{casos únicos donde ambos aparecen juntos}|

% Casos coocurren = (Num Casos coocurrencia / 16) × 100

Num Fuentes (coocurrencia) = |{fuentes únicas donde ambos aparecen juntos}|

Fuerza de Asociación = (Veces juntos / MAX(Freq N1, Freq N2)) × 100
                      (alternativa: usar MIN para mayor severidad)

% Casos Juntos vs Separados = (Num Casos coocurrencia / 
                               (Num Casos N1 + Num Casos N2 - Num Casos coocurrencia)) × 100
                             = Índice de Jaccard simplificado
```

---

## 📝 Cómo Usar

### **Paso 1: Prepara tu Excel**

Tu archivo debe estar en `datos/brutos/Análisis temático.xlsx` con estas columnas:

| ID | Caso | Fuente | Etiqueta [Nivel 1] | Etiqueta [Nivel 2] | Etiqueta [Nivel 3] | Caracterización | Cita |
|----|------|--------|-------------------|-------------------|-------------------|-----------------|------|
| E_001_1 | 1 | Entrevista | Análisis | Temático | De contenido | ... | "El análisis temático..." |

### **Paso 2: Ejecuta Script 1**

```bash
python scripts/01_limpiar_y_extraer_ngramas.py
```

- Genera: `datos/procesados/01_ngrams_procesados.xlsx`
- Revisa las 4 hojas para entender la estructura

### **Paso 3: Selecciona N-Gramas (Opcional - Para Script 1B)**

1. Abre `01_ngrams_procesados.xlsx`
2. Copia filas desde "Frecuencias Globales" a "Frecuencias_seleccion_1" o "_2"
3. Esto es necesario **solo si** quieres ver análisis jerárquico

### **Paso 4: Ejecuta Script 1B (Opcional)**

```bash
python scripts/01b_analisis_jerarquico.py
```

- Genera: `resultados/01b_analisis_jerarquico.xlsx` + gráficos jerárquicos
- Solo si hay n-gramas en "Frecuencias_seleccion_1" o "_2"

### **Paso 5: Ejecuta Script 2**

```bash
python scripts/02_analizar_coocurrencias.py
```

- Genera: `resultados/02_analisis_coocurrencias.xlsx`
- Muestra TODAS las coocurrencias encontradas

### **Paso 6: Selecciona Co-ocurrencias**

1. Abre `02_analisis_coocurrencias.xlsx`
2. Copia filas desde "Co-ocurrencias Fuertes" o "Débiles" a "Coocurrencias_seleccion_1" o "_2"
3. Guarda el archivo

### **Paso 7: Ejecuta Script 2B**

```bash
python scripts/02b_visualizar_coocurrencias.py
```

- Genera: Gráficos PNG de las co-ocurrencias seleccionadas
- Visualiza en `resultados/`

---

## ⚙️ Configuración

Todas las rutas y nombres de hojas están configurados en cada script. Modifica si necesitas:

```python
ARCHIVO_ENTRADA = "datos/brutos/Análisis temático.xlsx"
ARCHIVO_SALIDA = "datos/procesados/01_ngrams_procesados.xlsx"
```

---

## 🐛 Troubleshooting

### **"0 coocurrencias encontradas"**
- Verifica que el Registro Detallado tiene múltiples n-gramas por caso/fuente/nivel
- Si cada combinación tiene solo 1 n-grama, no hay coocurrencias posibles

### **"No se encontraron n-gramas con frecuencia >= 2"**
- Tu dataset es muy pequeño o muy diverso
- Reduce el threshold de frecuencia en Script 1 (línea ~195): cambiar `>= 2` a `>= 1`

### **Error "Hoja no encontrada"**
- Verifica que copiaste datos a "Frecuencias_seleccion_1" antes de ejecutar Script 1B
- Verifica que copiaste datos a "Coocurrencias_seleccion_1" antes de ejecutar Script 2B

---

## 📄 Licencia

Proyecto abierto para análisis académico y de investigación.

---

## ✨ Notas Finales

- **Todo es reproducible**: Los pasos son siempre los mismos
- **Los cálculos son determinísticos**: Mismos datos = mismos resultados
- **Escalable**: Funciona con datasets pequeños y grandes
- **Documentado**: Cada variable tiene explicación clara

¿Preguntas? Revisa los comentarios en cada script.