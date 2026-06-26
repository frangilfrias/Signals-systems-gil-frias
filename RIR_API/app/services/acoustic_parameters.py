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


def regresion_lineal(x: np.ndarray, y: np.ndarray) -> tuple[float, float, float]:
    """
    Calcula la regresion lineal por minimos cuadrados.

    Parameters
    ----------
    x : np.ndarray
        Variable independiente (tipicamente tiempo en segundos).
    y : np.ndarray
        Variable dependiente (tipicamente curva de Schroeder en dB).

    Returns
    -------
    tuple[float, float, float]
        (pendiente, ordenada_al_origen, r_cuadrado)
        pendiente en dB/s, ordenada en dB, coeficiente de determinacion.

    Raises
    ------
    ValueError
        Si los arrays tienen distinto largo o menos de 2 puntos.
    """
    x = np.asarray(x, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)

    if len(x) != len(y):
        raise ValueError(f"x e y deben tener el mismo largo. Got len(x)={len(x)}, len(y)={len(y)}")
    if len(x) < 2:
        raise ValueError("Se necesitan al menos 2 puntos para la regresion.")

    N = len(x)

    sum_x = np.sum(x)
    sum_y = np.sum(y)
    sum_xy = np.sum(x * y)
    sum_x2 = np.sum(x**2)

    denominador = N * sum_x2 - sum_x**2

    if denominador == 0:
        raise ValueError("Los valores de x son constantes, no se puede ajustar una recta.")

    m = (N * sum_xy - sum_x * sum_y) / denominador
    b = (sum_y - m * sum_x) / N

    y_pred = m * x + b
    y_media = np.mean(y)
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - y_media) ** 2)

    r_cuadrado = 1.0 - (ss_res / ss_tot) if ss_tot > 0 else 1.0

    return float(m), float(b), float(r_cuadrado)


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
    raise NotImplementedError("Implementar en Milestone 3 (opcional)")
