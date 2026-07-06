---
Título: "Desarrollo de un software para el cálculo de parámetros acústicos según la norma ISO 3382"
Asignatura: Señales y Sistemas, Ingeniería de Sonido
Autores: "Mora Sawczyc, Francisco Gil Frías, Matías Moreira"
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
    2.1 Generales

    2.2 Particulares


## 3. Marco teórico
## 4. Desarrollo 

    4.1 Arquitecura

    En la figura 1 se observa el esquema del diseño de arquitectura del proyecto.

 ![Imagen 1 Diagrama de arquitectura](IMAGENES/ARQUITECTURA.png)

    4.2 Diseño
        Cliente
        Routers
        Schemas
        Servirces
        Endpoints


    4.3 Funciones
        Generación de señales
        Reproducción y grabación
        Cargar audio
        Sintetizar RI
        Obtener RI desde sweep
        Filtro de octava
        Convertir a escala logarítmica
        Suavizar señal
        Integral de Schroeder
        Regresión lineal
        Calcular parámetros acústicos
        RIR_API
    4.4 Tests
            
## 5. Resultados
    5.1 Gráficos
    5.2 Tablas
    5.3 Validación
## 6. Conclusiones
    Se ha desarrollado el software RIR-API en lenguaje python capaz de generar la señal de excitación, registrar la respuesta del recinto, procesarla y otorgar los parámetros acústicos EDT, T20, T30, D50 y C80 por bandas de octava cumpliendo con las recomendaciones dadas en las normas ISO 3381-1 e IEC 60621-1.

## 7. Adversidades, confesiones y desafíos

    7.1 Adversidades
        El escaso o nulo conocimiento previo tanto del lenguaje de programación utilizado como de los sistemas asociados configuraron la mayor proporción de tiempo destinado al desarrollo del proyecto, restando una pequeña parte para el cumplimiento de los objetivos técnicos vinculados al análisis conceptual del procesamiento de señales.
        
    7.2 Confesiones
        Debido a las razones expuestas en 7.1, se ha recurrido sistemáticamente al vivecoding. 

    7.3 Desafíos
        Comprender en profundidad y adquirir agilidad en la implementación de las buenas prácticas vinculadas a la programación y al procesamiento digital de señales.




## 8. Trabajo futuro
    8.1 RI sintética

    8.2 Filtros
    8.3 Parámetros
    8.4 Front end


## Referencias

    [1] ISO 3382-1:2009: Acoustics — Measurement of room acoustic       parametersPart 1: Spaces for music, speech and communication. (2009).

    [2]IEC 60621-1:2014: Electroacoustics – Octave-band and fractional-octave-band filters –Part 1: Specifications. (2014).

    [3]Fariña, A. . Simultaneous measurement of impulse response and distortion with a swept-sine technique. 108th AES Convention.(2000).