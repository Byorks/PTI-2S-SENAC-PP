
from ..models.produto import Produto
from ..repositories.produtos import ProdutoRepository

class ProdutoService: 
    # Injeção de dependência
    # Aqui estamos definindo que PessoaService espera receber um repository que seja ou herde
    # de ProdutoRepository, dessa forma evita acoplamento inserindo o ProdutoRepository
    # diretamente dentro da ProdutosService
    def __init__(self, repo: ProdutoRepository):
    # Armazena o repositório recebido como um atributo de instância
    # Dessa forma conseguimos chamar a qualquer momento dentro da ProdutoService 
    # self.repo.adicionar()
     self.repo = repo

    def cadastrar(self, codigo: str, nome: str, preco: float, quantidade: int) -> Produto:
        # Validações
        
        # verificar se cod já existe
        # Posso criar uma busca por cod, se retornar False(Não encontrado), pode continuar
        # Ou se encontrar, dá erro
        
        # verificar se o preço ou estoque não está negativo
        if preco < 0:
            raise ValueError("Preços negativos não são permitidos.")
        
        if quantidade < 0:
            raise ValueError("Quantidades negativas não são permitidas.")
        
        
        
        # Após verificação montar entidade
        novo_produto = Produto (
            codigo=codigo,
            nome= nome.strip().title(),
            preco=preco,
            quantidade=quantidade
        )
        print(novo_produto)
        
        self.repo.adicionar(novo_produto)
        return novo_produto
    
    def listar_todos(self) -> list[Produto]:
       return self.repo.listar_todos()