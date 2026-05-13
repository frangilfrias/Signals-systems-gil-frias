import numpy as np

from app.services.reproducir_grabar import reproducir_y_grabar

# ACÁ HABRÍA QUE PONER LA OPCIÓN PARA QUE EL USUARIO PUEDA ELEGIR CON QUÉ GRABAR, PORQUE SI NO HAY NADA ES POR DEFAULT
# POR EJEMPLO:
# import sounddevice as sd
# print(sd.default.device) AHÍ VEN LO QUE ESTÁ POR DEFAULT
# SI QUIEREN CAMBIAR POR OTRO DISPOSITIVO:
# import sounddevice as sd
# print(sd.query_devices()) ACÁ VEN CUAL QUIEREN
# sd.default.device = (input_id, output_id) ACÁ LO ELIGEN

fs = 44100
duracion = 2.0
duracion_grabacion = 4.0


t = np.linspace(0, duracion, int(duracion * fs), endpoint=False)
signal = 0.5 * np.sin(2 * np.pi * 440 * t)


grabacion = reproducir_y_grabar(signal, fs, duracion_grabacion)

print(f"Muestras grabadas: {len(grabacion)}")
print(f"Duración grabación: {len(grabacion) / fs:.2f} s")
