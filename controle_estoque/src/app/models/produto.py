from dataclasses import dataclass, field
import uuid
from datetime import date

# @dataclass(frozen=True) frozen para tornar a entidade imutável
@dataclass (frozen=True) # Não permite alterações na entidade
# Parâmetros com valor default dever vir após parâmetros obrigatórios, do contrário dá erro
class Produto:
    codigo: str
    nome: str
    preco: float
    quantidade: int
    id: uuid.UUID = field(default_factory=uuid.uuid4) # o init=False diz que ao criar um prod ele não precisa passar o argumento id, mas na hora de montar novamente a entidade dá problema
    
    # __post_init__ opcional para validações extras após criação
    def __post_init__(self):
        if not self.codigo:
            raise ValueError("Código obrigatório")