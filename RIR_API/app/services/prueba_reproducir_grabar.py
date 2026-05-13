import numpy as np
import sounddevice as sd

from app.services.reproducir_grabar import reproducir_y_grabar

sd.default.device = (1, 4)


fs = 44100
duracion = 2.0
duracion_grabacion = 4.0


t = np.linspace(0, duracion, int(duracion * fs), endpoint=False)
signal = 0.5 * np.sin(2 * np.pi * 440 * t)


grabacion = reproducir_y_grabar(signal, fs, duracion_grabacion)

print(f"Muestras grabadas: {len(grabacion)}")
print(f"Duración grabación: {len(grabacion) / fs:.2f} s")
