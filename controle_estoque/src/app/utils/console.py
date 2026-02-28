import os
import time

# Limpar console
def limpar_console():
    os.system("cls" if os.name == "nt" else "clear")


def carregamento_pontos():
    print("...")
    time.sleep(.5)
    print("\033[A                             \033[A")
    print("..")
    time.sleep(.5)
    print("\033[A                             \033[A")
    time.sleep(.5)
    print(".")
    time.sleep(.5)
    print("\033[A                             \033[A")
