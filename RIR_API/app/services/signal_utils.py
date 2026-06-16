"""Utilidades de procesamiento de senales.

Milestone 2: Procesamiento de la respuesta al impulso.
"""

import numpy as np

from app.services.filter import filtro_octava


def cargar_audio(ruta: str) -> tuple[np.ndarray, int]:
    """Carga un archivo de audio y retorna la senal y la frecuencia de muestreo.

    Parameters
    ----------
    ruta : str
        Ruta al archivo de audio a cargar.

    Returns
    -------
    signal : np.ndarray
        Senal de audio como array 1D (mono).
    fs : int
        Frecuencia de muestreo del archivo en Hz.

    Raises
    ------
    FileNotFoundError
        Si el archivo especificado no existe.
    """
    raise NotImplementedError("Implementar en Milestone 2")


def sintetizar_ri(t60_por_banda: dict[float, float], fs: int, duracion: float) -> np.ndarray:
    """Sintetiza una respuesta al impulso artificial a partir de valores T60 por banda.

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
    EPS = 1e-12

    for fc, t60 in t60_por_banda.items():
        print(f"Procesando banda {fc} Hz")
        if t60 <= 0:
            continue

        # a) ruido blanco POR BANDA (correcto según consigna)
        ruido = np.random.randn(n)

        # b) filtrado en banda de octava
        ruido_banda = filtro_octava(
            signal=ruido,
            fc=fc,
            fs=fs,
            orden=4,
        )
        # c) Normalización del rudio filtrado por cada banda
        ruido_banda_rms = np.sqrt(np.mean(ruido_banda**2))

        ruido_banda_norm = ruido_banda / (ruido_banda_rms + EPS)

        # d) envolvente exponencial según T60
        alpha = 6.91 / t60
        envolvente = np.exp(-alpha * t)

        banda = ruido_banda_norm * envolvente

        # suma de contribuciones
        rir_total += banda

        # d) normalización final
    rir_total /= np.max(np.abs(rir_total)) + EPS

    return rir_total


def obtener_ri_desde_sweep(grabacion: np.ndarray, filtro_inverso: np.ndarray) -> np.ndarray:
    """Obtiene la respuesta al impulso mediante deconvolucion de un sine sweep.

    Parameters
    ----------
    grabacion : np.ndarray
        Senal grabada que contiene la respuesta de la sala al sweep.
    filtro_inverso : np.ndarray
        Filtro inverso del sweep utilizado.

    Returns
    -------
    np.ndarray
        Respuesta al impulso estimada, normalizada.
    """
    raise NotImplementedError("Implementar en Milestone 2")


def a_escala_log(signal: np.ndarray) -> np.ndarray:
    """Convierte una senal a escala logaritmica (dB) normalizada.

    Parameters
    ----------
    signal : np.ndarray
        Senal de entrada (array 1D).

    Returns
    -------
    np.ndarray
        Senal en escala logaritmica (dB), normalizada a 0 dB en el maximo.
    """
    raise NotImplementedError("Implementar en Milestone 2")
