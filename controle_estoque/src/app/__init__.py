

"""_Centralização de funções_

from .controller.produtos import iniciar_cadastro
Nesse caso precisei criar um project.toml definindo o empacotador backend
Porque ele não estava localizando minha pasta com o main.py
Logo após a criação instalei o pacote
pip install -e .
Instalado corretamente agora com o seguinte comando ele executa o programa sem problemas
python -m app.main
-m quer dizer que main é o script principal

__all__ = [
   
    "iniciar_cadastro"
]

"""

