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



# ----------------- CONFIGURACIÓN -----------------


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
    pyperclip.copy(codigo)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(ESPERA_CORTA)
    enter()



# ----------------- CICLO PRINCIPAL -----------------

def main():
    print("Iniciando en 10 segundos... deja a Excel activo, con el cursor en la celda A2.")
    time.sleep(10)

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
        # 3. Pegar código
        pegar_codigo_en_siigo(codigo)

        # 4. Tab 4 veces
        pyautogui.press('tab') 
        pyautogui.press('tab') 
        pyautogui.press('tab') 
        pyautogui.press('tab') 
        time.sleep(ESPERA_CORTA)

        # 5. abajo una vez
        
        pyautogui.press('down')          # elije la primera opcion que es bogota      
        

        # 6. Enter
        enter()
        
        # 7. Tab 2 veces
        pyautogui.press('tab') 
        pyautogui.press('tab') 
        time.sleep(ESPERA_CORTA)

        # 8. abajo una vez
        pyautogui.press('down')

        # 9. Enter
        enter()

        # 10. Tab 2 veces
        pyautogui.press('tab') 
        pyautogui.press('tab') 

        # 11.Cambia ventana
        cambiar_ventana()

        # 12. ir a cantidad
        pyautogui.press('left') 
        pyautogui.press('left')

        # 13. Copiar cant 
        codigo = copiar_celda_actual_excel()

        # 14.Cambia ventana
        cambiar_ventana()

        # 15. Pegar código
        pegar_codigo_en_siigo(codigo)

        # 16. Tab 2 veces
        pyautogui.press('tab') 
        pyautogui.press('tab') 

        # 17.Cambia ventana
        cambiar_ventana()

        # 18. siguiente codigo
        pyautogui.press('right') 
        pyautogui.press('right') 
        pyautogui.press('down')

    print("Proceso terminado.")


if __name__ == "__main__":
    main()
