# RIR-API

API REST para procesamiento y analisis de respuestas al impulso según la norma ISO 3382.

<!-- Badges -->
![CI](../../actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.12+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Descripción

RIR-API es una API RESTful desarrollada en Python utilizando el framework **FastAPI**. Su objetivo principal es el cálculo de parámetros acústicos (EDT, T20, T30, T60, D50, C80) de salas a partir de Respuestas al Impulso (RI), siguiendo estrictamente los lineamientos de la norma internacional ISO 3382-1.

## Integrantes del equipo
* Mora Sawczyk - Legajo 79832 (Procesamiento de señales)
* Matias Moreira - Legajo 29222 (Generación de señales/Docs)
* Francisco Gil Frias - Legajo 50070 (Testing/CI) 

## Branching strategy 
Para el presente proyecto se adopta una estrategia en la cual el desarrollo presenta efectos solamente en la rama Develop, con el objetivo de realizar las modificaciones simultáneamente y que sea útil en el entorno de pruebas, reservando la rama MAIN para los procesos productivos.  

## Requisitos previos

- Python 3.12 o superior
- [uv](https://docs.astral.sh/uv/) (gestor de paquetes y entornos virtuales)
- [git](https://git-scm.com/install) (herramienta para controlar versiones de código)

## Instalación 

```bash
# Clonar el repositorio
git clone https://github.com/frangilfrias/Signals-systems-gil-frias.git
cd RIR_API

# Crear entorno virtual e instalar dependencias
uv venv
uv pip install -e ".[dev]"
```

## Ejecución

```bash
# Iniciar la API con hot-reload
uvicorn app.main:app --reload

# O usando el modulo directamente
python -m app.main
```
Para no tener problemas levantando la api, los comandos que sean con uvicorn hay que forzarlos a trabajar con el entorno virtual (venv) escribiendo:

"uv run uvicorn [...]"

La API estará disponible en `http://127.0.0.1:8000`. Documentación interactiva en:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Estructura del proyecto

```
RIR_API/
├── app/
│   ├── __init__.py
│   ├── main.py                    # Punto de entrada FastAPI
│   ├── routers/
│   │   ├── health.py              # GET /health
│   │   ├── signals.py             # Endpoints de generacion (M1 → M3)
│   │   ├── filters.py             # Endpoints de filtrado (M2 → M3)
│   │   ├── acoustics.py           # Endpoints de analisis (M3)
│   │   └── utils.py               # Endpoints de utilidades (M3)
│   ├── schemas/
│   │   └── ...                    # Modelos Pydantic de request/response
│   └── services/
│       ├── pink_noise.py          # Generacion de ruido rosa (M1)
│       ├── sine_sweep.py          # Generacion de sine sweep (M1)
│       ├── signal_utils.py        # Utilidades de procesamiento (M2)
│       ├── filter.py              # Filtros de banda de octava (M2)
│       └── acoustic_parameters.py # Parametros acusticos ISO 3382 (M3)
├── tests/
│   ├── test_generacion.py         # Tests de generacion (M1)
│   ├── test_procesamiento.py      # Tests de procesamiento (M2)
│   ├── test_analisis.py           # Tests de analisis (M3)
│   └── test_api.py                # Tests de endpoints (M3)
├── docs/                          # Documentacion
├── .github/workflows/ci.yml       # Integracion continua
├── pyproject.toml                 # Configuracion del proyecto
└── README.md
```

## Diagrama de arquitectura
```mermaid
flowchart LR

  subgraph Core["Capa principal"]
    Cliente["Cliente<br/>HTTP (request)"]
    Routers["Routers<br/>ENDPOINTS"]
    Schemas["Schemas<br/>PYDANTIC (validación)"]
    Services["Services<br/>LÓGICA"]
  end

  subgraph Modules["Modulos"]
    M0["M0<br/>Armado / Estructuración"]
    M1["M1<br/>Generación"]
    M2["M2<br/>Procesamiento"]
    M3["M3<br/>Análisis"]
  end

  Cliente --> Routers
  Routers --> Services
  Schemas -.-> Routers
  Services --> M0
  Services --> M1
  Services --> M2
  Services --> M3
```
## Milestones

### M0 — Setup del entorno
**Fecha:** Semana 5

- [ ] Hacer fork del repositorio template.
- [ ] Clonar el fork y verificar que el entorno se instala correctamente.
- [ ] Ejecutar la API: `uvicorn app.main:app --reload`.
- [ ] Verificar que `/health` responde correctamente.
- [ ] Ejecutar los tests (todos deben fallar con `NotImplementedError` excepto los de API).
- [ ] Verificar que el CI funciona en GitHub Actions.

### M1 — Generacion de senales
**Fecha:** Semana 8

- [ ] Implementar `generar_ruido_rosa()` en `app/services/pink_noise.py`.
- [ ] Implementar `generar_sine_sweep()` en `app/services/sine_sweep.py`.
- [ ] Implementar `reproducir_y_grabar()`.
- [ ] Todos los tests de `test_generacion.py` deben pasar.

### M2 — Procesamiento de senales
**Fecha:** Semana 12

- [ ] Implementar `cargar_audio()` en `app/services/signal_utils.py`.
- [ ] Implementar `obtener_ri_desde_sweep()` en `app/services/signal_utils.py`.
- [ ] Implementar `filtro_octava()` en `app/services/filter.py`.
- [ ] Implementar `a_escala_log()` en `app/services/signal_utils.py`.
- [ ] Implementar `sintetizar_ri()` para validacion.
- [ ] Todos los tests de `test_procesamiento.py` deben pasar.

### M3 — API REST y analisis de parametros acusticos
**Fecha:** Semana 15

- [ ] Implementar `integral_schroeder()` en `app/services/acoustic_parameters.py`.
- [ ] Implementar `regresion_lineal()` en `app/services/acoustic_parameters.py`.
- [ ] Implementar `calcular_parametros_acusticos()` en `app/services/acoustic_parameters.py`.
- [ ] Crear routers y schemas para exponer toda la funcionalidad como API REST.
- [ ] Todos los tests de `test_analisis.py` y `test_api.py` deben pasar.
- [ ] (Opcional) Implementar `metodo_lundeby()`.

## Como correr los tests

```bash
# Ejecutar todos los tests
uv run pytest -v

# Ejecutar tests de un modulo especifico
uv run pytest tests/test_generacion.py -v

# Ejecutar tests de la API
uv run pytest tests/test_api.py -v

# Ejecutar tests con reporte de cobertura
uv run pytest --tb=short
```

## Como correr el linter

```bash
# Verificar estilo de codigo
uv run ruff check app/ tests/

# Corregir automaticamente lo que se pueda
uv run ruff check --fix app/ tests/

# Formatear el codigo
uv run ruff format app/ tests/
```

## Licencia

Este proyecto esta licenciado bajo la Licencia MIT. Ver el archivo `LICENSE` para mas detalles.
