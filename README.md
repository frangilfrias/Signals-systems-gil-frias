# API REST 
## RIR-API es una API RESTful desarrollada en Python utilizando el framework **FastAPI**. Su objetivo principal es el cálculo de parámetros acústicos de salas a partir de Respuestas al Impulso (RI), siguiendo estrictamente los lineamientos de la norma internacional **ISO 3382** (UNE-EN ISO 3382, 2010).

## Integrantes del equipo
* Mora Sawczyk - Legajo 79832 
* Matias Moreira - Legajo 29222
* Francisco Gil Frias - Legajo 50070 

## Instrucciones 
Una vez desarrollada la API vamos a dejar los comandos CURL para ejecutarla 


## Estructura 
RIR-API/
├── app/
│   ├── __init__.py
│   ├── main.py              # Punto de entrada con CORS y routers
│   ├── settings.py          # Configuración extendida
│   ├── exceptions.py        # Excepciones personalizadas (AnalysisError)
│   ├── utils.py             # Validación y utilidades
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── enums.py         # BandwidthType enum
│   │   └── responses.py     # Modelos Pydantic de respuesta
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── analysis.py      # Endpoints /api/v1/analysis/
│   │   └── health.py        # Health check
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── signal_utils.py      # Utilidades para análisis de señales
│   │   ├── acoustic_parameters.py # Cálculo de parámetros acústicos
│   │   ├── filter.py            # Filtros de banda (octava/tercio)
│   │   ├── pink_noise.py        # Generación de ruido rosa
│   │   └── sine_sweep.py        # Generación de sine sweeps
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Fixtures de pytest
│   ├── test_api.py          # Tests de API
│   └── test_services.py     # Tests de servicios
│
├── run.py                   # Script de ejecución rápida
├── requirements.txt
└── README.md

## Branching strategy 
Para este proyecto vamos a adoptar una estrategia en la cual vamos a desarrollar en la rama Develop para poder subir nuestros cambios en simultáneo y de paso que nos sirva como entorno de pruebas, usando así la rama MAIN para los procesos productivos.     

## Instalación 
git clone https://github.com/frangilfrias/Signals-systems-gil-frias.git
cd Signals-systems-gil-frias
cuando terminemos los requirements acá va a ir el pip install
ejecutar API 
