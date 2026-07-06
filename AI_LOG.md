# AI Log

Registro de consultas realizadas a herramientas de IA durante el desarrollo del proyecto. Se utilizaron las siguientes inteligencias artificiales: ChatGPT y Claude.

---

# M0

### Consulta 1

Pregunta: ¿Cómo organizar la estructura inicial del proyecto y el repositorio?

Respuesta: Se brindó orientación sobre la organización de carpetas, estructura del proyecto y uso inicial de Git.


### Consulta 2

Pregunta: ¿Cómo documentar el proyecto utilizando Markdown?

Respuesta: Se explicó cómo estructurar archivos README y la documentación técnica utilizando Markdown.

### Consulta 3

Pregunta: ¿Cómo organizar la estructura inicial del proyecto y su documentación?

Respuesta: Se brindó orientación sobre la estructura del repositorio, organización de carpetas y documentación utilizando README y archivos auxiliares.

---

# M1

### Consulta 1

Pregunta: ¿Cómo implementar y validar funciones de procesamiento de señales?

Respuesta: Se explicó el funcionamiento de distintas funciones de procesamiento y se propusieron casos de prueba para su validación.

### Consulta 2

Pregunta: ¿Cómo interpretar resultados de ejercicios y cálculos relacionados con señales?

Respuesta: Se resolvieron ejercicios paso a paso y se explicaron los fundamentos matemáticos utilizados.

### Consulta 3

Pregunta: ¿Cómo mejorar la documentación del proyecto?

Respuesta: Se realizaron sugerencias sobre la estructura del README y la organización de la documentación técnica.

### Consulta 4

Pregunta: ¿Cómo trabajar colaborativamente utilizando Git y GitHub?

Respuesta: Se explicó el uso de ramas de desarrollo, git pull --rebase, resolución de conflictos y buenas prácticas para mantener un historial limpio.

---

# M2

### Consulta 1

Pregunta: ¿Cómo implementar y validar filtros por bandas de octava?

Respuesta: Se brindó asistencia para comprender el funcionamiento de los filtros y generar gráficos para verificar su respuesta.

### Consulta 2

Pregunta: ¿Cómo representar resultados mediante gráficos?

Respuesta: Se desarrollaron scripts utilizando Matplotlib para visualizar señales y respuestas de filtros.

### Consulta 3

Pregunta: ¿Cómo organizar la arquitectura del proyecto?

Respuesta: Se colaboró en la elaboración de diagramas de arquitectura y esquemas de módulos del sistema.

### Consulta 4

Pregunta: ¿Cómo resolver problemas relacionados con Git y VS Code?

Respuesta: Se ayudó a resolver conflictos de ramas, diferencias entre versiones y problemas de configuración del entorno de desarrollo.

---


# M3

### Consulta 1

**Pregunta:** ¿Cómo generar gráficos de la curva de Schroeder utilizando la respuesta al impulso de la API?

**Respuesta:** Se adaptó un script para utilizar la RI sintética generada por la API, aplicando filtrado por bandas, integral de Schroeder y regresión para T30.

---

### Consulta 2

**Pregunta:** ¿Cómo hacer que los gráficos tengan un formato similar al utilizado en la documentación de filtros?

**Respuesta:** Se configuró un estilo común para Matplotlib, ajustando tipografías, grillas, escalas y formato general de las figuras.

---

### Consulta 3

**Pregunta:** ¿Cómo implementar un pipeline completo de validación acústica?

**Respuesta:** Se construyó un script que ejecuta el flujo: filtrado por octava → suavizado → método de Lundeby → integral de Schroeder → cálculo de EDT, T20 y T30.

---

### Consulta 4

**Pregunta:** ¿Cómo utilizar una respuesta al impulso real en lugar de una sintética?

**Respuesta:** Se modificó el script para cargar archivos WAV utilizando SoundFile y procesarlos con el mismo pipeline de análisis.

---

### Consulta 5

**Pregunta:** ¿Cómo evitar que los scripts y archivos de validación formen parte del repositorio?

**Respuesta:** Se creó una carpeta local para validaciones y se agregó al `.gitignore` para mantener el desarrollo fuera del control de versiones.

---

### Consulta 6

**Pregunta:** ¿Cómo resolver errores relacionados con rutas, guardado de gráficos y ejecución de scripts?

**Respuesta:** Se corrigieron rutas de salida, creación automática de directorios y la ubicación correcta desde donde ejecutar los scripts.

---

### Consulta 7

**Pregunta:** ¿Cómo crear una Release en GitHub con un changelog resumido?

**Respuesta:** Se preparó un changelog con las funcionalidades principales implementadas y las correcciones realizadas para publicar la versión v1.0.0.

---

### Consulta 8

**Pregunta:** ¿Cómo resolver problemas durante el merge y la ejecución de la API?

**Respuesta:** Se identificaron problemas de rama y directorio de ejecución, indicando el procedimiento para realizar el merge correctamente y ejecutar Uvicorn desde la carpeta del proyecto.

---

### Consulta 9

Pregunta: ¿Cómo implementar el método de Lundeby para determinar el punto de truncamiento de una respuesta al impulso?

Respuesta: Se explicó el algoritmo iterativo, su validación y se propusieron mejoras para depurar la implementación.

---

### Consulta 10

Pregunta: ¿Cómo implementar la Integral de Schroeder?

Respuesta: Se explicó el cálculo de la Energy Decay Curve (EDC), la integración acumulativa inversa y su normalización.

---

# Temas de consulta frecuentes

Método de Lundeby.

Integral de Schroeder.

Conversión a escala logarítmica.

Documentación técnica.

Git y GitHub.

NumPy y estilo de documentación.

Norma ISO 3382 y parámetros acústicos.

Calidad y organización del código.