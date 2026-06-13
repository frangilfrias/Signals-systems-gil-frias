"""Utilidades de procesamiento de senales.

Milestone 2: Procesamiento de la respuesta al impulso.
"""

from pathlib import Path

import numpy as np
import soundfile as sf


def a_escala_log(signal: np.ndarray) -> np.ndarray:
    """
    Convierte una senal a escala logaritmica normalizada (dB).

    Parameters
    ----------
    signal : np.ndarray
        Senal de entrada (valores lineales).

    Returns
    -------
    np.ndarray
        Senal en decibeles, normalizada respecto al valor maximo.
        El maximo queda en 0 dB. Piso de ruido en -120 dB.
    """
    safe = np.where(signal == 0, np.finfo(float).eps, np.abs(signal))
    resultado = 20 * np.log10(safe / np.max(safe))
    return np.maximum(resultado, -120.0)
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
