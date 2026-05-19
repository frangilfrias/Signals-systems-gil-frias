# Documentacion de RIR-API

## Estructura

Este directorio contiene la documentacion del proyecto. Se recomienda organizar los
archivos de la siguiente manera:

```
docs/
├── README.md              # Este archivo
├── teoria/                # Notas teoricas y referencias
│   ├── iso_3382.md        # Resumen de la norma ISO 3382
│   └── parametros.md      # Explicacion de EDT, T20, T30
├── mediciones/            # Reportes de mediciones realizadas
│   └── sala_ejemplo.md    # Informe de una medicion
└── imagenes/              # Graficos y diagramas generados
```

## API de referencia

Explorar la [documentacion interactiva de la API de la catedra](https://rir-api.onrender.com/docs)
para entender la estructura de endpoints, schemas y respuestas esperadas.

## Referencias utiles

- **ISO 3382-1:2009** — Acoustics — Measurement of room acoustic parameters.
- Farina, A. (2000). *Simultaneous measurement of impulse response and distortion
  with a swept-sine technique.*
- Schroeder, M. R. (1965). *New method of measuring reverberation time.*
  The Journal of the Acoustical Society of America.
- Lundeby, A. et al. (1995). *Uncertainties of measurements in room acoustics.*
  Acta Acustica.
- [FastAPI: documentacion oficial](https://fastapi.tiangolo.com/)
- [Pydantic: validacion de datos](https://docs.pydantic.dev/)

## Notas

Cada milestone deberia documentarse brevemente en este directorio, incluyendo:

1. Decisiones de diseno tomadas.
2. Resultados de validacion (graficos, tablas comparativas).
3. Problemas encontrados y como se resolvieron.


## Decisiones de diseño

El método para la generación del sine sweep fue dado por la fórmula matemática:

$$x(t) = \sin\left[\frac{2\pi f_1 T}{\ln(f_2/f_1)} \left(e^{t \ln(f_2/f_1)/T} - 1\right)\right]$$

Donde:
$f_1$ es la frecuencia inicial (Hz)
$f_2$ es la frecuencia final (Hz)
$T$ es la duracion total del sweep (s)
$t$ es el tiempo, con $0 \leq t \leq T$

Por lo tanto la señal generada tendrá crecimiento exponencial, lo que conlleva a que haya mayor cantidad de energía en las frecuencias cercanas a $f_1$ , esto se toma en cuenta al crear el filtro inverso.

Para generar el filtro inverso, se invirtió el sweep temporalmente y se corrigió la amplitud debido a la distribución no uniforme de la energía en el rango de frecuencias dado.

$$x_{inv}(t) = \frac{x(T - t)}{A(t)}$$

$$A(t) = e^{-t \ln(f_2/f_1)/T}$$

En la convolusión de la señal generada y el filtro inverso, se obtuvo un impulso con lóbulos al rededor del mismo con menor amplitud, energía. Este comportamiento valida el correcto funcionamiento  del algoritmo de generación y del proceso del filtrado.

Además, el código cuenta con validacio2n de datos de ingreso para que no haya ninguna ruptura en las funciones del mismo por valores no permitidos. Con respecto a la frecuencia de sampleo, se seleccionaron las frecuencias de: 44100 Hz, 48000 Hz, 88200 Hz, 96000 Hz, 176400 Hz, 192000, 352800 Hz, 384000 Hz, 705600 Hz, 768000 Hz , las cuales son las más utilizadas.

## Validación

Se validó manualmente la función de generación de sine sweep mediante dos métodos:

a. Inspección visual.
b. Comparación con una señal de sine sweep de referencia.

El barrido de frecuencias de referencia utilizado fue el generado por REW, con las características de:
- Barrido de 20 Hz a 20 KHz
- 5 segundos de duración
- Frecuencia de sampleo seteada a 44.1 KHz


## Resultados

Al graficar el sine sweep generado por nuestro algoritmo, pudimos verificar que cubre el rango de frecuencias especificado, presenta un barrido logarítmico continuo, con la distribución de energía no uniforme. Al convolucionar nuestra señal con el filtro inverso, la respuesta obtenida es una aproximación discreta del impulso de Dirac, es decir un pico temporal predominante acompañado de pequeños lóbulos

![Sine_sweep + Convolución](RIR_API/docs/IMÁGENES/Figure_1.png)
![Lóbulo principal](RIR_API/docs/IMÁGENES/Figure_2.png)

Al comparar la señal generada con la obtenida mediante el algoritmo comercial de referencia, puede observarse una distribución de energía espectral similar en todo el rango de frecuencias analizado.

![Espectrograma](RIR_API/docs/IMÁGENES/Captura de pantalla 2026-05-18 a la(s) 21.07.39.png)

## Problemas encontrados

Uno de los principales inconvenientes encontrados durante el desarrollo estuvo relacionado con la validación de parámetros de entrada y la implementación de los tests, ya que inicialmente varias pruebas no eran superadas correctamente por el código desarrollado.
Por lo tanto utilizamos la herramienta (chat gpt) y analizamos de manera crítica la solución brindada, en varias ocaciones se pidió que vuelva a formular el código debido a que no funcionaba de manera correcta.
Además se utilizó su ayuda para la generación de lo gráficos con sus descripciones.

