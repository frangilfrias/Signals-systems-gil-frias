"""Servicio de filtrado por bandas de octava.

Milestone 2: Procesamiento de la respuesta al impulso.
"""

import numpy as np
from scipy import signal as sig


def filtro_octava(
    signal: np.ndarray,
    fc: float,
    fs: int,
    orden: int = 4,
) -> np.ndarray:

    # Frecuencias de corte
    f_low = fc / np.sqrt(2)
    f_high = fc * np.sqrt(2)

    # Validación de la frecuencia de corte superior
    if f_high >= fs / 2:
        raise ValueError("Frecuencia de corte superior superpuesta con fs")

    # Diseño del filtro pasabanda
    sos = sig.butter(
        orden,
        [f_low, f_high],
        btype="bandpass",
        fs=fs,
        output="sos",
    )

    # Aplicación del filtro pasa banda
    signal_filtrada = sig.sosfiltfilt(
        sos,
        signal,
    )

    return signal_filtrada
