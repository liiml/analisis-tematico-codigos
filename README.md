# Análisis Temático de Códigos: N-gramas y Co-ocurrencias

Sistema automatizado para análisis de etiquetas codificadas usando procesamiento de lenguaje natural, extracción de n-gramas, análisis de coocurrencias y estructuras jerárquicas.

---

## 📋 Descripción

Este proyecto analiza un archivo Excel con etiquetas codificadas en múltiples niveles (16 casos, 13 fuentes) y:

1. **Limpia y procesa** el texto (lematización, eliminación de tildes, stop-words)
2. **Extrae n-gramas** que se repiten 2+ veces
3. **Genera selecciones jerárquicas** (n-gramas principales + subordinados)
4. **Calcula co-ocurrencias** (fuertes, débiles y jerárquicas)
5. **Genera reportes Excel** con tablas de frecuencias, matrices y análisis
6. **Visualiza redes temáticas** como gráficos interactivos

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
