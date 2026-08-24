"""
CopiarPegarExcelSiigo.py

Automatiza el ciclo entre Excel y Siigo:
1. Copia el código de la columna A (fila N) en Excel
2. Cambia a Siigo con Alt+Tab, pega en (414,448), doble click, espera,
   Enter y click
3. En Siigo, triple click en (330,448) y copia el texto resultante
4. Cambia a Excel con Alt+Tab, mueve a columna B (misma fila) y pega
5. Vuelve a columna A y baja a la fila siguiente

Se detiene cuando la celda de columna A está vacía.

REQUISITOS:
    pip install pyautogui pyperclip

IMPORTANTE ANTES DE CORRER:
- Deben estar SOLO estas dos ventanas abiertas (Excel y Siigo), o el
  Alt+Tab rápido puede no alternar entre las correctas.
- Antes de correr el script, deja la ventana de Excel activa con el
  cursor ya parado en la celda A2 (o la fila donde quieras empezar).
  El script NO usa clicks ni Ctrl+G para ubicarse en Excel; solo usa
  flechas, así que la posición inicial de la celda activa importa.
- Verifica las coordenadas (414,448) y (330,448) en Siigo antes de
  correr el script; son coordenadas de pantalla.
- Deja el mouse quieto en la esquina superior izquierda (0,0) en
  cualquier momento para activar el "failsafe" de pyautogui y frenar
  el script de emergencia.
"""

import time
import ctypes
import pyautogui
import pyperclip

# En Windows, si la pantalla tiene escalado (125%, 150%, etc.), pyautogui
# puede calcular mal las coordenadas si el proceso no es "DPI aware".
# Esto corrige ese desfase entre las coordenadas capturadas y las reales.
try:
    ctypes.windll.user32.SetProcessDPIAware()
except Exception:
    pass


# ----------------- MOUSE DE BAJO NIVEL (API de Windows directa) -----------------
# Se usa ctypes directo en vez de pyautogui/pydirectinput para el mouse,
# porque ambas librerías normalizan las coordenadas (0-65535) y eso estaba
# calculando mal la posición real en este equipo. SetCursorPos coloca el
# pixel exacto sin ninguna conversión de por medio.

MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004


def mover_mouse(x: int, y: int):
    ctypes.windll.user32.SetCursorPos(x, y)


def click_mouse_simple(intervalo: float = 0.05):
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(intervalo)
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    time.sleep(intervalo)


def click_en(x: int, y: int, veces: int = 1):
    """Mueve el cursor a (x, y) y hace 'veces' clicks ahí (para doble/triple click)."""
    mover_mouse(x, y)
    time.sleep(0.1)
    for _ in range(veces):
        click_mouse_simple()

# ----------------- CONFIGURACIÓN -----------------

POS_PEGAR_CODIGO = (414, 448)   # Posición en Siigo donde se pega el código
POS_COPIAR_TEXTO = (230, 448)   # Posición en Siigo donde se copia el texto resultante

ESPERA_CORTA = 1
ESPERA_CAMBIO_VENTANA = 0.4     # Espera tras Alt+Tab, para que la ventana tome el foco

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.15


# ----------------- FUNCIONES -----------------

def enter():
    pyautogui.press("enter")
    time.sleep(ESPERA_CORTA)


def cambiar_ventana():
    """Alt+Tab rápido: alterna entre las dos últimas ventanas usadas."""
    pyautogui.keyDown('alt')
    pyautogui.press('tab')
    pyautogui.keyUp('alt')
    time.sleep(ESPERA_CAMBIO_VENTANA)


def copiar_celda_actual_excel() -> str:
    """Copia la celda actualmente seleccionada en Excel y devuelve el contenido."""
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.2)
    return pyperclip.paste()


def pegar_codigo_en_siigo(codigo: str):
    """Doble click en el campo de código, pega, espera, Enter y confirma con click."""
    click_en(*POS_PEGAR_CODIGO, veces=1)
    time.sleep(0.5)
    click_en(*POS_PEGAR_CODIGO, veces=1)
    pyperclip.copy(codigo)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(ESPERA_CORTA)
    enter()


def copiar_texto_de_siigo() -> str:
    """Triple click sobre el texto resultante en Siigo y lo copia."""
    time.sleep(ESPERA_CORTA)   # da tiempo a que Siigo termine de cargar el campo
    print(f"  [debug] posición ANTES de mover: {pyautogui.position()}")
    click_en(*POS_COPIAR_TEXTO, veces=3)
    print(f"  [debug] posición DESPUÉS de mover (objetivo {POS_COPIAR_TEXTO}): {pyautogui.position()}")
    time.sleep(0.2)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.2)
    return pyperclip.paste()


# ----------------- CICLO PRINCIPAL -----------------

def main():
    print("Iniciando en 7 segundos... deja a Excel activo, con el cursor en la celda A2.")
    time.sleep(7)

    fila = 2

    while True:
        # 1. Copiar código desde la celda actual de Excel (columna A)
        codigo = copiar_celda_actual_excel().strip()

        if not codigo:
            print(f"Fila {fila}, columna A vacía. Fin del proceso.")
            break

        print(f"Fila {fila}: código '{codigo}'")

        # 2. Cambiar a Siigo y pegar el código
        cambiar_ventana()
        pegar_codigo_en_siigo(codigo)

        # 3. Copiar texto resultante en Siigo
        texto_resultado = copiar_texto_de_siigo()
        print(f"  -> Resultado de Siigo: '{texto_resultado}'")

        # 4. Volver a Excel, mover a columna B (misma fila) y pegar
        cambiar_ventana()
        pyautogui.press('right')          # de columna A a columna B, misma fila
        pyperclip.copy(texto_resultado)
        pyautogui.hotkey('ctrl', 'v')

        # 5. Volver a columna A y bajar a la siguiente fila
        pyautogui.press('left')           # de vuelta a columna A
        pyautogui.press('down')           # siguiente fila
        fila += 1

    print("Proceso terminado.")


if __name__ == "__main__":
    main()
