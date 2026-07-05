---
Título: "Desarrollo de software para el cálculo de parámetros acústicos ISO 3382"
Asignatura: Señales y Sistemas, Ingeniería de Sonido
Autores: "Mora Sawczyc, Francisco Gil Frías, Matías Moreira"
Fecha: "07/07/2026"
---

# Desarrollo de software para el cálculo de parámetros acústicos ISO 3382

---

## Resumen

Este documento presenta el desarrollo de un software RIR-API orientado al cálculo de parámetros acústicos según la norma ISO 3382-1. El objetivo principal es automatizar el análisis de respuestas impulsivas de recintos para la obtención de parámetros acústicos a través de la generación de un barrido senoidal como señal de excitación, y el procesamiento de la respuesta a través del correspondeinte filtro inverso. Por otra parte se ha diseñado un generador de ruido rosa y un banco de filtros de octava según la norma IEC 61260:2014.

**Keywords:** ISO 3382, acústica, respuesta impulsiva,IR, procesamiento digital de señales, DSP

---

## 1. Introducción y objetivos

El análisis acústico de salas mediante la norma ISO 3382 permite caracterizar el comportamiento sonoro de espacios cerrados a partir de la respuesta impulsiva. Este trabajo aborda el desarrollo de un software capaz de procesar señales acústicas y extraer parámetros objetivos de calidad sonora.

## 2. Marco teórico
## 3. Desarrollo 

    3.1 Arquitecura

        En la figura 1 se observa el esquema del diseño de arquitectura del proyecto.

 ![Imagen 1 Diagrama de arquitectura](IMAGENES/ARQUITECTURA.png)

        3.2 Diseño
            Cliente
            Routers
            Schemas
            Servirces
            Endpoints


        3.3 Funciones
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
        3.4 Tests
            
## 4. Resultados
    4.1 Gráficos
    4.2 Tablas
    4.3 Validación
## 5. Conclusiones
        5.1 Generales
            Se ha desarrollado un software RIR-API en lenguaje python capaz de generar la señal de excitación, registrar la respuesta del recinto, procesarla y otorgar los parámetros acústicos EDT, T20, T30, D50 y C80 por bandas de octava cumpliendo con las recomendaciones dadas en las normas ISO 3381-1 e IEC 60621-1.
        5.2 Particulares
            Complicaciones
            Desafíos


## 6. Trabajo futuro
        6.1 RI sintética
        6.2 Filtros
        6.3 Parámetros
        6.4 Front end
        

## Referencias

- ISO 3382-1: Acoustics — Measurement of room acoustic parameters
- IEC 60621-1:2014: Electroacoustics – Octave-band and fractional-octave-band filters –Part 1: Specifications
- Fariña: Acá va el papper del sweep (incluir en la sección del marco teórico)