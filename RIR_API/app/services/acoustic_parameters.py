"""Servicio de calculo de parametros acusticos segun ISO 3382.

Milestone 3: Analisis de parametros acusticos.
"""

import numpy as np
from app.services.filter import filtro_octava
from app.services.signal_utils import a_escala_log

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


def calcular_parametros_acusticos(ri: np.ndarray, fs: int) -> dict[str, dict[float, float]]:
    """Calcula los parametros acusticos de una sala a partir de su RI para cada banda de octava.

    Parameters
    ----------
    ri : np.ndarray
        Respuesta al impulso (array 1D).
    fs : int
        Frecuencia de muestreo en Hz.

    Returns
    -------
    dict[str, dict[float, float]]
        Diccionario con los parametros acusticos por banda.

    References
    ----------
    .. [1] ISO 3382-1:2009. "Acoustics -- Measurement of room acoustic
       parameters -- Part 1: Performance spaces."
    """
    ri = np.asarray(ri, dtype=float)

    if ri.ndim != 1:
        raise ValueError("La respuesta al impulso debe ser un vector unidimensional.")

    if fs <= 0:
        raise ValueError("La frecuencia de muestreo debe ser mayor que cero.")

    # Bandas de octava normalizadas
    bandas = [125, 250, 500, 1000, 2000, 4000, 8000]

    parametros = {
        "EDT": {},
        "T10": {},
        "T20": {},
        "T30": {},
        "T60": {},
        "D50": {},
        "C80": {},
    }

    for fc in bandas:

        # Filtrado por banda de octava
        ri_filtrada = filtro_octava(
            signal=ri,
            fc=fc,
            fs=fs,
        )

        # Curva de Schroeder
        edc = integral_schroeder(ri_filtrada)
        edc_db = a_escala_log(edc)
        tiempo = np.arange(len(ri_filtrada)) / fs

        # Función auxiliar para EDT, T10, T20 y T30, para no escribir el mismo procedimiento
        # en todos los casos, simplemente toma los límites de cada parámetros y hace el cálculo.


        def calcular_rt(db_inicio: float, db_fin: float) -> float:

            indice_inicio = np.argmin(np.abs(edc_db - db_inicio))
            indice_fin = np.argmin(np.abs(edc_db - db_fin))

            if indice_fin <= indice_inicio:
                return np.nan

            pendiente, _, _ = regresion_lineal(
                tiempo[indice_inicio:indice_fin + 1],
                edc_db[indice_inicio:indice_fin + 1],
            )

            if pendiente >= 0:
                return np.nan

            return -60.0 / pendiente

        # Tiempos de reverberación
        edt = calcular_rt(0, -10)
        t10 = calcular_rt(-5, -15)
        t20 = calcular_rt(-5, -25)
        t30 = calcular_rt(-5, -35)

        # ISO 3382: normalmente se reporta T30 como T60
        t60 = t30 if not np.isnan(t30) else t20

        # Energía
        energia = ri_filtrada ** 2
        energia_total = np.sum(energia)

        if energia_total == 0:
            d50 = np.nan
            c80 = np.nan
        else:

            # D50
            n50 = min(int(round(0.050 * fs)), len(energia))
            energia_50 = np.sum(energia[:n50])
            d50 = 100 * energia_50 / energia_total

            # C80
            n80 = min(int(round(0.080 * fs)), len(energia))
            energia_80 = np.sum(energia[:n80])
            energia_tardia = np.sum(energia[n80:])

            c80 = (
                np.inf 
                if energia_tardia <= 0
                else 10 * np.log10(energia_80 / energia_tardia)
            )
        # Guardar resultados


        parametros["EDT"][fc] = float(edt)
        parametros["T10"][fc] = float(t10)
        parametros["T20"][fc] = float(t20)
        parametros["T30"][fc] = float(t30)
        parametros["T60"][fc] = float(t60)
        parametros["D50"][fc] = float(d50)
        parametros["C80"][fc] = float(c80)

    return parametros


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
