"""
Script de diagnóstico: úsalo para verificar coordenadas.

1. Corre este script.
2. En los 5 segundos que tienes, pasa el mouse manualmente sobre el
   campo de "copiar texto" en Siigo y NO lo muevas.
3. El script imprimirá la posición real donde está el cursor.
4. Compara ese número con POS_COPIAR_TEXTO = (330, 448) en tu script
   principal. Si no coinciden, esas son las coordenadas correctas
   que debes usar.
"""
import time
import ctypes
try:
    ctypes.windll.user32.SetProcessDPIAware()
except Exception:
    pass

import pyautogui

print("Tienes 5 segundos: pon el mouse sobre el campo de texto en Siigo...")
for i in range(5, 0, -1):
    print(i)
    time.sleep(1)

x, y = pyautogui.position()
print(f"Posición real del cursor: ({x}, {y})")
