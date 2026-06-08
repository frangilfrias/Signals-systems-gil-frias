"""Utilidades de procesamiento de senales.

Milestone 2: Procesamiento de la respuesta al impulso.
"""

import numpy as np
from scipy.signal import fftconvolve

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


def sintetizar_ri(
    t60_por_banda: dict[float, float], fs: int, duracion: float
) -> np.ndarray:
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
    raise NotImplementedError("Implementar en Milestone 2")


def obtener_ri_desde_sweep(
    grabacion: np.ndarray, filtro_inverso: np.ndarray
) -> np.ndarray:
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
    # Validación de datos
    if len(grabacion) == 0:
        raise ValueError("grabacion no puede estar vacia")

    if len(filtro_inverso) == 0:
        raise ValueError("filtro_inverso no puede estar vacio")
    
    # Obtengo la rta al impulso convolucionando la señal grabada con el filtro inverso
    ri = fftconvolve(
        grabacion,
        filtro_inverso,
        mode="full"
    )

    # Busco la posición del valor pico absoluto = llegada directa de la señal
    idx_pico = np.argmax(np.abs(ri))

    #Establezco un margen para el recorte, y recorto la señal
    margen = 100
    inicio = max(0,idx_pico - margen)
    ri = ri[inicio:]
    
    # Busco la máxima amplitud de mi señal para normalizarla
    pico = np.max(np.abs(ri))

    if pico > 0:
        ri = ri / pico

    return ri


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
