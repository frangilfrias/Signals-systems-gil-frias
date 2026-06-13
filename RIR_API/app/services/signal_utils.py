"""Utilidades de procesamiento de senales.

Milestone 2: Procesamiento de la respuesta al impulso.
"""

import numpy as np


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
