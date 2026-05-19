import sounddevice as sd

print("=== DISPOSITIVOS DISPONIBLES ===")
print(sd.query_devices())

print("\n=== DISPOSITIVOS POR DEFECTO ===")
print(sd.default.device)
