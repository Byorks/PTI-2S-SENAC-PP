import os

def arquivo_vazio(arquivo: str) -> bool:
    # Verifica se arquivo existe
    if not os.path.exists(arquivo):
        return True
    # Verifica se está vazio
    return os.path.getsize(arquivo) == 0

