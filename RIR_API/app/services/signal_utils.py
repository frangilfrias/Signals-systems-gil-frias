"""Utilidades de procesamiento de senales.

Milestone 2: Procesamiento de la respuesta al impulso.
"""

import numpy as np
from scipy.signal import fftconvolve
import soundfile as sf
from pathlib import Path
from app.services.filter import filtro_octava


def a_escala_log(signal: np.ndarray) -> np.ndarray:
    """Convierte una señal a escala logaritmica normalizada (dB).

    Parameters
    ----------
    signal : np.ndarray
        Señal de entrada (valores lineales).

    Returns
    -------
    np.ndarray
        Señal en decibeles, normalizada respecto al valor maximo.
        El maximo queda en 0 dB. Piso de ruido en -120 dB.

    """
    safe = np.where(signal == 0, np.finfo(float).eps, np.abs(signal))
    resultado = 20 * np.log10(safe / np.max(safe))
    return np.maximum(resultado, -120.0)


def sintetizar_ri(
        t60_por_banda: dict[float, float],
        fs: int, duracion: float
) -> np.ndarray:
    """Sintetiza una respuesta al impulso artificial
    a partir de valores T60 por banda.

    Parameters
    ----------
    t60_por_banda : dict[float, float]
        Diccionario {frecuencia_central_Hz: T60_segundos}.
    fs : int
        Frecuencia de muestreo en Hz.
    duracion : float
        Duracion de la respuesta al impulso en segundos.

    Returns
    -------
    np.ndarray
        Respuesta al impulso sintetizada (array 1D).
    """

    n = int(fs * duracion)
    t = np.linspace(0, duracion, n, endpoint=False)

    rir_total = np.zeros(n)
    eps = 1e-12

    for fc, t60 in t60_por_banda.items():
        if t60 <= 0:
            continue

        # Ruido blanco por banda de octava
        ruido = np.random.randn(n)

        # Filtrado en banda de octava
        ruido_banda = filtro_octava(
            signal=ruido,
            fc=fc,
            fs=fs,
            orden=4,
        )
        # Normalización del rudio filtrado por cada banda
        ruido_banda_rms = np.sqrt(np.mean(ruido_banda**2))

        ruido_banda_norm = ruido_banda / (ruido_banda_rms + eps)

        # Envolvente exponencial según T60
        alpha = 6.91 / t60
        envolvente = np.exp(-alpha * t)

        banda = ruido_banda_norm * envolvente

        # Suma de contribuciones
        rir_total += banda

        # Normalización final
    rir_total /= np.max(np.abs(rir_total)) + eps

    return rir_total


def obtener_ri_desde_sweep(
        grabacion: np.ndarray,
        filtro_inverso: np.ndarray
) -> np.ndarray:
    """Obtiene la respuesta al impulso mediante deconvolucion de un sine sweep.
     """
    # Validación de datos
    if len(grabacion) == 0:
        raise ValueError("grabacion no puede estar vacia")

    if len(filtro_inverso) == 0:
        raise ValueError("filtro_inverso no puede estar vacio")

    # Obtengo la rta al impulso convolucionando la señal con el filtro inverso
    ri = fftconvolve(
        grabacion,
        filtro_inverso,
        mode="full"
    )

    # Busco la posición del valor pico absoluto = llegada directa de la señal
    idx_pico = np.argmax(np.abs(ri))

    # Establezco un margen para el recorte, y recorto la señal
    margen = 100
    inicio = max(0, idx_pico - margen)
    ri = ri[inicio:]

    # Busco la máxima amplitud de mi señal para normalizarla
    pico = np.max(np.abs(ri))

    if pico > 0:
        ri = ri / pico

    return ri


def cargar_audio(ruta: str | Path) -> tuple[np.ndarray, int]:
    """
    Carga un archivo de audio WAV o FLAC.

    Parameters
    ----------
    ruta : str | Path
        Ruta al archivo de audio.

    Returns
    -------
    tuple[np.ndarray, int]
        Tupla con (senal, frecuencia_de_muestreo).
        La senal se devuelve como float64 normalizada entre -1 y 1.
        Si el audio es estereo, shape = (n_muestras, n_canales).

    Raises
    ------
    FileNotFoundError
        Si el archivo no existe.
    ValueError
        Si el formato no es soportado (solo WAV o FLAC).
    """
    ruta = Path(ruta)

    if not ruta.exists():
        raise FileNotFoundError(f"No se encontro el archivo: {ruta}")

    extension = ruta.suffix.lower()
    if extension not in (".wav", ".flac"):
        raise ValueError(f"Formato '{extension}' no soportado. Usar WAV o FLAC.")

    senal, sample_rate = sf.read(ruta, dtype="float64")

    maximo = np.max(np.abs(senal))
    if maximo > 0:
        senal = senal / maximo

    return senal, sample_rate
