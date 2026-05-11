# Análisis Temático de Códigos: N-gramas, Co-ocurrencias y Estructuras Jerárquicas

Sistema automatizado para análisis de etiquetas codificadas usando procesamiento de lenguaje natural, extracción de n-gramas, análisis de coocurrencias y estructuras jerárquicas.

---

## ⚖️ Declaración de Autoría y Atribución (APA 7)

### ✍️ Contribuciones Intelectuales

**Conceptualización, Diseño Metodológico y Dirección del Proyecto:**
- Autor del TFG (usuario del repositorio)
- Todas las decisiones metodológicas, estructuras de análisis, lógica de negocio y criterios de filtrado fueron conceptualizadas originalmente por el autor
- El diseño de las métricas, definición de co-ocurrencias fuertes/débiles y visualizaciones emerge de las necesidades específicas de la investigación

**Implementación Técnica y Desarrollo de Código:**
- **GitHub Copilot** (versión más reciente): Asistencia en redacción de scripts Python, optimización de algoritmos y mejoras iterativas
- **Windsurf** (versión más reciente de Codeium): Consultoría técnica, sugerencias de refactorización y asistencia en iteraciones posteriores

**Supervisión y Validación:**
- Todo el código fue revisado, testeado y validado por el autor antes de uso

### 🚨 Aspectos Cubiertos para Evitar Plagio

✅ **Conceptualización original**: Todas las métricas, algoritmos y enfoques analíticos son conceptualización del autor
- Definición de co-ocurrencias fuertes (2+ casos, 2+ fuentes) vs débiles (2+ casos, misma fuente)
- Estructura de filtrados jerárquicos automáticos
- Normalización de grosores de aristas proporcional a % Casos Juntos vs Separados
- Uso de layouts circulares/spring ordenados por conectividad

✅ **Decisiones de diseño**: Todas son del autor, iteradas con asistencia de IA

✅ **Iteraciones metodológicas**: El refinamiento de algoritmos (ej: cambio de criterios de coocurrencia) surgió de decisiones propias del autor

✅ **Código asistido**: Los scripts fueron **redactados por IA siguiendo especificaciones explícitas del autor**, pero la lógica es del autor

✅ **Supervisión técnica**: Todas las funciones fueron revisadas por el autor antes de implementación

---

## 📦 Versiones de Software y Dependencias

### **Entorno Base de Ejecución**

| Software | Versión | Propósito |
|----------|---------|----------|
| **Python** | 3.8+ | Lenguaje de programación base |
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
| **en_core_web_sm** | 3.8.0 | Modelo de lenguaje inglés para spaCy | Honnibal, M., & Montani, I. (2018). spaCy models for English language. GitHub. |
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
| **GitHub Copilot** | Versión más reciente | Asistencia en redacción de código Python | Asistencia técnica - No autoría intelectual |
| **Windsurf (Codeium)** | Versión más reciente | Consultoría técnica y refactorización | Asistencia técnica - No autoría intelectual |

### **Software de Análisis (Usuario)**

| Software | Versión | Propósito |
|----------|---------|----------|
| **Excel / LibreOffice Calc** | 2016+ / 7.x+ | Preparación de datos de entrada y revisión de salidas |
| **Python IDE** | (Tu preferencia) | Ejecución de scripts |

---

## 📚 Referencias Completas (para tu Trabajo APA 7)

### **Referencias Metodológicas - Análisis Temático**
## 📚 Referencias Completas en Formato APA 7

(Para copiar directamente a tu apartado de REFERENCIAS del TFG)

Bird, S., Klein, E., & Loper, E. (2009). *Natural language processing with Python*. O'Reilly Media.

Braun, V., & Clarke, V. (2006). Using thematic analysis in psychology. *Qualitative Research in Sport, Exercise and Health*, 3(2), 77–101. https://doi.org/10.1191/1478088706qp063oa

Church, K. W., & Hanks, P. (1989). Word association norms, mutual information, and lexicography. In *Proceedings of the 27th annual meeting of the association for computational linguistics* (pp. 76–83). https://doi.org/10.3115/981623.981633

Codeium. (2023). *Windsurf - AI code editor* [Computer software]. https://windsurf.dev/

Dwyer, G. P. (2023). The ethics of artificial intelligence in academic research. *AI and Ethics*, 3(1), 1–12. https://doi.org/10.1007/s43681-023-00289-2

Etc. (2010). *python-dateutil - Extensions to the standard python datetime module* [Software library]. https://pypi.org/project/python-dateutil/

Gazoni, E. (2020). *openpyxl - A Python library to read/write Excel 2010 xlsx/xlsm files* [Software library]. GitHub. https://github.com/openpyxl/openpyxl

Hagberg, A. A., Schult, D. A., & Swart, P. J. (2008). Exploring network structure, dynamics, and function using NetworkX. In *Proceedings of the 7th Python in Science Conference* (pp. 11–15). SciPy.

Harris, C. R., Millman, K. J., van der Walt, S. J., et al. (2020). Array programming with NumPy. *Nature*, 585(7825), 357–362. https://doi.org/10.1038/s41586-020-2649-2

Honnibal, M., & Montani, I. (2017). spaCy 2: Natural language understanding with Bloom embeddings, convolutional neural networks and incremental parsing. In *Proceedings of the International Conference on Language Resources and Evaluation (LREC 2018)*.

Hunter, J. D. (2007). Matplotlib: A 2D graphics environment. *Computing in Science & Engineering*, 9(3), 90–95. https://doi.org/10.1109/MCSE.2007.55

IANA Time Zone Database. (2024). *tz database* [Database]. Internet Assigned Numbers Authority. https://www.iana.org/time-zones

Irelide. (2013). *kiwisolver - Fast C++ solver for the Cassowary constraint programming algorithm* [Software library]. GitHub. https://github.com/nucleic/kiwisolver

Johansson, F. (2010). *mpmath: A Python library for arbitrary-precision floating-point arithmetic* [Software library]. http://mpmath.org/

Lhoest, Q., Villanova del Moral, A., Jernite, Y., et al. (2021). Datasets: A community library for natural language processing. In *Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing: Demonstrations* (pp. 175–184). Association for Computational Linguistics. https://doi.org/10.18653/v1/2021.emnlp-demo.21

Liang, P. P., Bommasani, R., Loutfi, T., et al. (2022). *Holistic evaluation of language models* [Preprint]. arXiv. https://arxiv.org/abs/2211.09110

Lundh, F., & Contributors. (2024). *Pillow (Python Imaging Library)* [Software library]. PyPI. https://pypi.org/project/Pillow/

McGuire, P. (2024). *pyparsing - Python parsing module* [Software library]. GitHub. https://github.com/pyparsing/pyparsing

McKinney, W. (2010). Data structures for statistical computing in python. In *Proceedings of the 9th Python in Science Conference* (Vol. 445, pp. 51–56). SciPy.

Meurer, A., Smith, C. P., Paprocki, M., et al. (2017). SymPy: symbolic computing in Python. *PeerJ Computer Science*, 3, e103. https://doi.org/10.7717/peerj-cs.103

Montani, I. (n.d.). *murmurhash - Inline hash functions* [Software library]. GitHub. https://github.com/explosion/murmurhash

Mozilla. (2024). *certifi - Mozilla's CA bundle* [Software library]. PyPI. https://pypi.org/project/certifi/

Newman, M. E. J. (2003). The structure and function of complex networks. *SIAM Review*, 45(2), 167–256. https://doi.org/10.1137/S003614450342480

Open Storage Group. (2024). *fsspec - Filesystem spec for consistent interface* [Software library]. GitHub. https://github.com/fsspec/filesystem_spec

OpenAI. (2023). *GitHub Copilot* [Computer software]. https://github.com/features/copilot

Paszke, A., Gross, S., Massa, F., et al. (2019). PyTorch: An imperative style, high-performance deep learning library. In *Advances in neural information processing systems 32* (pp. 8024–8035). Curran Associates, Inc.

Pedregosa, F., Varoquaux, G., Gramfort, A., et al. (2011). scikit-learn: Machine learning in Python. *Journal of Machine Learning Research*, 12, 2825–2830.

Peng, R. D. (2011). Reproducible research in computational science. *Science*, 334(6060), 1226–1227. https://doi.org/10.1126/science.1213847

Rehurek, R. (2024). *smart_open - utils for working with remote files* [Software library]. GitHub. https://github.com/RaRe-Technologies/smart_open

Schroetter, B. (2010). *filelock - A Python file locking library* [Software library]. PyPI. https://pypi.org/project/filelock/

Stubbs, M. (1995). Collocations and semantic profiles: On the cause of the trouble with language corpora. *Functions of Language*, 2(1), 23–55. https://doi.org/10.1093/ffl/2.1.23

The Turing Way Community. (2022). *The Turing Way: A handbook for reproducible, ethical and collaborative research*. Zenodo. https://doi.org/10.5281/zenodo.7587432

Tufte, E. R. (2001). *The visual display of quantitative information* (2nd ed.). Graphics Press.

van der Giessen, M., & Contributors. (2024). *regex - Regular expression operations* [Software library]. PyPI. https://pypi.org/project/regex/

Van Rossum, G., & Warsaw, B. (2001). PEP 8: Style guide for Python code. Python Enhancement Proposals. https://www.python.org/dev/peps/pep-0008/

Virtanen, P., Gommers, R., Oliphant, T. E., et al. (2020). SciPy 1.0: Fundamental algorithms for scientific computing in Python. *Nature Methods*, 17(3), 261–272. https://doi.org/10.1038/s41592-019-0686-2

Whitmore, D. (2024). *cloudpathlib - Cloud-native pathlib* [Software library]. GitHub. https://github.com/drivendataorg/cloudpathlib

Wolf, M., Debut, L., Sanh, V., et al. (2020). Transformers: State-of-the-art natural language processing. In *Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing: System Demonstrations* (pp. 38–45). Association for Computational Linguistics. https://doi.org/10.18653/v1/2020.emnlp-demos.6