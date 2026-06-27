"""Servicio de calculo de parametros acusticos segun ISO 3382.

Milestone 3: Analisis de parametros acusticos.
"""

import numpy as np


def suavizar_signal(signal: np.ndarray, ventana: int) -> np.ndarray:
    """Aplica un suavizado por media movil a la senal.

    Parameters
    ----------
    signal : np.ndarray
        Senal de entrada (array 1D).
    ventana : int
        Tamano de la ventana de suavizado en muestras.

    Returns
    -------
    np.ndarray
        Senal suavizada, de la misma longitud que ``signal``.
    """
    raise NotImplementedError("Implementar en Milestone 3")


def integral_schroeder(ri: np.ndarray) -> np.ndarray:
    """Calcula la integral de Schroeder (Energy Decay Curve).

    Parameters
    ----------
    ri : np.ndarray
        Respuesta al impulso (array 1D).

    Returns
    -------
    np.ndarray
        Curva de decaimiento energetico (EDC), normalizada.

    References
    ----------
    .. [1] Schroeder, M. R. (1965). "New method of measuring reverberation
       time." The Journal of the Acoustical Society of America.
    """
    raise NotImplementedError("Implementar en Milestone 3")


def regresion_lineal(x: np.ndarray, y: np.ndarray) -> tuple[float, float]:
    """Calcula la regresion lineal por minimos cuadrados.

    Parameters
    ----------
    x : np.ndarray
        Variable independiente (array 1D).
    y : np.ndarray
        Variable dependiente (array 1D).

    Returns
    -------
    pendiente : float
        Pendiente de la recta ajustada (m).
    ordenada : float
        Ordenada al origen de la recta ajustada (b).
    """
    raise NotImplementedError("Implementar en Milestone 3")


def calcular_parametros_acusticos(ri: np.ndarray, fs: int) -> dict:
    """Calcula los parametros acusticos de una sala a partir de su RI.

    Parameters
    ----------
    ri : np.ndarray
        Respuesta al impulso (array 1D).
    fs : int
        Frecuencia de muestreo en Hz.

    Returns
    -------
    dict
        Diccionario con los parametros acusticos por banda.

    References
    ----------
    .. [1] ISO 3382-1:2009. "Acoustics -- Measurement of room acoustic
       parameters -- Part 1: Performance spaces."
    """
    raise NotImplementedError("Implementar en Milestone 3")


def metodo_lundeby(ri: np.ndarray, fs: int) -> int:
    """Estima el punto de truncamiento de la RI (metodo de Lundeby).

    Parameters
    ----------
    ri : np.ndarray
        Respuesta al impulso (array 1D).
    fs : int
        Frecuencia de muestreo en Hz.

    Returns
    -------
    int
        Indice de la muestra donde se estima el punto de truncamiento.

    Notes
    -----
    Esta funcion es **opcional** (extra credit).

    References
    ----------
    .. [1] Lundeby, A. et al. (1995). "Uncertainties of measurements in
       room acoustics." Acta Acustica.
    """
    ri = np.asarray(ri, dtype=float)

    if ri.ndim != 1:
        raise ValueError("RI debe ser 1D.")

    if len(ri) < 10:
        return len(ri) - 1

    # Energía y curva de Schroeder

    energia = ri ** 2
    energia = np.maximum(energia, np.finfo(float).eps)

    edc = np.cumsum(energia[::-1])[::-1]
    edc = edc / np.max(edc)

    edc_db = 10 * np.log10(edc)

    t = np.arange(len(ri)) / fs

    # Estimación inicial de ruido (últimos 10%)

    n = len(ri)
    n_ruido = max(int(0.1 * n), 10)

    ruido_db = 10 * np.log10(np.mean(energia[-n_ruido:]))

    indice_trunc = int(0.5 * n)

    # Iteraciones Lundeby

    for _ in range(5):

        nivel_corte = ruido_db + 10

        idx = np.where(edc_db <= nivel_corte)[0]

        if len(idx) == 0:
            break

        indice_trunc = idx[0]

        if indice_trunc < 5:
            break

        # regresión hasta el punto de cruce
        m, b = np.polyfit(t[:indice_trunc], edc_db[:indice_trunc], 1)

        # estimación de la curva
        fit = m * t + b

        residuo = edc_db - fit

        ruido_db = np.mean(residuo[-n_ruido:])

    # Cruce final con el nivel de ruido

    fit_final = m * t + b

    diff = fit_final - ruido_db

    cruces = np.where(diff <= 0)[0]

    if len(cruces) == 0:
        return len(ri) - 1

    return int(cruces[0])
