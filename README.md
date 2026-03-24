# Análisis de Campañas de Marketing Bancario 📊

## Propósito del Proyecto
El objetivo principal de este proyecto es determinar el éxito de la actual campaña de marketing de un Banco portugués, basada en la captación de depósitos a plazo mediante llamadas telefónicas. A través de un proceso de **ETL** (Extracción, Transformación y Carga) y un **Análisis Exploratorio de Datos** (EDA), se busca identificar el perfil del cliente con mayor propensión a suscribir el producto y optimizar la eficiencia operativa de las llamadas.

## Estructura del Repositorio
* `/data`: Contiene los archivos en bruto (`bank-additional.csv`, `unified-customer-details.xlsx`) y el dataset final procesado.
* `/notebooks`: Incluye el archivo `EDA_Bank.ipynb` con todo el desarrollo del código en Python.
* `README.md`: Informe ejecutivo y descripción del proceso.

## Transformación y Limpieza de los Datos
El proceso de transformación de datos se enfocó en garantizar la integridad estadística para un análisis financiero riguroso:

1.  **Unificación**: Se consolidaron las bases de datos mediante un `merge` por la columna común `ID`.
2.  **Normalización**: Traducción de etiquetas y variables string al español para mejorar la interpretabilidad.
3.  **Tratamiento de Nulos**:
    * **Variables Macroeconómicas**: Extrapolación lineal y media para `id_precio.cons` y `tasa_interes.3m`.
    * **Perfil Sociodemográfico**: Imputación condicional de `nivel_educativo` basado en `empleo` y uso de la mediana para `edad`.
    * **Variables de Riesgo**: Imputación de ceros en `morosidad` (dada la baja prevalencia) y codificación de `-1` (desconocido) en `hipoteca` y `prestamos` para evitar sesgos de confirmación.
    * **Temporalidad**: Uso de *Forward Fill* para `fecha_llam` preservando el orden cronológico.

### Segmentación de Datos (Feature Engineering)
Se crearon nuevas dimensiones estratégicas para profundizar el análisis:
* `duracion_llam_min`: Conversión de segundos a minutos para una interpretación más práctica.
* `antiguedad_cliente_anos`: Cálculo del ciclo de vida del cliente desde su vinculación hasta el impacto de la campaña.
* **Categorizaciones**: Segmentación por Nivel Educativo (Bajo/Medio/Alto), Ingresos (cuartiles), Tamaño de Familia (Pequeña/Mediana/Grande) y Frecuencia de Consultas Web.

## Informe Explicativo del Análisis (Hallazgos Principales)
Tras el análisis bivariado y multivariado, se desprenden las siguientes conclusiones clave:

### 1. El Factor Tiempo como Predictor de Éxito ⏱️
Se identificó una correlación positiva directa entre la duración de la llamada y la suscripción. Mientras que las llamadas de rechazo suelen durar menos de 3 minutos, las suscripciones exitosas requieren, en promedio, una interacción de **9.19 minutos**.
* **Insight**: El tiempo es una inversión necesaria; llamadas cortas son indicadores tempranos de falta de interés.

### 2. Punto de Saturación y Eficiencia Operativa 📞
El análisis del número de llamadas (`num_llam`) revela un rendimiento decreciente. La probabilidad de éxito alcanza su pico entre el 1er y 3er intento, luego la rentabilidad cae drásticamente.
* **Insight**: Contactar a un cliente más de 5 veces para la misma campaña reduce drásticamente el ROI y aumenta el riesgo de insatisfacción.

### 3. Perfil del Cliente Suscriptor 👤
* **Educación e Ingresos**: Existe una mayor propensión de compra en clientes con nivel educativo **Alto**, sugiriendo que el producto es percibido como una herramienta financiera sofisticada.
* **Carga Financiera**: El "Heatmap de Endeudamiento" mostró que los clientes sin préstamos personales previos tienen mayor liquidez y disposición para contratar nuevos servicios.

### 4. Comparativa de Campañas 📈
Al contrastar con la campaña previa, se observa que la eficiencia ha mejorado (**11.27%** de éxito frente a un **3.34%** previo). No obstante, este resultado debe tomarse con cautela, ya que la campaña previa contiene un 86% de datos catalogados como "inexistente", lo que cual hace una comparativa inconsistente desde un punto de vista estadístico.

## Recomendaciones de Negocio
Basado en el análisis realizado, se proponen las siguientes acciones estratégicas:
* **Limitar las llamadas a un máximo de 4 intentos** para optimizar el tiempo operativo y el ROI.
* **Priorizar la prospección de clientes sin deudas vigentes** (hipotecas o préstamos personales).
* Enfocar los esfuerzos comerciales en perfiles con un **nivel educativo medio-alto**, quienes muestran una respuesta más favorable al producto.

## Visualización de los Datos
El proyecto incluye visualizaciones avanzadas utilizando `Seaborn` y `Matplotlib`:
* **Histogramas y KDE**: Análisis de la distribución de edad e ingresos.
* **Boxplots Comparativos**: Detección de outliers en el esfuerzo comercial.
* **Heatmaps de Correlación**: Identificación de variables críticas en la decisión de suscripción.

## Tecnologías Utilizadas
* **Python 3.12**
* **Pandas & NumPy**: Manipulación y limpieza de datos.
* **Matplotlib & Seaborn**: Visualización estadística.
* **VS Code & Jupyter Notebook**: Entornos de desarrollo.

## 👨‍💻 Autor
**Rodrigo Antúnez**  
Economist & Data Analyst en formación, con manejo de Python, SQL & Herramientas BI.

🔗 GitHub: https://github.com/rgoantunez 
🔗 Repositorio del proyecto: