# Análisis Temático de Códigos: N-gramas, Co-ocurrencias y Estructuras Jerárquicas

Sistema automatizado para análisis de etiquetas codificadas usando procesamiento de lenguaje natural, extracción de n-gramas, análisis de coocurrencias y estructuras jerárquicas.

---

## ⚖️ Declaración de Autoría y Atribución

### ✍️ Contribuciones Intelectuales

**Conceptualización, Diseño Metodológico y Dirección del Proyecto:**
- Autora del TFG (usuaria del repositorio)
- Todas las decisiones metodológicas, estructuras de análisis, lógica de análisis y criterios de filtrado fueron conceptualizadas originalmente por la autora
- El diseño de las métricas, definición de co-ocurrencias fuertes/débiles y visualizaciones emerge de las necesidades específicas de la investigación

**Implementación Técnica y Desarrollo de Código:**
- **GitHub Copilot** (versión 0.45.1): Asistencia en redacción de scripts Python, optimización de algoritmos y mejoras iterativas
- **Windsurf** (versión 1.48.2): Consultoría técnica, sugerencias de refactorización y asistencia en iteraciones posteriores

**Supervisión y Validación:**
- Todo el código fue revisado, testeado y validado por el autor antes de uso

### 🚨 Aspectos Cubiertos para Evitar Plagio

✅ **Conceptualización original**: Todas las métricas son conceptualización de la autora
- Definición de co-ocurrencias fuertes (2+ casos, 2+ fuentes) vs débiles (2+ casos, misma fuente)
- Normalización de grosores de aristas proporcional a % Casos Juntos vs Separados
- Uso de layouts circulares/spring ordenados por conectividad

✅ **Decisiones de diseño**: Todas son de la autora, implementadas con asistencia de IA

✅ **Iteraciones metodológicas**: El refinamiento de algoritmos (ej: cambio de criterios de coocurrencia) surgió de decisiones propias de la autora

✅ **Código asistido**: Los scripts fueron **redactados por IA siguiendo especificaciones explícitas de la autora**, pero la lógica es de la autora

✅ **Supervisión técnica**: Todas las funciones fueron revisadas por la autora antes de implementación

---

## 📦 Versiones de Software y Dependencias

### **Entorno Base de Ejecución**

| Software | Versión | Propósito |
|----------|---------|----------|
| **Python** | 3.13.3 | Lenguaje de programación base |
| **pip** | 26.1 | Gestor de paquetes Python |
| **setuptools** | 81.0.0 | Construcción y distribución de paquetes |
| **wheel** | 0.47.0 | Formato de paquete Python |

### **Procesamiento de Datos y DataFrames**

| Biblioteca | Versión | Propósito | Referencia APA 7 |
|-----------|---------|----------|------------------|
| **pandas** | 3.0.2 | Lectura/procesamiento de Excel y DataFrames | McKinney, W. (2010). Data structures for statistical computing in python. *Proceedings of the 9th Python in Science Conference*, 445, 51-56. |
| **openpyxl** | 3.1.5 | Escritura avanzada en archivos Excel | Gazoni, E. (2020). openpyxl - A Python library to read/write Excel 2010 xlsx/xlsm files. GitHub. |
| **python-dateutil** | 2.9.0 | Utilidades para manejo de fechas | Etc (BSD License). python-dateutil. |
| **tzdata** | 2026.1 | Base de datos de zonas horarias | IANA Time Zone Database. |
| **six** | 1.17.0 | Compatibilidad Python 2/3 | Benjamin, C. (2010). Six: Python 2 and 3 compatibility library. |

### **Procesamiento de Lenguaje Natural (NLP)**

| Biblioteca | Versión | Propósito | Referencia APA 7 |
|-----------|---------|----------|------------------|
| **spaCy** | 3.8.14 | Lematización, tokenización y NLP | Honnibal, M., & Montani, I. (2017). spaCy 2: Natural language understanding with Bloom embeddings, convolutional neural networks and incremental parsing. In *Proceedings of LREC 2018*. |
| **spacy-legacy** | 3.0.12 | Compatibilidad con versiones anteriores de spaCy | Honnibal, M., & Montani, I. (n.d.). spacy-legacy. GitHub. |
| **spacy-loggers** | 1.0.5 | Sistema de logging para spaCy | Honnibal, M., & Montani, I. (n.d.). spacy-loggers. GitHub. |
| **es_core_news_sm** | 3.8.0 | Modelo de lenguaje español para spaCy | Honnibal, M., & Montani, I. (2018). spaCy models for Spanish language. GitHub. |
| **cymem** | 2.0.13 | Gestor de memoria para spaCy | Honnibal, M. (n.d.). cymem. GitHub. |
| **murmurhash** | 1.0.15 | Función hash para spaCy | Honnibal, M. (n.d.). murmurhash. GitHub. |
| **preshed** | 3.0.13 | Estructuras de datos hash para NLP | Honnibal, M. (n.d.). preshed. GitHub. |
| **catalogue** | 2.0.10 | Registro de componentes para spaCy | Honnibal, M., & Montani, I. (n.d.). catalogue. GitHub. |
| **srsly** | 2.5.3 | Serialización de datos en spaCy | Honnibal, M., & Montani, I. (n.d.). srsly. GitHub. |
| **thinc** | 8.3.13 | Librería de machine learning para NLP | Honnibal, M., & Montani, I. (n.d.). Thinc. GitHub. |
| **blis** | 1.3.3 | Algebra lineal optimizada para NLP | Montani, I. (n.d.). BLIS. GitHub. |
| **regex** | 2026.4.4 | Motor de expresiones regulares avanzado | Van der Giessen, M., & Contributors. (2024). regex - Regular expression operations for Python. PyPI. |

### **Análisis de Redes y Grafos**

| Biblioteca | Versión | Propósito | Referencia APA 7 |
|-----------|---------|----------|------------------|
| **networkx** | 3.6.1 | Creación, análisis y visualización de grafos | Hagberg, A. A., Schult, D. A., & Swart, P. J. (2008). Exploring network structure, dynamics, and function using NetworkX. In *Proceedings of the 7th Python in Science Conference* (Vol. 2008, pp. 11-15). SciPy. |

### **Visualización y Gráficos**

| Biblioteca | Versión | Propósito | Referencia APA 7 |
|-----------|---------|----------|------------------|
| **matplotlib** | 3.10.9 | Generación de visualizaciones y gráficos | Hunter, J. D. (2007). Matplotlib: A 2D graphics environment. *Computing in Science & Engineering*, 9(3), 90-95. |
| **pillow** | 12.2.0 | Procesamiento de imágenes | Lundh, F., & Contributors (2024). Pillow - Python Imaging Library. PyPI. |
| **contourpy** | 1.3.3 | Cálculo de contornos para matplotlib | Casey, A., & Contributors. (2023). contourpy. PyPI. |
| **kiwisolver** | 1.5.0 | Solver de constraints para matplotlib | Irelide (2013). kiwisolver. GitHub. |
| **fonttools** | 4.62.1 | Herramientas para tipografía en gráficos | Pycnocopy, T. (2024). fonttools. GitHub. |
| **pyparsing** | 3.3.2 | Parser para matplotlib | McGuire, P. (2024). pyparsing. GitHub. |

### **Análisis Científico y Estadístico**

| Biblioteca | Versión | Propósito | Referencia APA 7 |
|-----------|---------|----------|------------------|
| **numpy** | 2.4.4 | Cálculos numéricos y algebra lineal | Harris, C. R., et al. (2020). Array programming with NumPy. *Nature*, 585(7825), 357-362. |
| **scipy** | 1.17.1 | Algoritmos científicos y estadísticos | Virtanen, P., et al. (2020). SciPy 1.0: fundamental algorithms for scientific computing in Python. *Nature Methods*, 17(3), 261-272. |
| **sympy** | 1.14.0 | Matemáticas simbólicas | Meurer, A., et al. (2017). SymPy: symbolic computing in Python. *PeerJ Computer Science*, 3, e103. |
| **mpmath** | 1.3.0 | Aritmética de precisión arbitraria | Johansson, F. (2010). mpmath: a Python library for arbitrary-precision floating-point arithmetic. |

### **Herramientas de Deep Learning e IA**

| Biblioteca | Versión | Propósito | Referencia APA 7 |
|-----------|---------|----------|------------------|
| **torch** | 2.11.0 | Framework de deep learning (usado por transformers) | Paszke, A., et al. (2019). PyTorch: An imperative style, high-performance deep learning library. In *Advances in neural information processing systems* (pp. 8026-8037). |
| **transformers** | 5.7.0 | Modelos preentrenados de NLP | Wolf, M., et al. (2020). Transformers: State-of-the-art natural language processing. In *Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing: System Demonstrations* (pp. 38-45). |
| **huggingface_hub** | 1.13.0 | API para acceder a modelos de Hugging Face | Lhoest, Q., et al. (2021). Datasets: A community library for natural language processing. In *Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing: Demo* (pp. 175-184). |
| **tokenizers** | 0.22.2 | Tokenizadores rápidos para transformers | Cousin, A., et al. (2022). 🤗 Tokenizers: Fast State-of-the-art Tokenization on Raw Text. |
| **safetensors** | 0.7.0 | Formato seguro para guardar tensores | Lhoest, Q., et al. (2023). safetensors: Safely store and load machine learning models. Hugging Face. |
| **filelock** | 3.29.0 | Bloqueos de archivos para descarga segura | Schroetter, B. (2010). filelock - A Python file locking library. PyPI. |
| **fsspec** | 2026.4.0 | Abstracción de sistemas de archivos | Open Storage Group (2024). fsspec - Filesystem Spec. GitHub. |
| **smart_open** | 7.6.0 | Lectura de archivos desde URLs o almacenamiento en la nube | Rehurek, R. (2024). smart_open. GitHub. |
| **cloudpathlib** | 0.24.0 | Rutas de objetos en la nube | Whitmore, D. (2024). cloudpathlib. GitHub. |
| **hf-xet** | 1.4.3 | Protocolo XET para Hugging Face | Hugging Face (2024). hf-xet. PyPI. |
| **accelerate** | 1.13.0 | Aceleración de entrenamiento y inferencia | Manté, L., et al. (2024). Accelerate - Easy distributed training and inference in PyTorch. Hugging Face. |

### **Gestión de Configuración y Tipos**

| Biblioteca | Versión | Propósito |
|-----------|---------|----------|
| **pydantic** | 2.13.3 | Validación de datos y gestión de esquemas |
| **pydantic_core** | 2.46.3 | Motor principal de Pydantic |
| **annotated-types** | 0.7.0 | Anotaciones de tipos avanzadas |
| **annotated-doc** | 0.0.4 | Documentación de anotaciones |
| **confection** | 1.3.3 | Gestión de configuración para NLP |
| **typer** | 0.25.1 | Framework CLI basado en type hints |
| **click** | 8.3.3 | Interfaz de línea de comandos |
| **shellingham** | 1.5.4 | Detección de shell para CLI |

### **Comunicaciones y HTTP**

| Biblioteca | Versión | Propósito |
|-----------|---------|----------|
| **requests** | 2.33.1 | Librería HTTP para Python |
| **httpx** | 0.28.1 | Cliente HTTP moderno |
| **httpcore** | 1.0.9 | Motor HTTP de bajo nivel |
| **urllib3** | 2.6.3 | Conexiones HTTP pooled para requests |
| **certifi** | 2026.4.22 | Certificados CA del navegador Mozilla |
| **idna** | 3.13 | Decodificación IDNA de dominios |
| **charset-normalizer** | 3.4.7 | Detección de encoding de caracteres |
| **h11** | 0.16.0 | Máquina de estados HTTP |
| **anyio** | 4.13.0 | Interfaz asíncrona agnóstica |

### **Utilidades y Miscelánea**

| Biblioteca | Versión | Propósito |
|-----------|---------|----------|
| **tqdm** | 4.67.3 | Barras de progreso para loops |
| **Jinja2** | 3.1.6 | Motor de plantillas (usado por spaCy) |
| **MarkupSafe** | 3.0.3 | Escapado seguro de HTML/XML |
| **PyYAML** | 6.0.3 | Parser YAML para configuración |
| **lxml** | 6.0.2 | Procesamiento de XML/HTML |
| **python-docx** | 1.2.0 | Creación de documentos Word |
| **et_xmlfile** | 2.0.0 | Utilidades para archivos XML Excel |
| **bibtexparser** | 1.4.4 | Parser BibTeX para referencias |
| **rispy** | 0.10.0 | Parser RIS para gestores bibliográficos |
| **markdown-it-py** | 4.0.0 | Parser Markdown |
| **mdurl** | 0.1.2 | Parsing de URLs en Markdown |
| **Pygments** | 2.20.0 | Resaltado de sintaxis |
| **rich** | 15.0.0 | Formateo rico de terminal |
| **colorama** | 0.4.6 | Colores en terminal cross-platform |
| **wasabi** | 1.1.3 | Mensajes formateados (usado por spaCy) |
| **psutil** | 7.2.2 | Información del sistema |
| **typing_extensions** | 4.15.0 | Extensiones typing para Python <3.10 |
| **typing-inspection** | 0.4.2 | Inspección de tipos |
| **packaging** | 26.2 | Utilidades de versioning |
| **weasel** | 1.0.0 | Gestor de dependencias para spaCy |

### **Herramientas de IA Asistidas (Desarrollo)**

| Herramienta | Versión | Función | Declaración |
|-------------|---------|---------|-------------|
| **GitHub Copilot** | 0.45.1 | Asistencia en redacción de código Python | Asistencia técnica - No autoría intelectual |
| **Windsurf (Codeium)** | 1.48.2 | Consultoría técnica y refactorización | Asistencia técnica - No autoría intelectual |

### **Software de Análisis (Usuario)**

| Software | Versión | Propósito |
|----------|---------|----------|
| **Microsoft Excel** | 2019 (Hogar y Estudiantes) | Preparación de datos de entrada y revisión de salidas |
| **Python IDE** | - | Ejecución de scripts |
