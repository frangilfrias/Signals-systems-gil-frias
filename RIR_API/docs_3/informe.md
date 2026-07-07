---
Título: "Desarrollo de un software para el cálculo de parámetros acústicos según la norma ISO 3382"
Asignatura: Señales y Sistemas, Ingeniería de Sonido
Autores: "Mora Sawczyk, Francisco Gil Frías, Matías Moreira"
Fecha: "07/07/2026"
---

# Desarrollo de un software para el cálculo de parámetros acústicos según la norma ISO 3382-1

---

## Resumen

Este documento presenta el desarrollo de una API RESTful orientada al cálculo de parámetros acústicos según la norma ISO 3382-1. El software diseñado procesa la respuesta al impulso para la obtención de parámetros acústicos por bandas de octava, tanto a través de la generación de un barrido senoidal, y el posterior procesamiento de la respuesta de la sala a través del correspondiente filtro inverso, como de la carga de archivos en formato wav que contienen señales de respuestas impulsivas. Por otra parte se incluye la posibilidad de generar ruido rosa.

**Keywords:** ISO 3382, acústica, respuesta impulsiva (RI), procesamiento digital de señales (DSP)

---

## 1. Introducción 

El análisis acústico de salas basado en la norma ISO 3382-1 [1], permite caracterizar su comportamiento a partir de la respuesta al impulso, considerando el recinto como un sistema lineal e invariante en el tiempo. RIR-API (Room Impulse Response Application Programming Interface), es una biblioteca de software implementada en lenguaje Python que reúne los algoritmos necesarios para la generación de señales de excitación, la obtención y procesamiento de respuestas impulsivas y el cálculo de parámetros acústicos objetivos.

Con el propósito de facilitar la integración del software con aplicaciones externas y desacoplar la lógica de procesamiento de la interfaz de usuario, las funcionalidades de RIR-API se exponen mediante una API RESTful. Esta interfaz permite acceder a los distintos servicios del sistema a través del protocolo HTTP, utilizando recursos y métodos estandarizados para la generación de señales, la carga y procesamiento de respuestas impulsivas y la obtención de resultados en formato JSON.

La combinación de una biblioteca especializada para el procesamiento digital de señales y una arquitectura basada en servicios REST proporciona una solución modular, escalable y reutilizable, permitiendo que el sistema pueda integrarse con interfaces web.

El software desarrollado automatiza el flujo completo de análisis acústico, desde la generación de la señal de excitación hasta la obtención de los principales parámetros definidos en [1], entre ellos EDT,T20 ,T30,D50 y C80, calculados por bandas de octava mediante filtros conformes a la norma IEC 61260-1 [2].

## 2 Objetivos
### 2.1 Generales
Desarrollar una biblioteca en Python para el procesamiento y análisis de señales acústicas, complementada con una API REST que permita acceder a sus funcionalidades de manera organizada, modular y reutilizable, aplicando buenas prácticas de ingeniería de software, validación mediante pruebas automatizadas y documentación técnica.

### 2.2 Particulares
Implementar funciones para la generación, adquisición y procesamiento de señales de audio.
Desarrollar algoritmos de análisis acústico basados en la norma ISO 3382 para la estimación de parámetros de reverberación.
Implementar filtros en bandas de octava y herramientas para el cálculo de la curva de decaimiento energético (EDC).
Exponer las funcionalidades de la biblioteca mediante una API REST utilizando FastAPI.
Verificar el correcto funcionamiento de cada módulo mediante pruebas unitarias y de integración.
Documentar el proyecto y mantener un flujo de desarrollo colaborativo utilizando Git y GitHub.

## 3. Marco teórico

La respuesta al impulso de un recinto (Room Impulse Response, RIR) describe el comportamiento acústico de un ambiente frente a una excitación impulsiva. A partir de ella es posible caracterizar objetivamente las propiedades acústicas del recinto mediante diferentes parámetros normalizados.

Para el análisis de la RIR, la señal se divide en bandas de octava utilizando filtros digitales, permitiendo evaluar el comportamiento en distintas frecuencias. Posteriormente, la envolvente energética de la respuesta se obtiene mediante la transformada de Hilbert y se aplica el método de Lundeby para estimar el punto donde la energía de la señal alcanza el nivel de ruido de fondo, evitando que éste afecte el cálculo de los parámetros.

La energía acumulada se determina mediante la integral de Schroeder, que genera la Energy Decay Curve (EDC). Sobre esta curva se realizan regresiones lineales en distintos intervalos de decaimiento para obtener parámetros como EDT, T10, T20, T30 y T60, representativos del tiempo de reverberación del recinto.

Además de los tiempos de reverberación, la API calcula parámetros relacionados con la inteligibilidad y la claridad del sonido, como D50 y C80, ampliamente utilizados en acústica arquitectónica y definidos por la norma ISO 3382. Estos indicadores permiten evaluar objetivamente la calidad acústica de un espacio a partir de su respuesta al impulso.

## 4. Desarrollo 

### 4.1 Arquitecura

En la figura 1 se observa el esquema del diseño de arquitectura del proyecto.

 ![Imagen 1 Diagrama de arquitectura](IMAGENES/ARQUITECTURA.png)

### 4.2 Diseño
La API fue desarrollada siguiendo una arquitectura modular basada en el framework FastAPI, separando claramente las responsabilidades de cada componente para facilitar el mantenimiento, la reutilización del código y la escalabilidad del proyecto.

El usuario interactúa con la aplicación mediante solicitudes HTTP dirigidas a los distintos endpoints. Cada endpoint pertenece a un router, encargado de definir las rutas disponibles y recibir los parámetros enviados por el cliente.

Antes de ejecutar cualquier procesamiento, los datos de entrada y salida son validados mediante schemas implementados con Pydantic. Esto asegura que la información recibida tenga el formato esperado y permite generar respuestas consistentes.

Una vez validados los datos, los routers delegan la lógica de procesamiento a los services, donde se implementan los distintos algoritmos de generación, procesamiento y análisis de señales acústicas. Esta separación permite mantener desacoplada la lógica de negocio de la capa de comunicación HTTP.

Los resultados obtenidos por los servicios son devueltos al router, que construye la respuesta utilizando los schemas correspondientes y la envía nuevamente al cliente en formato JSON.

De esta forma, el flujo general de la aplicación puede resumirse como:

Cliente → Endpoints → Routers → Schemas → Services → Respuesta JSON

Esta organización favorece la claridad del código, simplifica la incorporación de nuevas funcionalidades y facilita el desarrollo colaborativo al mantener cada componente con una responsabilidad específica.


### 4.3 Funciones
#### Generación de señales: 
*Pink noise*: 

*Sine sweep*: Con el objetivo de caracterizar completamente un sistema, la API implementa la generación de un barrido de senoidal logarítmico (sine sweep). Esta función genera tanto la señal de excitación como su filtro invers, necesario para su procesamiento posterior para recuperar la respuesta al impulso, a partir de la cual es posible calcular los distintos parámetros acústicos implementados en la API.

#### Reproducción y grabación: 
La función de reproducción y grabación permite reproducir una señal de audio a través del sistema de salida seleccionado mientras registra simultáneamente la respuesta capturada por un dispositivo de entrada. Su objetivo es obtener una grabación sincronizada de la señal emitida para posteriormente analizar la respuesta impulsiva (RIR) del recinto.

Internamente se encarga de configurar los dispositivos de audio, establecer la frecuencia de muestreo, controlar la duración de la adquisición y devolver la señal registrada en un arreglo numérico apto para su procesamiento posterior. Esta función constituye el punto de partida del flujo completo de medición acústica.

#### Cargar audio: 
La función de carga de audio permite importar un archivo de sonido almacenado en disco para incorporarlo al flujo de procesamiento del sistema.

Su propósito es obtener la señal digital y su frecuencia de muestreo, independientemente del origen del archivo, permitiendo trabajar posteriormente con filtros, cálculos energéticos y parámetros acústicos. Además, valida que el archivo exista y que el formato sea compatible con el procesamiento.

#### Obtener RI desde sweep:
La función de obtención de la respuesta al impulso permite recuperar la caracterización de un sistema a partir de la "deconvolusión" de la grabación de la respuesta del sistema al sine sweep y su filtro inverso, de esta manera elimina el efecto de la señal de excitación. 

Esta respuesta constituye la entrada para las etapas posteriores de procesamiento, permitiendo calcular los parámetros acústicos de acuerdo con la metodología implementada en la API.

#### Filtro de octava:

#### Convertir a escala logarítmica: 
La función de conversión a escala logarítmica transforma una señal expresada en escala lineal hacia decibeles (dB), utilizando una escala logarítmica.

Esta conversión resulta indispensable en acústica, ya que la percepción humana del sonido y la mayoría de los parámetros acústicos se expresan en decibeles. Además del cálculo logarítmico, la función contempla el tratamiento de valores cercanos a cero para evitar errores numéricos durante la operación.

#### Suavizar señal:

#### Integral de Schroeder:

#### Regresión lineal:
La función de regresión lineal calcula la recta que mejor aproxima un conjunto de datos mediante el método de mínimos cuadrados. Dentro del proyecto se utiliza principalmente para estimar los tiempos de reverberación (EDT, T10, T20 y T30) a partir de la curva de decaimiento energético obtenida mediante la integral de Schroeder.

Como resultado devuelve la pendiente, la ordenada al origen y el coeficiente de determinación (R²), el cual permite evaluar la calidad del ajuste realizado.

#### Calcular parámetros acústicos:
La función de cálculo de parámetros acústicos permite obtener los principales indicadores utilizados para caracterizar el comportamiento acústico de un recinto a partir de su respuesta al impulso.

Su propósito es calcular automáticamente los parámetros T10, T20, T30, T60, EDT, C80 y D50. Para ello, utiliza la curva de decaimiento energético obtenida mediante la integral de Schroeder y aplica una regresión lineal sobre los intervalos establecidos por la norma para estimar los distintos tiempos de reverberación. Los parámetros obtenidos constituyen el resultado final del análisis realizado por la API.

#### Método lundeby
La función implementa el método de Lundeby para estimar automáticamente el punto de truncamiento de una respuesta al impulso. A partir de este punto es posible separar el decaimiento útil del ruido de fondo, mejorando la precisión de los cálculos posteriores de la curva de decaimiento energético y de los parámetros acústicos.

#### RIR_API:
La API desarrollada expone mediante servicios HTTP las principales funcionalidades implementadas durante el proyecto, permitiendo ejecutar los algoritmos de procesamiento acústico sin necesidad de acceder directamente al código fuente.

Cada endpoint recibe los parámetros necesarios, ejecuta el procesamiento correspondiente y devuelve los resultados en formato JSON, facilitando la integración con otras aplicaciones o interfaces gráficas.

Entre los servicios disponibles se encuentran operaciones sobre señales, filtros, generación de curvas en escala logarítmica, suavizado, regresión lineal y cálculo de parámetros acústicos.

### 4.4 Tests

#### Generación de señales: 
***Pink noise***:

***Sine sweep***: Los tests verifican que la función genere correctamente el sine sweep y su filtro inverso; ambas señales tengan la longitud esperada; el barrido cubra el rango de frecuencias especificado; la frecuencia instantánea aumente de forma monótona; la convolución entre el sine sweep y su filtro inverso produzca una aproximación a un impulso; y se manejen correctamente parámetros inválidos, tanto de tipo como de valor.

#### Reproducción y grabación: 
Los tests verifican que la función complete correctamente el proceso de reproducción y grabación; la señal obtenida tenga la longitud esperada; la frecuencia de muestreo utilizada sea la indicada; el tipo de dato devuelto sea el correcto;
la función responda adecuadamente ante parámetros inválidos.

#### Cargar audio: 
Los tests verifican que el archivo pueda abrirse correctamente; la señal cargada tenga dimensiones válidas; la frecuencia de muestreo corresponda con la almacenada en el archivo; se detecten archivos inexistentes; se manejen correctamente errores de lectura.

#### Sintetizar RI: 

#### Obtener RI desde sweep:
Los tests verifican que la deconvolución entre la grabación del sine sweep y su filtro inverso permita recuperar correctamente la respuesta al impulso; el pico principal de la respuesta obtenida sea claramente identificable; la respuesta recuperada conserve una alta similitud con una respuesta al impulso sintetizada; y el proceso de obtención de la RI produzca resultados consistentes para su posterior análisis acústico.

#### Filtro de octava:

#### Convertir a escala logarítmica: 
Los tests verifican que la conversión produzca los valores esperados; la salida conserve la longitud de la señal original; no aparezcan valores indefinidos (NaN o infinito);
se manejen correctamente señales con energía muy baja o nula.

#### Suavizar señal:

#### Integral de Schroeder:

#### Regresión lineal:
Los tests verifican que la pendiente calculada sea correcta; la ordenada al origen corresponda con los datos utilizados; el coeficiente R² tenga el valor esperado; la función responda correctamente ante conjuntos de datos pequeños;
se detecten correctamente casos degenerados o inválidos.

#### Calcular parámetros acústicos:
Los tests verifican que los parámetros acústicos se calculen correctamente a partir de una respuesta al impulso sintetizada; el valor estimado de T30 sea consistente con el tiempo de reverberación utilizado para generar la señal; el parámetro D50 se encuentre dentro del rango físico esperado; y C80 presente valores coherentes para respuestas al impulso con la energía concentrada al comienzo.

#### Método lundeby
Los tests verifican que la función estime correctamente el punto de truncamiento de una respuesta al impulso; el índice obtenido se encuentre dentro de los límites de la señal; el algoritmo responda correctamente tanto para respuestas con decaimiento exponencial como para señales dominadas por ruido; y los resultados sean estables al procesar señales equivalentes.

#### RIR_API:
Los tests de la API verifican que cada endpoint responda correctamente a solicitudes válidas; los códigos de estado HTTP sean los esperados; las respuestas contengan la estructura JSON correcta; se validen adecuadamente los parámetros recibidos; se gestionen correctamente solicitudes inválidas o incompletas; los resultados devueltos coincidan con los obtenidos por las funciones internas del sistema.
            
## 5. Resultados
### 5.1 Gráficos
### 5.2 Tablas
### 5.3 Validación
## 6. Conclusiones
Se ha desarrollado el software RIR-API en lenguaje python capaz de generar la señal de excitación, registrar la respuesta del recinto, procesarla y otorgar los parámetros acústicos EDT, T20, T30, D50 y C80 por bandas de octava cumpliendo con las recomendaciones dadas en las normas ISO 3381-1 e IEC 60621-1.

## 7. Adversidades, confesiones y desafíos

### 7.1 Adversidades
El escaso o nulo conocimiento previo tanto del lenguaje de programación utilizado como de los sistemas asociados configuraron la mayor proporción de tiempo destinado al desarrollo del proyecto, restando una pequeña parte para el cumplimiento de los objetivos técnicos vinculados al análisis conceptual del procesamiento de señales.
        
### 7.2 Confesiones
Debido a las razones expuestas en 7.1, se ha recurrido sistemáticamente al vivecoding. 

### 7.3 Desafíos
Comprender en profundidad y adquirir agilidad en la implementación de las buenas prácticas vinculadas a la programación y al procesamiento digital de señales.


## Referencias

[1] ISO 3382-1:2009: Acoustics — Measurement of room acoustic       parametersPart 1: Spaces for music, speech and communication. (2009).

[2]IEC 60621-1:2014: Electroacoustics – Octave-band and fractional-octave-band filters –Part 1: Specifications. (2014).

[3]Fariña, A. . Simultaneous measurement of impulse response and distortion with a swept-sine technique. 108th AES Convention.(2000).